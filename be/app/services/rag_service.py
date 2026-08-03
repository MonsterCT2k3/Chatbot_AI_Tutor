import os
import re
from typing import List, Tuple

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from ddgs import DDGS

from app.core.config import settings

class RAGService:
    def __init__(self, data_dir: str):
        # 1. Initialize the Search Engine (Vector)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY)
        
        db_dir = os.path.join(data_dir, "chroma_db")
        self.vector_db = Chroma(persist_directory=db_dir, embedding_function=self.embeddings)
        
        # Pre-load all documents for BM25
        chroma_data = self.vector_db.get()
        self.all_docs = []
        for text, metadata in zip(chroma_data['documents'], chroma_data['metadatas']):
            self.all_docs.append(Document(page_content=text, metadata=metadata))
            
        # 2. Initialize the AI Agent (Generation) using OpenRouter
        self.llm = ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4o-mini" 
        )
        
        # 3. Create Prompts
        self.evaluator_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a smart router for an AI Tutor.
            Read the provided context chunks and the user's question.
            Determine which of the following 3 actions to take:
            
            1. If the context contains the answer to the question -> Output exactly: [ANSWER]
            2. If the context DOES NOT contain the answer, AND the question is related to AI, Tech, Product, or the course -> Output exactly: [WEB_SEARCH]
            3. If the context DOES NOT contain the answer, AND the question is completely irrelevant (e.g., cooking, weather, sports) -> Output exactly: [IRRELEVANT]
            
            Output ONLY one of the bracketed actions. Nothing else.
            
            Context from lessons:
            {context}"""),
            ("user", "{question}")
        ])
        self.evaluator_chain = self.evaluator_prompt | self.llm
        
        self.rewrite_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a search query optimization assistant. Your task is to generate 3 different variations of the user's question to help a search engine find the best results.
            - Variation 1: Fix spelling, capitalize abbreviations (e.g., 'ai' -> 'AI'), and spell out numbers to words (e.g., '3' -> 'Ba').
            - Variation 2: Use synonyms and expand abbreviations (e.g., 'AI' -> 'Trí tuệ nhân tạo').
            - Variation 3: Keep it extremely simple, focusing only on the core keywords (e.g., 'Ba nhóm AI chính').
            - Keep the language in Vietnamese.
            - Output ONLY the 3 questions, separated by newlines. Do not include numbers, bullets, or any other text.
            """),
            ("user", "{question}")
        ])
        self.rewrite_chain = self.rewrite_prompt | self.llm
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI Tutor. 
            Answer the user's question using ONLY the context provided below. 
            If the context does not contain the answer, politely say you don't know based on the provided information.
            
            CRITICAL RULE 1: You MUST cite your sources! The context below contains tags like [Slide X] or [Nguồn: Internet]. 
            Whenever you state a fact or provide information, you must add the source tag at the end of the sentence or paragraph.
            Example 1: Trí tuệ nhân tạo có 3 nhóm chính [Slide 15].
            Example 2: Thông tin mới nhất cho thấy... [Nguồn: Internet].
            
            CRITICAL RULE 2: At the end of your response, you MUST suggest exactly 3 follow-up questions that the user can ask to learn more about the current topic. 
            Format them under a bold heading: "**💡 Gợi ý tìm hiểu thêm:**".
            
            Please answer in Vietnamese.
            
            Context:
            {context}"""),
            ("user", "{question}")
        ])
        self.generation_chain = self.prompt_template | self.llm
        
        # Web search
        self.ddgs = DDGS()

    def _multi_query_hybrid_search(self, queries: List[str], bm25_retriever, chroma_retriever, k=6) -> List[Document]:
        scores = {}
        doc_metadata = {}
        
        for question in queries:
            docs_bm25 = bm25_retriever.invoke(question)
            docs_chroma = chroma_retriever.invoke(question)
            
            for rank, doc in enumerate(docs_bm25):
                content = doc.page_content
                scores[content] = scores.get(content, 0) + 1.0 / (rank + 60)
                doc_metadata[content] = doc.metadata
                
            for rank, doc in enumerate(docs_chroma):
                content = doc.page_content
                scores[content] = scores.get(content, 0) + 1.0 / (rank + 60)
                doc_metadata[content] = doc.metadata
                
        sorted_contents = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        top_contents = sorted_contents[:k]
        return [Document(page_content=c, metadata=doc_metadata[c]) for c in top_contents]

    def ask(self, question: str, target_lesson: str = None) -> Tuple[str, str, List[str]]:
        """
        Returns: (answer_text, action_taken, list_of_follow_ups)
        """
        # Setup retrievers for specific lesson if needed
        if target_lesson:
            target_source = f"{target_lesson}_full_rag_ready.md"
            bm25_docs = [d for d in self.all_docs if d.metadata.get("source") == target_source]
            if not bm25_docs:
                bm25_docs = self.all_docs
                chroma_retriever = self.vector_db.as_retriever(search_kwargs={"k": 6})
            else:
                chroma_retriever = self.vector_db.as_retriever(search_kwargs={"k": 6, "filter": {"source": target_source}})
        else:
            bm25_docs = self.all_docs
            chroma_retriever = self.vector_db.as_retriever(search_kwargs={"k": 6})
            
        bm25_retriever = BM25Retriever.from_documents(bm25_docs)
        bm25_retriever.k = 6
        
        # A. Multi-Query
        rewritten_response = self.rewrite_chain.invoke({"question": question})
        queries = [q.strip() for q in rewritten_response.content.strip().split('\n') if q.strip()]
        if question not in queries:
            queries.append(question)
            
        # B. Hybrid Search
        docs = self._multi_query_hybrid_search(queries, bm25_retriever, chroma_retriever, k=6)
        
        context_chunks = []
        for doc in docs:
            page_num = doc.metadata.get('page_number', 'Unknown')
            context_chunks.append(f"[Slide {page_num}]\n{doc.page_content}")
            
        context_text = "\n\n---\n\n".join(context_chunks)
        
        # C. Evaluation
        eval_response = self.evaluator_chain.invoke({"context": context_text, "question": question})
        action = eval_response.content.strip().upper()
        
        if "[IRRELEVANT]" in action:
            return ("Xin lỗi, tôi là AI Tutor của khóa học K3. Tôi chỉ giải đáp các thắc mắc liên quan đến bài học và công nghệ. Vui lòng hỏi đúng chủ đề!", "[IRRELEVANT]", [])
            
        if "[WEB_SEARCH]" in action:
            try:
                web_results = self.ddgs.text(question, max_results=3)
                web_text = "\n".join([f"- {r.get('title')}: {r.get('body')}" for r in web_results])
                context_text = f"[Nguồn: Internet]\n{web_text}"
                action = "[WEB_SEARCH]"
            except Exception as e:
                return (f"Xin lỗi, tôi không thể tìm thấy thông tin này trong bài học và việc tra cứu Internet cũng gặp lỗi.", "[ERROR]", [])
        else:
            action = "[ANSWER]"
            
        # D. Generation
        response = self.generation_chain.invoke({
            "context": context_text,
            "question": question
        })
        full_text = response.content
        
        # Parse follow up questions from the response
        parts = full_text.split("**💡 Gợi ý tìm hiểu thêm:**")
        answer_text = parts[0].strip()
        follow_ups = []
        
        if len(parts) > 1:
            follow_up_text = parts[1].strip()
            # extract lines that look like list items or numbers
            for line in follow_up_text.split('\n'):
                clean_line = re.sub(r'^[\d\.\-\*\s]+', '', line).strip()
                if clean_line:
                    follow_ups.append(clean_line)
                    
        return (answer_text, action, follow_ups)

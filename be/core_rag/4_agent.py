import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

# Load environment variables
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
load_dotenv(os.path.join(project_root, ".env"))

def multi_query_hybrid_search(queries, bm25_retriever, chroma_retriever, k=6):
    scores = {}
    doc_metadata = {}
    
    for question in queries:
        # 1. Get results from both Search Engines for this specific query variation
        docs_bm25 = bm25_retriever.invoke(question)
        docs_chroma = chroma_retriever.invoke(question)
        
        # 2. Combine them using Reciprocal Rank Fusion (RRF)
        for rank, doc in enumerate(docs_bm25):
            content = doc.page_content
            scores[content] = scores.get(content, 0) + 1.0 / (rank + 60)
            doc_metadata[content] = doc.metadata
            
        for rank, doc in enumerate(docs_chroma):
            content = doc.page_content
            scores[content] = scores.get(content, 0) + 1.0 / (rank + 60)
            doc_metadata[content] = doc.metadata
            
    # 3. Sort by the highest score across ALL queries and engines
    sorted_contents = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    
    # 4. Return the Top K results
    top_contents = sorted_contents[:k]
    return [Document(page_content=c, metadata=doc_metadata[c]) for c in top_contents]


def run_agent():
    DB_DIR = os.path.join(current_dir, "chroma_db")
    
    # 1. Initialize the Search Engine (Vector)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    # 2. Initialize the AI Agent (Generation) using OpenRouter
    llm = ChatOpenAI(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model="openai/gpt-4o-mini" 
    )
    
    # 3. Create the System Prompts
    
    # --- NEW: Evaluator Prompt (Smart Router) ---
    evaluator_prompt = ChatPromptTemplate.from_messages([
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
    evaluator_chain = evaluator_prompt | llm
    
    # --- NEW: Query Rewriter Prompt (Multi-Query) ---
    rewrite_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a search query optimization assistant. Your task is to generate 3 different variations of the user's question to help a search engine find the best results.
        - Variation 1: Fix spelling, capitalize abbreviations (e.g., 'ai' -> 'AI'), and spell out numbers to words (e.g., '3' -> 'Ba').
        - Variation 2: Use synonyms and expand abbreviations (e.g., 'AI' -> 'Trí tuệ nhân tạo').
        - Variation 3: Keep it extremely simple, focusing only on the core keywords (e.g., 'Ba nhóm AI chính').
        - Keep the language in Vietnamese.
        - Output ONLY the 3 questions, separated by newlines. Do not include numbers, bullets, or any other text.
        """),
        ("user", "{question}")
    ])
    rewrite_chain = rewrite_prompt | llm
    
    # --- EXISTING: Answer Generation Prompt ---
    prompt_template = ChatPromptTemplate.from_messages([
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
    
    # Initialize Web Search Tool
    web_search = DuckDuckGoSearchRun()
    
    print("\n" + "="*50)
    print("🤖 AI TUTOR AGENT IS READY!")
    print("="*50)
    
    target_lesson = input("Which lesson do you want to ask about? (e.g., type 'b1' or leave empty for ALL): ").strip()
    
    print("\n⏳ Preparing Hybrid Search Engine (Vector + BM25)...")
    # A. Extract all data from Chroma
    chroma_data = vector_db.get()
    all_docs = []
    for text, metadata in zip(chroma_data['documents'], chroma_data['metadatas']):
        all_docs.append(Document(page_content=text, metadata=metadata))
        
    # B. Filter documents for BM25 if the user selected a specific lesson
    if target_lesson:
        target_source = f"{target_lesson}_full_rag_ready.md"
        bm25_docs = [d for d in all_docs if d.metadata.get("source") == target_source]
        
        # If the user typed an invalid lesson name (e.g., a whole question)
        if not bm25_docs:
            print(f"⚠️  Cảnh báo: Không tìm thấy bài học nào tên là '{target_lesson}'. Hệ thống sẽ tìm kiếm trên TẤT CẢ các bài học.")
            target_lesson = ""
            bm25_docs = all_docs
            chroma_retriever = vector_db.as_retriever(search_kwargs={"k": 6})
        else:
            chroma_retriever = vector_db.as_retriever(search_kwargs={"k": 6, "filter": {"source": target_source}})
    else:
        bm25_docs = all_docs
        chroma_retriever = vector_db.as_retriever(search_kwargs={"k": 6})
        
    # C. Initialize BM25 Retriever
    bm25_retriever = BM25Retriever.from_documents(bm25_docs)
    bm25_retriever.k = 6
    
    print(f"✅ Hybrid Search Engine Ready!")

    while True:
        question = input(f"\nAsk the AI Tutor about {target_lesson if target_lesson else 'ALL lessons'} (or type 'quit' to stop): ")
        if question.lower() == 'quit':
            break
            
        print("\n⏳ Thinking...")
        
        # --- Step A: Multi-Query Generation ---
        rewritten_response = rewrite_chain.invoke({"question": question})
        # Split the response into a list of queries by newlines
        queries = [q.strip() for q in rewritten_response.content.strip().split('\n') if q.strip()]
        
        # Always include the original exact question just in case
        if question not in queries:
            queries.append(question)
            
        print(f"   [Multi-Query] Đang tìm kiếm bằng {len(queries)} biến thể câu hỏi khác nhau...")
        for i, q in enumerate(queries):
            print(f"      {i+1}. {q}")
        
        # --- Step B: Search for context (Multi-Query Hybrid Retrieval) ---
        docs = multi_query_hybrid_search(queries, bm25_retriever, chroma_retriever, k=6)
        
        # Combine the text and INJECT the metadata so the LLM knows where it came from
        context_chunks = []
        for doc in docs:
            page_num = doc.metadata.get('page_number', 'Unknown')
            
            chunk_with_source = f"[Slide {page_num}]\n{doc.page_content}"
            context_chunks.append(chunk_with_source)
            
        context_text = "\n\n---\n\n".join(context_chunks)
        
        # --- NEW: Step C: Evaluation (Evaluate Context) ---
        eval_response = evaluator_chain.invoke({
            "context": context_text,
            "question": question
        })
        action = eval_response.content.strip().upper()
        
        if "[IRRELEVANT]" in action:
            print("\n🎓 AI Tutor: Xin lỗi, tôi là AI Tutor của khóa học K3. Tôi chỉ giải đáp các thắc mắc liên quan đến bài học và công nghệ. Vui lòng hỏi đúng chủ đề!")
            continue
            
        if "[WEB_SEARCH]" in action:
            print(f"   [Evaluator] Câu hỏi '{question}' không có trong tài liệu. Đang tìm kiếm trên Internet...")
            try:
                web_results = web_search.invoke(question)
                context_text = f"[Nguồn: Internet]\n{web_results}"
                print("   [Web Search] Đã lấy được dữ liệu từ Internet!")
            except Exception as e:
                print(f"   [Web Search Lỗi] {e}")
                print("\n🎓 AI Tutor: Xin lỗi, tôi không thể tìm thấy thông tin này trong bài học và việc tra cứu Internet cũng gặp lỗi.")
                continue
        else:
            # If [ANSWER], proceed normally
            print("   [Evaluator] Đã tìm thấy thông tin trong tài liệu!")
        
        # --- Step D: Ask the AI (Generation) ---
        # We pass the original question and the context we just found to the Prompt
        chain = prompt_template | llm
        
        response = chain.invoke({
            "context": context_text,
            "question": question
        })
        
        print(f"\n🎓 AI Tutor:\n{response.content}\n")
        
if __name__ == "__main__":
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY is not set in your .env file!")
    elif not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY is not set in your .env file! (We still need it for searching)")
    else:
        run_agent()

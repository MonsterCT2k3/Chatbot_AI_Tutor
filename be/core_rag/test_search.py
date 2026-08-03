import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
load_dotenv(os.path.join(project_root, ".env"))

def hybrid_search(question, bm25_retriever, chroma_retriever, k=6):
    docs_bm25 = bm25_retriever.invoke(question)
    docs_chroma = chroma_retriever.invoke(question)
    scores = {}
    doc_metadata = {}
    for rank, doc in enumerate(docs_bm25):
        content = doc.page_content
        scores[content] = scores.get(content, 0) + 1.0 / (rank + 60)
        doc_metadata[content] = doc.metadata
    for rank, doc in enumerate(docs_chroma):
        content = doc.page_content
        scores[content] = scores.get(content, 0) + 1.0 / (rank + 60)
        doc_metadata[content] = doc.metadata
    sorted_contents = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [Document(page_content=c, metadata=doc_metadata[c]) for c in sorted_contents[:k]]

DB_DIR = os.path.join(current_dir, "chroma_db")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

chroma_data = vector_db.get()
all_docs = [Document(page_content=text, metadata=metadata) for text, metadata in zip(chroma_data['documents'], chroma_data['metadatas'])]
target_source = "b1_full_rag_ready.md"
bm25_docs = [d for d in all_docs if d.metadata.get("source") == target_source]
chroma_retriever = vector_db.as_retriever(search_kwargs={"k": 6, "filter": {"source": target_source}})
bm25_retriever = BM25Retriever.from_documents(bm25_docs)
bm25_retriever.k = 6

docs = hybrid_search("Ba nhóm trí tuệ nhân tạo (AI) chính là gì?", bm25_retriever, chroma_retriever, k=6)
for i, doc in enumerate(docs):
    print(f"\n--- Rank {i+1} ---")
    print(doc.page_content[:200] + "...")

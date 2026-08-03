import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
load_dotenv(os.path.join(project_root, ".env"))

DB_DIR = os.path.join(current_dir, "chroma_db")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

retriever = vector_db.as_retriever(search_kwargs={"k": 6})
docs = retriever.invoke("3 nhóm AI chính là gì?")

print("Vector Search Top 6:")
for i, doc in enumerate(docs):
    print(f"{i+1}. {doc.page_content[:150]}")

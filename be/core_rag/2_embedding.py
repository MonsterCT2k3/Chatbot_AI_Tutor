import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# We can just import 1_chunking directly since it's in the same folder now
import importlib
chunking_module = importlib.import_module("1_chunking")
load_and_chunk_directory = chunking_module.load_and_chunk_directory

# Load environment variables (like OPENAI_API_KEY) from .env file
# Go up one folder to find the .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
load_dotenv(os.path.join(project_root, ".env"))

def create_vector_db():
    DATA_DIR = os.path.join(project_root, "pdf_extract", "output_ocr", "full_rag_ready")
    DB_DIR = os.path.join(current_dir, "chroma_db") # The folder where our database will be saved
    
    print("1. Loading and Chunking documents...")
    all_chunks = load_and_chunk_directory(DATA_DIR)
    print(f"-> Total chunks ready to embed: {len(all_chunks)}\n")
    
    print("2. Initializing OpenAI Embeddings...")
    # This uses the text-embedding-3-small model which is fast and cheap
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    print(f"3. Creating Vector Database in '{DB_DIR}'...")
    print("   (This will send chunks to OpenAI to convert them to vectors. It might take a minute!)")
    
    # Create the database and save it to the DB_DIR folder
    vector_db = Chroma.from_documents(
        documents=all_chunks, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    
    print("\n✅ Success! The Vector Database has been created and saved locally.")
    print("You can now search for information very quickly!")

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY is not set in your .env file!")
    else:
        create_vector_db()

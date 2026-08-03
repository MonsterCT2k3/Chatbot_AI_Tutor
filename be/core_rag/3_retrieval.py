import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
load_dotenv(os.path.join(project_root, ".env"))

def run_search_engine():
    DB_DIR = os.path.join(current_dir, "chroma_db")
    
    # 1. Initialize the same Embedding model we used to create the database
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # 2. Connect to our existing local database
    print("Connecting to the Vector Database...")
    vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    print("\n" + "="*50)
    print("🔍 AI SEARCH ENGINE IS READY!")
    print("="*50)
    
    # Ask which lesson to search
    target_lesson = input("Which lesson do you want to search? (e.g., type 'b3' or leave empty for ALL): ").strip()
    
    # 3. Create a loop so you can keep asking questions
    while True:
        question = input(f"\nAsk a question about {target_lesson if target_lesson else 'ALL lessons'} (or type 'quit' to stop): ")
        
        if question.lower() == 'quit':
            break
            
        print("\nSearching...")
        
        # 4. Perform the Vector Similarity Search WITH METADATA FILTER!
        if target_lesson:
            # We filter by the "source" metadata we added in Phase 1
            filter_dict = {"source": f"{target_lesson}_full_rag_ready.md"}
            results = vector_db.similarity_search(question, k=3, filter=filter_dict)
        else:
            results = vector_db.similarity_search(question, k=3)
        
        # 5. Print out the results so we can see what the DB found
        print(f"\n✅ Found {len(results)} matches for your question:")
        for i, doc in enumerate(results):
            print(f"\n--- Match {i+1} ---")
            print(f"Metadata (Source info): {doc.metadata}")
            print(f"Content:\n{doc.page_content}")
            print("-" * 20)

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY is not set in your .env file!")
    else:
        run_search_engine()

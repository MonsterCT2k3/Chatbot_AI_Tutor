import os
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

import re

def load_and_chunk_directory(directory_path):
    all_chunks = []
    
    # 2. Define the Markdown headers we want to split by
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )
    
    # Create a secondary Splitter
    chunk_size = 500
    chunk_overlap = 50
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )

    # We only process b1_full_rag_ready.md to save API tokens during testing!
    filename = "b1_full_rag_ready.md"
    file_path = os.path.join(directory_path, filename)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        
        # Split text by page marker using Regex
        parts = re.split(r'<!-- START PAGE (\d+) -->', md_text)
        
        # Process text before the first page marker (if any)
        if parts[0].strip():
            md_header_splits = markdown_splitter.split_text(parts[0])
            final_chunks = text_splitter.split_documents(md_header_splits)
            for chunk in final_chunks:
                chunk.metadata["source"] = filename
                chunk.metadata["page_number"] = "0"
            all_chunks.extend(final_chunks)
            
        # Process each page
        for i in range(1, len(parts), 2):
            page_num = parts[i]
            page_content = parts[i+1]
            
            # Remove the END PAGE marker
            page_content = re.sub(r'<!-- END PAGE \d+ -->', '', page_content)
            
            # Split the page document based on headers
            md_header_splits = markdown_splitter.split_text(page_content)
            final_chunks = text_splitter.split_documents(md_header_splits)
            
            # Add the filename and page number to the metadata
            for chunk in final_chunks:
                chunk.metadata["source"] = filename
                chunk.metadata["page_number"] = page_num
                
            all_chunks.extend(final_chunks)
            
        print(f"Loaded {filename}: {len(all_chunks)} chunks with page numbers.")
    else:
        print(f"File not found: {file_path}")

    print(f"\nTotal chunks generated: {len(all_chunks)}")
    
    # Print the first 2 chunks to inspect the result
    print("\n=== INSPECTING FIRST 2 CHUNKS ===")
    for i in range(min(2, len(all_chunks))):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Metadata (Headers): {all_chunks[i].metadata}")
        print(f"Content:\n{all_chunks[i].page_content}")
        print("-" * 20)
        
    return all_chunks

if __name__ == "__main__":
    # Calculate the path from the core_rag folder back to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, "..")
    DATA_DIR = os.path.join(project_root, "pdf_extract", "output_ocr", "full_rag_ready")
    
    if os.path.exists(DATA_DIR):
        load_and_chunk_directory(DATA_DIR)
    else:
        print(f"Directory not found: {DATA_DIR}. Please check the path.")

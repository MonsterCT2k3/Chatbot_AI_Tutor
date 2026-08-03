import re
with open("/run/media/monsterct2k3/Storages/Documents/Workspace/vinai/hackathon day5/Batch03-K3-AI-Product-Hackathon/pdf_extract/output_ocr/full_rag_ready/b1_full_rag_ready.md", "r") as f:
    text = f.read()

parts = re.split(r'<!-- START PAGE (\d+) -->', text)
for i in range(1, min(len(parts), 6), 2):
    page_num = parts[i]
    content = parts[i+1][:100]
    print(f"Page {page_num}: {content.strip()}")

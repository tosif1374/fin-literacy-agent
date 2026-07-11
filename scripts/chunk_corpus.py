# scripts/02_chunk_corpus.py
import csv, json
from pypdf import PdfReader

CHUNK_SIZE = 700     # tokens (approx, using words as proxy)
CHUNK_OVERLAP = 100

def extract_text(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return chunks

def main():
    all_chunks = []
    with open("data/manifest.csv") as f:
        for row in csv.DictReader(f):
            path = f"data/raw/{row['file']}"
            text = extract_text(path)
            for i, chunk in enumerate(chunk_text(text)):
                all_chunks.append({
                    "id": f"{row['file']}_{i}",
                    "text": chunk,
                    "topic": row["topic"],
                    "source": row["source"],
                    "url": row["url"],
                })
    with open("data/chunks.jsonl", "w") as out:
        for c in all_chunks:
            out.write(json.dumps(c) + "\n")
    print(f"Wrote {len(all_chunks)} chunks")

if __name__ == "__main__":
    main()
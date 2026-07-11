# scripts/03_build_vectorstore.py
import json
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection("fin_literacy")

chunks = [json.loads(l) for l in open("data/chunks.jsonl")]

texts = [c["text"] for c in chunks]
embeddings = model.encode(texts, show_progress_bar=True).tolist()

collection.add(
    ids=[c["id"] for c in chunks],
    embeddings=embeddings,
    documents=texts,
    metadatas=[{"topic": c["topic"], "source": c["source"], "url": c["url"]} for c in chunks],
)
print("Vector store built:", collection.count(), "chunks")
import re
import json
import chromadb
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

_client = chromadb.PersistentClient(path="data/chroma_db")

# Try loading existing collection
try:
    _collection = _client.get_collection("fin_literacy")

# If collection missing (Streamlit Cloud), rebuild it
except Exception:
    _collection = _client.get_or_create_collection("fin_literacy")

    chunks = [json.loads(l) for l in open("data/chunks.jsonl", encoding="utf-8")]

    texts = [c["text"] for c in chunks]
    embeddings = _model.encode(texts, show_progress_bar=False).tolist()

    _collection.add(
        ids=[c["id"] for c in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {
                "topic": c["topic"],
                "source": c["source"],
                "url": c["url"],
            }
            for c in chunks
        ],
    )

PII_PATTERNS = [
    r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    r"\bupi\s*pin\b",
    r"\botp\b",
]

def contains_pii_request(query: str) -> bool:
    q = query.lower()
    return any(re.search(p, q) for p in PII_PATTERNS)

def retrieve(query: str, k: int = 4):
    embedding = _model.encode([query]).tolist()

    results = _collection.query(
        query_embeddings=embedding,
        n_results=k
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    return list(zip(docs, metas))
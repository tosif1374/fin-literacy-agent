# app/retriever.py
import re
import chromadb
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")
_client = chromadb.PersistentClient(path="data/chroma_db")
_collection = _client.get_collection("fin_literacy")

PII_PATTERNS = [
    r"\b\d{4}\s?\d{4}\s?\d{4}\b",     # card/aadhaar-like number
    r"\bupi\s*pin\b",
    r"\botp\b",
]

def contains_pii_request(query: str) -> bool:
    q = query.lower()
    return any(re.search(p, q) for p in PII_PATTERNS)

def retrieve(query: str, k: int = 4):
    embedding = _model.encode([query]).tolist()
    results = _collection.query(query_embeddings=embedding, n_results=k)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return list(zip(docs, metas))
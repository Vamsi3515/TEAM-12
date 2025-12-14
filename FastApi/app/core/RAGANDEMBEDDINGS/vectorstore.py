from __future__ import annotations
import os
import chromadb

# Use PersistentClient (recommended) and a stable path under data/
DB_PATH = os.path.join("data", "chroma")
os.makedirs(DB_PATH, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=DB_PATH)

def get_or_create_collection(name: str = "portfolio_knowledge"):
    # Metadata like hnsw:space may be ignored depending on backend; kept for compatibility.
    return chroma_client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})
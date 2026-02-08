#!/usr/bin/env python3

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

qdrant = QdrantClient("http://localhost:6333")
print(qdrant.count("kb"))


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embs = model.encode(["Who was Ray's brother?"])

print(qdrant.query_points(
                    "kb",
                    query=embs[0],
                    limit=3,
                ))
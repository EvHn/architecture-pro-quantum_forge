#!/usr/bin/env python3

import os
import random
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

qdrant = QdrantClient("http://localhost:6333")
qdrant.create_collection(
        collection_name="kb",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

files = [f for f in os.listdir('../Task2/knowledge_base')]

text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def generate_time_based_id():
    t = int(time.time() * 1000)  # миллисекунды
    rand = random.randint(0, 999)
    return (t << 10) | rand

for j, file in enumerate(files):
    with open('../Task2/knowledge_base/' + file, 'r', encoding='utf-8') as f:
        text = f.read()
    # print(f"File name: {file}")

    chunks = text_splitter.split_text(text)
    # print(f"Chanks: {len(chunks)}")

    embs = model.encode(chunks)

    qdrant.upsert(
        collection_name="kb",
        points=[
            PointStruct(
                id=generate_time_based_id(),
                vector=emb,
                payload={
                    "path": file,
                    "text": chunks[idx],
                    "lang": "en",
                    "chunk_index": generate_time_based_id(),
                },
            )
            for idx, emb in enumerate(embs)
        ],
    )

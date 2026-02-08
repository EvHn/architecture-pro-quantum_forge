#!/usr/bin/env python3

import os
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

for j, file in enumerate(files):
    with open('../Task2/knowledge_base/' + file, 'r', encoding='utf-8') as f:
        large_text = f.read()
    # print(f"File name: {file}")

    # Initialize the splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_text(large_text)
    # print(f"Chanks: {len(chunks)}")

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embs = model.encode(chunks)

    qdrant.upsert(
        collection_name="kb",
        points=[
            PointStruct(
                id=100000 * j + idx,
                vector=emb,
                payload={
                    "path": file,
                    "text": chunks[idx],
                    "lang": "en",
                    "chunk_index": 100000 * j + idx,
                },
            )
            for idx, emb in enumerate(embs)
        ],
    )

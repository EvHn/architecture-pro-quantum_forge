
import sys
from pathlib import Path
import random
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from datetime import date

qdrant = QdrantClient("http://localhost:6333")

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

def main():
    # Получаем директорию из аргументов командной строки
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])
    else:
        root = Path.cwd()

    if not root.is_dir():
        print(f"Ошибка: '{root}' не является директорией или не существует.", file=sys.stderr)
        sys.exit(1)

    errors = 0
    added = 0
    now = time.time()
    one_day = 24 * 60 * 60  # 86400 секунд
    chunkCountBefor = qdrant.count('kb')
 
    for item in root.iterdir():
        if not item.is_file():
            continue
        try:
            mtime = item.stat().st_mtime
            if now - mtime > one_day:
                continue
        except OSError:
            errors+=1
            continue

        try:
            with open(item, 'r', encoding='utf-8') as f:
                text = f.read()
        except (UnicodeDecodeError, OSError):
            errors+=1
            print(f"Ошибка при чтении файла: {item}")
            continue

        chunks = text_splitter.split_text(text)
 
        embs = model.encode(chunks)

        qdrant.upsert(
            collection_name="kb",
            points=[
                PointStruct(
                    id=generate_time_based_id(),
                    vector=emb,
                    payload={
                        "path": item,
                        "text": chunks[idx],
                        "lang": "en",
                        "chunk_index": generate_time_based_id(),
                    },
                )
                for idx, emb in enumerate(embs)
            ],
        )
        added+=1

    totalChunks = qdrant.count('kb')
    print(f"Index updated at {date.today().strftime('%Y-%m-%d')}, {added} files added, {errors} errors.")
    print(f"Chunks added: {totalChunks.count - chunkCountBefor.count}, Total chunks: {totalChunks.count}")
if __name__ == '__main__':
    main()
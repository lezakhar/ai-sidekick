import json

import sys
import os
import hashlib

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import configs


def _text_to_int_id(text: str, max_bits: int = 64) -> int:
    hash_bytes = hashlib.sha256(text.encode()).digest()[: max_bits // 8]
    return int.from_bytes(hash_bytes, byteorder="big", signed=False)


def _get_knowledges(path_to_knowledges: str) -> list[dict]:
    try:
        with open(path_to_knowledges, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {path_to_knowledges} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"No valid JSON: {e}")
        return []


def add_payloads():
    payloads = _get_knowledges(path_to_knowledges=f"{configs.FILE_PATH}.json")

    client = QdrantClient(
        url=configs.QDRANT_URL,
        port=None,
        https=True,
    )

    model = SentenceTransformer(configs.ENCODER)

    if not client.collection_exists(collection_name=configs.QDRANT_COLLECTION_NAME):
        client.create_collection(
            collection_name=configs.QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE,
            ),
        )

    points = []
    for payload in payloads:
        embedding = model.encode(
            payload["title"],
            normalize_embeddings=True,
        ).tolist()

        points.append(
            models.PointStruct(
                id=_text_to_int_id(payload["title"]),
                vector=embedding,
                payload=payload,
            )
        )

    client.upsert(
        collection_name=configs.QDRANT_COLLECTION_NAME,
        points=points,
    )
    print(f"Succesfully added {len(points)} points")


if __name__ == "__main__":
    add_payloads()

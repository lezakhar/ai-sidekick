import json

from qdrant_client import QdrantClient
from qdrant_client.http import models

import configs

from point import Point


client = QdrantClient(
    url=configs.QDRANT_URL,
    port=None,
    https=True,
)


def create_collection_if_not_exists(
    collection_name: str,
    size: int = 1536,
):
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=size,
                distance=models.Distance.COSINE,
            ),
        )


def get_points(path_to_json: str) -> list[Point]:
    with open(path_to_json, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    points = []
    for item in dataset:
        payload = item.get("payload", {})
        points.append(
            Point(
                id=item.get("id"),
                title=item.get("title") or payload.get("title"),
                text=item.get("text") or payload.get("text"),
                keywords=item.get("keywords") or payload.get("keywords"),
            )
        )
    return points


def add_points(
    points: list[Point],
    collection_name: str,
):
    create_collection_if_not_exists(collection_name=collection_name)
    client.upsert(
        collection_name=collection_name,
        points=[point.to_qdrant_point_struct() for point in points],
    )
    print(f"Succesfully added {len(points)} points")

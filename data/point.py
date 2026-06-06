import hashlib
from qdrant_client.http import models

from sentence_transformers import SentenceTransformer

import configs

model = SentenceTransformer(configs.ENCODER)


def _text_to_int_id(text: str, max_bits: int = 64) -> int:
    hash_bytes = hashlib.sha256(text.encode()).digest()[: max_bits // 8]
    return int.from_bytes(hash_bytes, byteorder="big", signed=False)


class Point:
    def __init__(
        self,
        title: str | None,
        text: str | None,
        id: int | None = None,
        **kwargs,
    ) -> None:
        if title is None or text is None:
            raise ValueError("title and text cannot be None")

        self.title = title
        self.text = text
        self.id = id if id else _text_to_int_id(self.title)
        self.payload = {
            "title": self.title,
            "text": self.text,
        } | kwargs

    def __str__(self) -> str:
        return f"Point(id={self.id}, payload={self.payload})"

    def to_qdrant_point_struct(self) -> models.PointStruct:
        return models.PointStruct(
            id=self.id,
            vector=model.encode(
                self.title,
                normalize_embeddings=True,
            ).tolist(),
            payload=self.payload,
        )

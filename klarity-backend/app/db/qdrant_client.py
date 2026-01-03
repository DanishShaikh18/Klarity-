# app/db/qdrant_client.py

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Optional
import uuid

# Local embedded Qdrant (no Docker needed), stored in ./qdrant_data folder
_client = QdrantClient(path="qdrant_data")


def get_qdrant_client() -> QdrantClient:
    return _client


def upsert_embeddings(
    collection_name: str,
    vectors: List[List[float]],
    payloads: List[Dict],
):
    """
    vectors: list of embedding vectors (all same length)
    payloads: same length, each is a dict with metadata, e.g. {"text": "...", "doc_id": "..."}
    """
    if not vectors:
        # nothing to insert
        return

    client = get_qdrant_client()

    # auto-detect embedding dimension from the first vector
    embedding_dim = len(vectors[0])

    # 💥 DEV MODE: always recreate the collection so size always matches embeddings
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=embedding_dim,
            distance=Distance.COSINE,
        ),
    )

    points = []
    for vec, payload in zip(vectors, payloads):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload=payload,
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points,
    )


def search_embeddings(
    collection_name: str,
    query_vector: List[float],
    top_k: int = 5,
    query_filter: Optional[Dict] = None,
) -> List[Dict]:
    """
    Search similar embeddings in Qdrant.

    Returns a list of dicts:
    [
      {"id": ..., "score": ..., "payload": {...}},
      ...
    ]
    """
    client = get_qdrant_client()

    # Newer qdrant-client uses query_points instead of search()
    # We ignore query_filter for now (no filtering yet).
    result = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        # If later we use filters, we can map query_filter -> models.Filter
        # query_filter=...
    )

    points = result.points  # list of ScoredPoint

    return [
        {
            "id": p.id,
            "score": p.score,
            "payload": p.payload,
        }
        for p in points
    ]


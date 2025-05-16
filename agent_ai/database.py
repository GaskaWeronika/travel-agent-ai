from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_core.embeddings import Embeddings


def get_vector_store(embeddings: Embeddings, qdrant_url: str, qdrant_api_key: str) -> QdrantVectorStore:
    qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    vector_store = QdrantVectorStore(
        collection_name="travel_agent",
        client=qdrant_client,
        embedding=embeddings
    )
    return vector_store

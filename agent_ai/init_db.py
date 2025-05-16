from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from agent_ai.environment import Environment

def main():
    env = Environment()

    client = QdrantClient(
        url=env.qdrant_url,
        api_key=env.qdrant_api_key
    )

    client.recreate_collection(
        collection_name="travel_agent",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )

    print("The 'travel_agent' collection has been created or reset.")

if __name__ == "__main__":
    main()

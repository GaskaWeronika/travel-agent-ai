import os
from dotenv import find_dotenv, load_dotenv
from pydantic.v1 import SecretStr


class Environment:
    def __init__(self) -> None:
        load_dotenv(find_dotenv())
        self.qdrant_url: str = str(os.getenv("QDRANT_URL"))
        self.qdrant_api_key: str = str(os.getenv("QDRANT_API_KEY"))
        self.openai_api_key: SecretStr = SecretStr(str(os.getenv("OPENAI_API_KEY")))
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

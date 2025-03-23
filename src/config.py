import os
from dotenv import load_dotenv

load_dotenv()

# API Key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Qdrant
IS_CLOUD = os.getenv("IS_CLOUD", "false").lower() == "true"
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "wind_data")
QDRANT_HOST = os.getenv("QDRANT_HOST")

# Retool
RETOOL_PG_URL = os.getenv("RETOOL_PG_URL")

VECTOR_SIZE = 1024  # embed-english-v3.0
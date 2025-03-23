import os
import cohere
import pandas as pd
from src.config import COHERE_API_KEY, VECTOR_SIZE, IS_CLOUD, QDRANT_HOST, QDRANT_API_KEY, QDRANT_PORT, COLLECTION_NAME
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Init Cohere
co = cohere.Client(COHERE_API_KEY)

def embed_texts(texts):
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["float"]
    )

    # Unwrap embeddings safely
    if hasattr(response.embeddings, "float_"):
        return response.embeddings.float_

    return response.embeddings



def generate_daily_summaries(df):
    summaries = []
    grouped = df.groupby(["station_name", "date"])
    for (station, date), group in grouped:
        day_df = group.copy()
        avg_wind = day_df["value"].mean()
        max_wind = day_df["value"].max()
        summary = (
            f"On {date}, the average wind speed at {station} was {avg_wind:.2f} km/h, "
            f"with a maximum of {max_wind:.2f} km/h."
        )
        summaries.append(summary)
    return summaries

def get_qdrant_client():
    print("🌐 IS_CLOUD:", IS_CLOUD)
    if IS_CLOUD:
        print("🌍 Connecting to cloud Qdrant:", QDRANT_HOST)
        return QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)
    else:
        print("🏠 Connecting to local Qdrant: localhost", QDRANT_PORT)
        return QdrantClient(host="localhost", port=QDRANT_PORT)

def ensure_collection_exists(qdrant):
    if not qdrant.collection_exists(collection_name=COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )
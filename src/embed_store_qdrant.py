import pandas as pd
import uuid
from sqlalchemy import create_engine
from qdrant_client.models import PointStruct
from src.config import RETOOL_PG_URL, COLLECTION_NAME
from src.embedding.embedding_utils import (
    embed_texts,
    generate_daily_summaries,
    get_qdrant_client,
    ensure_collection_exists
)

engine = create_engine(RETOOL_PG_URL)
qdrant = get_qdrant_client()

def load_and_store_texts():
    df = pd.read_sql("SELECT * FROM wind_data_raw", engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["month"] = df["timestamp"].dt.strftime("%B")

    summaries = generate_daily_summaries(df)
    embeddings = embed_texts(summaries)
    
    print("📝 Number of summaries:", len(summaries))
    print("📐 Embedding shape:", len(embeddings), "x", len(embeddings[0]) if embeddings else 0)
    print("🔍 Sample summary:", summaries[0])
    print("🔍 Sample embedding:", embeddings[0][:5])

    ensure_collection_exists(qdrant)

    points = [
        PointStruct(id=uuid.uuid4().hex, vector=vec, payload={"text": text})
        for vec, text in zip(embeddings, summaries)
    ]

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Stored {len(points)} daily summaries in Qdrant.")
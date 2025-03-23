from sqlalchemy import create_engine
from src.config import RETOOL_PG_URL, COLLECTION_NAME
from qdrant_client.models import PointStruct
from src.embedding.embedding_utils import generate_daily_summaries, embed_texts, get_qdrant_client
import pandas as pd
import uuid

engine = create_engine(RETOOL_PG_URL)
qdrant = get_qdrant_client()

def load_and_store_texts():
    df = pd.read_sql("SELECT * FROM wind_data_raw", engine)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["month"] = df["timestamp"].dt.strftime("%B")

    summaries = generate_daily_summaries(df)

    embeddings = embed_texts(summaries)
    points = [
        PointStruct(id=uuid.uuid4().hex, vector=vec, payload={"text": text})
        for vec, text in zip(embeddings, summaries)
    ]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Stored {len(points)} daily summaries in Qdrant.")

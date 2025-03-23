import pandas as pd
from sqlalchemy import create_engine, text
from src.config import RETOOL_PG_URL
from src.data_ingest import fetch_wind_data
from src.embedding.embed_pipeline import load_and_store_texts

engine = create_engine(RETOOL_PG_URL)

def date_range_cached(start_date, end_date):
    """
    Check if any data for the date range exists in wind_data_raw.
    """
    query = text("""
        SELECT COUNT(*) FROM wind_data_raw
        WHERE timestamp::date BETWEEN :start AND :end
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"start": start_date, "end": end_date})
        count = result.scalar()

    return count > 0

def fetch_if_missing(start_date, end_date):
    """
    Fetches wind data from the API if it's not already in the database.
    Also triggers embedding after fetch.
    """
    if not date_range_cached(start_date, end_date):
        print(f"📡 Fetching wind data for {start_date} → {end_date}")
        fetch_wind_data(str(start_date), str(end_date))
        print("⚙️ Embedding newly fetched data into Qdrant...")
        load_and_store_texts()
    else:
        print(f"✅ Wind data already cached for {start_date} → {end_date}")
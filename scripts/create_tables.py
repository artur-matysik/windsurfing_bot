from sqlalchemy import create_engine, Table, Column, MetaData, Float, String, DateTime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Integer
import os
from dotenv import load_dotenv
load_dotenv()

# Replace with your connection string
DB_URL = os.getenv("RETOOL_PG_URL")  # or paste it directly if not using .env
engine = create_engine(DB_URL)

metadata = MetaData()

wind_data_raw = Table(
    "wind_data_raw", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),  # 👈 Add this line
    Column("timestamp", DateTime),
    Column("station_id", String),
    Column("station_name", String),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("value", Float),
)

station_metadata = Table(
    "station_metadata", metadata,
    Column("station_id", String, primary_key=True),
    Column("station_name", String),
    Column("latitude", Float),
    Column("longitude", Float),
)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("✅ Tables created successfully.")

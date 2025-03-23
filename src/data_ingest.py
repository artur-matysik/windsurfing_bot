import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import os
from src.config import RETOOL_PG_URL

engine = create_engine(RETOOL_PG_URL)

def fetch_wind_data(start_date, end_date):
    """
    Fetch wind data from data.gov.sg and insert into PostgreSQL (wind_data_raw + station_metadata).
    """
    base_url = "https://api.data.gov.sg/v1/environment/wind-speed"
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    all_records = []
    station_meta = {}

    for date in date_range:
        date_str = date.strftime("%Y-%m-%d")
        print(f"📅 Fetching: {date_str}")
        res = requests.get(base_url, params={"date": date_str})
        if res.status_code != 200:
            print(f"❌ Failed on {date_str}")
            continue

        data = res.json()

        # Extract station metadata
        for station in data.get("metadata", {}).get("stations", []):
            station_meta[station["id"]] = {
                "station_id": station["id"],
                "station_name": station["name"],
                "latitude": station["location"]["latitude"],
                "longitude": station["location"]["longitude"],
            }

        # Extract readings
        for item in data.get("items", []):
            timestamp = item["timestamp"]
            for reading in item.get("readings", []):
                s_id = reading["station_id"]
                record = {
                    "timestamp": timestamp,
                    "station_id": s_id,
                    "value": reading["value"]
                }
                meta = station_meta.get(s_id, {})
                record.update(meta)
                all_records.append(record)

    if not all_records:
        print("⚠️ No records found.")
        return

    df = pd.DataFrame(all_records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Insert wind data
    df.to_sql("wind_data_raw", engine, if_exists="append", index=False)
    print(f"✅ Inserted {len(df)} wind records.")

    # Insert station metadata
    meta_df = pd.DataFrame(station_meta.values()).drop_duplicates(subset=["station_id"])
    with engine.begin() as conn:
        for _, row in meta_df.iterrows():
            stmt = text("""
                INSERT INTO station_metadata (station_id, station_name, latitude, longitude)
                VALUES (:station_id, :station_name, :latitude, :longitude)
                ON CONFLICT (station_id) DO NOTHING;
            """)
            conn.execute(stmt, row.to_dict())

    print(f"✅ Inserted {len(meta_df)} station metadata rows (if new).")

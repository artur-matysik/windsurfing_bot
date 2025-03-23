import pandas as pd
from sqlalchemy import create_engine
from src.config import RETOOL_PG_URL
import os
import re
from src.utils.llm_matcher import match_station_name
from src.utils.date_parser import extract_dates_from_query

engine = create_engine(RETOOL_PG_URL)

def get_known_stations():
    """
    Load unique station names from the station_metadata table in PostgreSQL.
    """
    query = "SELECT DISTINCT station_name FROM station_metadata"
    df = pd.read_sql(query, engine)
    return df["station_name"].dropna().unique().tolist()

def get_months():
    return [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

def parse_query_filters(query: str, test_mode: bool = False):
    """
    Extracts station name, month, and specific date (if any) from the query.
    """
    months = get_months()
    month_match = next((m for m in months if m.lower() in query.lower()), None)

    station_match = None
    if any(kw in query.lower() for kw in ["changi", "tuas", "sentosa", "east", "west", "woodlands"]):
        station_match = match_station_name(query, test_mode=test_mode)

    start_date, end_date = extract_dates_from_query(query)
    date = start_date if start_date == end_date else None

    return {
        "station_name": station_match,
        "month": month_match,
        "date": date
    }

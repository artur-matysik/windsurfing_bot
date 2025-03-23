import cohere
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.config import RETOOL_PG_URL

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))
engine = create_engine(RETOOL_PG_URL)

def get_station_candidates():
    """
    Load station names directly from PostgreSQL.
    """
    df = pd.read_sql("SELECT DISTINCT station_name FROM station_metadata", engine)
    return df["station_name"].dropna().unique().tolist()

def match_station_name(user_query: str, test_mode=False):
    station_names = get_station_candidates()

    prompt = f"""You are a helpful assistant that selects the most likely weather station based on a user's query.

List of station names:
{', '.join(station_names)}

User query: \"{user_query}\"

From the list, return the **single most relevant station name**. Respond only with the station name.
"""

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=30,
        temperature=0.2,
    )

    match = response.generations[0].text.strip()
    return match if match in station_names else None

import re
from datetime import datetime
import dateparser
from dateparser.search import search_dates

def extract_dates_from_query(query: str):
    """
    Detects a specific date or month range in a query.
    Returns (start_date, end_date) as date objects or (None, None).
    """

    results = search_dates(query, settings={"PREFER_DATES_FROM": "past"})

    if results:
        parsed_date = results[0][1]
        if parsed_date.day != 1 or re.search(r"\d{1,2}", query):
            # It's a specific date (not just a month)
            return parsed_date.date(), parsed_date.date()

    # Fallback: look for full month by name
    match = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)(\s+\d{4})?",
        query,
        re.IGNORECASE,
    )
    if match:
        month = match.group(1)
        year = match.group(2) or str(datetime.today().year)
        month_num = datetime.strptime(month, "%B").month
        start = datetime(int(year), month_num, 1).date()
        if month_num == 12:
            end = datetime(int(year) + 1, 1, 1).date()
        else:
            end = datetime(int(year), month_num + 1, 1).date()
        return start, end

    return None, None

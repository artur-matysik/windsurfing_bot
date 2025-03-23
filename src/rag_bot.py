from calendar import monthrange
from src.utils.filter_extraction import parse_query_filters
from src.utils.date_parser import extract_dates_from_query
from src.utils.dynamic_fetch import fetch_if_missing
from src.retriever_qdrant import retrieve_top_k
from src.rag_chain import generate_answer
from datetime import date

def answer_question(query: str, k: int = 3, test_mode: bool = False, log=None):
    def log_msg(msg):
        if log:
            log(msg)
        else:
            print(msg)

    log_msg(f"🔍 Question: {query}")
    filters = parse_query_filters(query, test_mode=test_mode)
    log_msg(f"📌 Parsed filters: {filters}")

    # Default: no specific dates
    start_date = end_date = None

    # Priority: use date if clearly stated
    parsed_start, parsed_end = extract_dates_from_query(query)
    if parsed_start and parsed_end:
        start_date, end_date = parsed_start, parsed_end
        log_msg(f"🗓️ Date range detected: {start_date} → {end_date}")
        fetch_if_missing(start_date, end_date)
    elif filters["month"] and filters["station_name"]:
        # Fallback: infer full month date range
        month_name = filters["month"]
        month_num = date(1900, 1, 1).strftime("%B").index(month_name) + 1 if month_name else None
        import re

        # Try to extract a 4-digit year from the query
        year_match = re.search(r"(20\\d{2})", query)
        year = int(year_match.group(1)) if year_match else date.today().year

        start_date = date(year, month_num, 1)
        end_day = monthrange(year, month_num)[1]
        end_date = date(year, month_num, end_day)
        log_msg(f"📆 Inferred month range for {month_name}: {start_date} → {end_date}")
        fetch_if_missing(start_date, end_date)

    results = retrieve_top_k(query, k=k, **filters)
    log_msg(f"📄 Retrieved {len(results)} summaries")

    answer = generate_answer(results, query)
    log_msg("🧠 Generated final answer")

    return answer

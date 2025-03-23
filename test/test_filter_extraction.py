import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils.filter_extraction import parse_query_filters

def test_parse_station_only():
    query = "Tell me about wind conditions at Changi"
    filters = parse_query_filters(query, test_mode=True)
    assert "Changi" in filters["station_name"], f"Expected station containing 'Changi', got {filters['station_name']}"

    assert filters["month"] is None
    print("✅ test_parse_station_only passed")

def test_parse_month_only():
    query = "Where is the best wind in November?"
    filters = parse_query_filters(query, test_mode=True)
    assert filters["month"] == "November", f"Expected 'November', got {filters['month']}"
    assert filters["station_name"] is None
    print("✅ test_parse_month_only passed")

def test_parse_station_and_month():
    query = "How was Tuas South in March?"
    filters = parse_query_filters(query, test_mode=True)
    assert "Tuas" in filters["station_name"], f"Expected station containing 'Tuas', got {filters['station_name']}"

    assert filters["month"] == "March", f"Expected 'March', got {filters['month']}"
    print("✅ test_parse_station_and_month passed")

if __name__ == "__main__":
    test_parse_station_only()
    test_parse_month_only()
    test_parse_station_and_month()

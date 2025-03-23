import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.retriever_qdrant import retrieve_top_k

def test_filtered_retrieve():
    query = "Where is the best wind in March?"
    results = retrieve_top_k(query, station_name="Changi East", month="March")

    assert isinstance(results, list), "Result should be a list"
    assert len(results) > 0, "No results found with filter"

    print("✅ Filtered results:")
    for r in results:
        print("-", r)

if __name__ == "__main__":
    test_filtered_retrieve()

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.retriever_qdrant import retrieve_top_k

def test_retrieve():
    query = "When is the best time for windsurfing in Singapore?"
    results = retrieve_top_k(query)

    assert isinstance(results, list), "Result should be a list"
    assert len(results) > 0, "No results retrieved from Qdrant"
    
    print("✅ Retrieved top results:")
    for r in results:
        print("-", r)

if __name__ == "__main__":
    test_retrieve()
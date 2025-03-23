import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.retriever_qdrant import retrieve_top_k
from src.rag_chain import generate_answer

def test_rag_chain():
    query = "What month is best for windsurfing in Singapore?"
    context = retrieve_top_k(query)

    assert isinstance(context, list) and context, "No context retrieved"

    answer = generate_answer(context, query)

    print("🧠 Generated Answer:\n")
    print(answer)

if __name__ == "__main__":
    test_rag_chain()
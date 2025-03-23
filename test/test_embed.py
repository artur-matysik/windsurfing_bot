import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.embed_store_qdrant import load_and_store_texts


def test_embed_and_store():
    print("🚀 Running embedding test from PostgreSQL...")
    load_and_store_texts()
    print("✅ test_embed_and_store passed")

if __name__ == "__main__":
    test_embed_and_store()
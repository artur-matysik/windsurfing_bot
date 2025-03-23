import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag_bot import answer_question

if __name__ == "__main__":
    question = "How was the wind near Tuas on March 2, 2024?"
    answer = answer_question(question, test_mode=True)
    print("\n💬 Bot answer:\n", answer)

import cohere
from src.config import COHERE_API_KEY

co = cohere.Client(COHERE_API_KEY)

def generate_answer(context_list, user_query):
    """
    Generate a response based on retrieved context and a user query.
    """
    system_message = (
        "You are a wind and weather expert for Singapore. "
        "Always assume windsurfing activities happen during daytime hours (10am to 5pm) unless the user clearly specifies a time. "
        "Coastal stations (East Coast, Changi) are generally preferred for windsurfing. Assume these stations if not specified."
        "Use the provided wind summaries to answer naturally and helpfully. "
        "If multiple days are available, provide a general summary for the month unless the user requests a specific date."
    )

    prompt = f"""{system_message}

Context:
{chr(10).join(['- ' + c for c in context_list])}

User question:
{user_query}

Answer:"""

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
    )

    return response.generations[0].text.strip()

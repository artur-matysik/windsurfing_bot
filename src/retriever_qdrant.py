import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from src.config import COLLECTION_NAME, COHERE_API_KEY
from src.embedding.embedding_utils import embed_texts, get_qdrant_client

# Init Cohere
co = cohere.Client(COHERE_API_KEY)

# Qdrant client
qdrant = get_qdrant_client()

def retrieve_top_k(query, k=3, station_name=None, month=None, date=None):
    query_vector = embed_texts([query])[0]

    filters = []
    if station_name:
        filters.append(FieldCondition(key="text", match=MatchValue(value=station_name)))
    if month:
        filters.append(FieldCondition(key="text", match=MatchValue(value=month)))
    if date:
        filters.append(FieldCondition(key="text", match=MatchValue(value=str(date))))

    query_filter = Filter(must=filters) if filters else None

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k,
        query_filter=query_filter
    )

    return [hit.payload["text"] for hit in results]

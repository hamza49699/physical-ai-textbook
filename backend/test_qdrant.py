
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import time

load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

print(f"Testing Qdrant connection to: {QDRANT_URL}")

try:
    start = time.time()
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=5)
    collections = client.get_collections()
    print(f"Connection successful in {time.time()-start:.2f}s")
    print(f"Collections: {collections}")
except Exception as e:
    print(f"Connection failed: {e}")

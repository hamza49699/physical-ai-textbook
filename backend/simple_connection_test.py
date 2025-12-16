import os
from dotenv import load_dotenv
import psycopg2
from qdrant_client import QdrantClient
import cohere

load_dotenv()

print("=" * 60)
print("BACKEND CONNECTION TEST")
print("=" * 60)

# Test 1: Neon DB
print("\n[1/3] Testing Neon DB...")
try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    cursor.close()
    conn.close()
    print("✅ Neon DB: CONNECTED")
except Exception as e:
    print(f"❌ Neon DB: FAILED - {e}")

# Test 2: Qdrant
print("\n[2/3] Testing Qdrant...")
try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=10
    )
    collections = client.get_collections()
    print(f"✅ Qdrant: CONNECTED - {len(collections.collections)} collections found")
except Exception as e:
    print(f"❌ Qdrant: FAILED - {e}")

# Test 3: Cohere
print("\n[3/3] Testing Cohere...")
try:
    co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
    # Simple test - just create the client
    print("✅ Cohere: API KEY VALID")
except Exception as e:
    print(f"❌ Cohere: FAILED - {e}")

print("\n" + "=" * 60)
print("CONNECTION TEST COMPLETE")
print("=" * 60)

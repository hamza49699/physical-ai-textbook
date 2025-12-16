import os
import psycopg2
from qdrant_client import QdrantClient
import cohere
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def check_db():
    print("\n--- Checking PostgreSQL (Neon) ---")
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("FAIL: DATABASE_URL not set in .env")
        return False
    
    # Masking for log
    masked = db_url.split("@")[-1] if "@" in db_url else "..."
    print(f"Connecting to: ...@{masked}")

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        print("SUCCESS: Database connection established.")
        return True
    except Exception as e:
        print(f"FAIL: Database connection error: {e}")
        return False

def check_qdrant():
    print("\n--- Checking Qdrant ---")
    url = os.getenv("QDRANT_URL")
    key = os.getenv("QDRANT_API_KEY")
    
    if not url:
        print("FAIL: QDRANT_URL not set in .env")
        return False
        
    print(f"Target: {url}")
    
    try:
        client = QdrantClient(url=url, api_key=key)
        cols = client.get_collections()
        print("SUCCESS: Qdrant connection established. Collections fetched.")
        return True
    except Exception as e:
        print(f"FAIL: Qdrant connection error: {e}")
        return False

def check_cohere():
    print("\n--- Checking Cohere ---")
    key = os.getenv("COHERE_API_KEY")
    if not key or key == "your-cohere-api-key-here":
        print("SKIP: COHERE_API_KEY not set or default.")
        return True
        
    try:
        co = cohere.Client(api_key=key)
        # Use a simpler check that doesn't require model loading
        response = co.check_api_key()
        print("SUCCESS: Cohere API key valid.")
        return True
    except AttributeError:
        # If check_api_key doesn't exist, try a simple tokenize call
        try:
            co = cohere.Client(api_key=key)
            co.tokenize(text="test", model="command")
            print("SUCCESS: Cohere API key valid.")
            return True
        except Exception as e:
            print(f"FAIL: Cohere connection error: {e}")
            return False
    except Exception as e:
        print(f"FAIL: Cohere connection error: {e}")
        return False

if __name__ == "__main__":
    print(f"Python executable: {sys.executable}")
    success_db = check_db()
    success_qdrant = check_qdrant()
    success_cohere = check_cohere()
    
    if success_db and success_qdrant and success_cohere:
        print("\nOVERALL: ALL CHECKS PASSED")
    else:
        print("\nOVERALL: SOME CHECKS FAILED")

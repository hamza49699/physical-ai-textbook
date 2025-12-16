import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_db():
    print("--- Checking PostgreSQL (Neon) ---", flush=True)
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("FAIL: DATABASE_URL not set in .env", flush=True)
        return
    
    # Masking for log
    masked = db_url.split("@")[-1] if "@" in db_url else "..."
    print(f"Connecting to: ...@{masked}", flush=True)

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        res = cursor.fetchone()
        print(f"Query Result: {res}", flush=True)
        cursor.close()
        conn.close()
        print("SUCCESS: Database connection established.", flush=True)
    except Exception as e:
        print(f"FAIL: Database connection error: {e}", flush=True)

if __name__ == "__main__":
    check_db()

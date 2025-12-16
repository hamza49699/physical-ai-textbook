
import os
import psycopg2
from dotenv import load_dotenv
import sys

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Testing connection to: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'LOCAL'}")

try:
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")


import psycopg2

DATABASE_URL="postgresql://neondb_owner:npg_LB4wmJ8zuYGr@ep-patient-river-adabahlw-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

print("Connecting to DB...", flush=True)
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(cur.fetchone(), flush=True)
    cur.close()
    conn.close()
    print("SUCCESS: Connected to Neon DB", flush=True)
except Exception as e:
    print(f"FAILED: {e}", flush=True)

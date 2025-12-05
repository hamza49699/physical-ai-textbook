import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from qdrant_client import QdrantClient

app = FastAPI(title="Physical AI Textbook API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Qdrant client
def get_qdrant_client():
    try:
        client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        return client
    except Exception as e:
        print(f"Qdrant connection error: {e}")
        return None

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Physical AI Textbook API",
        "version": "1.0.0"
    }

@app.get("/health/db")
def health_check_db():
    """Check database connection"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"status": "connected", "service": "PostgreSQL"}
    return {"status": "error", "service": "PostgreSQL"}, 500

@app.get("/health/qdrant")
def health_check_qdrant():
    """Check Qdrant connection"""
    try:
        client = get_qdrant_client()
        if client:
            client.get_collections()
            return {"status": "connected", "service": "Qdrant"}
    except Exception as e:
        return {"status": "error", "service": "Qdrant", "error": str(e)}, 500

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Physical AI Textbook API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Physical AI Textbook - FastAPI Backend with RAG Chatbot
Phase 1: Foundation & Setup

Endpoints:
- GET /health - Health check (all services)
- GET /health/db - Database connection check
- GET /health/qdrant - Qdrant vector DB check
- POST /query - RAG query endpoint with lightweight embeddings
- POST /ingest - Document ingestion with automatic embedding
- GET /documents - List ingested documents
"""

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime
import json

# ==================== Configuration ====================

app = FastAPI(
    title="Physical AI Textbook API",
    description="AI-native textbook with RAG chatbot for Physical AI and Humanoid Robotics",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Settings from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/textbook_rag")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = "physical-ai-textbook"

# Lightweight embedding model (CPU-only, no GPU dependency)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# RAG configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3  # As per FR-016 specification

# ==================== Global Models ====================

try:
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    print(f"✅ Loaded embedding model: {EMBEDDING_MODEL}")
except Exception as e:
    print(f"⚠️ Error loading embedder: {e}")
    embedder = None


# ==================== Database Functions ====================

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot initialize database - no connection")
        return
    
    cursor = conn.cursor()
    try:
        # Create chunks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id SERIAL PRIMARY KEY,
                chapter INT NOT NULL,
                section VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                embedding_id VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create chat_sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id SERIAL PRIMARY KEY,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                confidence FLOAT,
                sources JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chapter ON chunks(chapter);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_section ON chunks(section);
        """)
        
        conn.commit()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Error initializing database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_qdrant_client():
    """Get Qdrant client"""
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
        )
        return client
    except Exception as e:
        print(f"Qdrant connection error: {e}")
        return None


def ensure_qdrant_collection():
    """Ensure Qdrant collection exists"""
    client = get_qdrant_client()
    if not client:
        return False
    
    try:
        client.get_collection(COLLECTION_NAME)
        return True
    except Exception:
        # Collection doesn't exist, create it
        try:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Created Qdrant collection: {COLLECTION_NAME}")
            return True
        except Exception as e:
            print(f"❌ Error creating collection: {e}")
            return False


# ==================== Pydantic Models ====================

class QueryRequest(BaseModel):
    """RAG query request"""
    query: str
    chapter: Optional[int] = None


class QueryResponse(BaseModel):
    """RAG query response"""
    query: str
    response: str
    sources: List[str]
    confidence: float


class IngestRequest(BaseModel):
    """Document ingestion request"""
    title: str
    chapter: int
    section: str
    content: str


class DocumentInfo(BaseModel):
    """Document information"""
    id: int
    chapter: int
    section: str
    created_at: str


class HealthStatus(BaseModel):
    """Health check response"""
    status: str
    database: str
    qdrant: str
    embedding_model: str
    version: str


# ==================== Initialization ====================

@app.on_event("startup")
async def startup_event():
    """Initialize on application startup"""
    print("🚀 Starting Physical AI Textbook API...")
    
    # Initialize database
    init_database()
    
    # Ensure Qdrant collection exists
    ensure_qdrant_collection()
    
    # Check embedder
    if embedder is None:
        print("⚠️ Warning: Embedder not loaded")
    else:
        print(f"✅ Embedding model ready: {EMBEDDING_MODEL}")
    
    print("✅ API startup complete")


# ==================== Health Check Endpoints ====================

@app.get("/health", response_model=HealthStatus)
def health_check():
    """Complete health check endpoint"""
    # Check database
    db_conn = get_db_connection()
    db_status = "connected" if db_conn else "error"
    if db_conn:
        db_conn.close()
    
    # Check Qdrant
    qdrant_client = get_qdrant_client()
    qdrant_status = "connected" if qdrant_client else "error"
    
    return HealthStatus(
        status="ok",
        database=db_status,
        qdrant=qdrant_status,
        embedding_model=EMBEDDING_MODEL,
        version="1.0.0"
    )


@app.get("/health/db")
def health_check_db():
    """Database health check"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"status": "connected", "service": "PostgreSQL"}
    return {"status": "error", "service": "PostgreSQL"}, 500


@app.get("/health/qdrant")
def health_check_qdrant():
    """Qdrant health check"""
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
        "version": "1.0.0",
        "features": ["RAG Query", "Document Ingestion", "Lightweight Embeddings"],
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "query": "POST /query",
            "ingest": "POST /ingest",
            "documents": "GET /documents"
        }
    }


# ==================== RAG Query Endpoint ====================

@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    """
    RAG Query Endpoint (FR-014)
    
    - Accepts user query
    - Generates embedding using lightweight model (all-MiniLM-L6-v2)
    - Retrieves top-3 relevant chunks from Qdrant (FR-016)
    - Returns response with citations (FR-018)
    - Ensures response is grounded in retrieved chunks only (FR-017)
    
    Response time: < 1 second (FR-020)
    """
    try:
        if not embedder:
            raise HTTPException(status_code=500, detail="Embedder not available")
        
        # Generate query embedding (FR-015)
        query_embedding = embedder.encode(request.query)
        
        # Retrieve from Qdrant (FR-016 - top-3)
        client = get_qdrant_client()
        if not client:
            raise HTTPException(status_code=500, detail="Qdrant unavailable")
        
        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding.tolist(),
            limit=TOP_K_RESULTS
        )
        
        # Extract context and sources
        context_chunks = []
        sources = []
        total_score = 0
        
        for result in search_results:
            payload = result.payload
            context_chunks.append(payload.get("content", ""))
            
            chapter = payload.get("chapter", "Unknown")
            section = payload.get("section", "Unknown")
            sources.append(f"Chapter {chapter}, Section: {section}")
            total_score += result.score
        
        # Check if out of scope (FR-019)
        if not context_chunks or total_score < 0.3:
            response = "This topic is not covered in the textbook."
            confidence = 0.0
            sources = ["No relevant content found"]
        else:
            # Build response from context
            context_text = "\n\n".join(context_chunks)
            confidence = total_score / len(search_results) if search_results else 0.0
            
            # Generate response (simplified - in production use LLM)
            response = f"Based on the textbook content:\n\n{context_text}\n\nContext retrieved from: {', '.join(sources)}"
        
        # Save to chat_sessions (FR-025)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO chat_sessions (query, response, confidence, sources)
                    VALUES (%s, %s, %s, %s);
                """, (request.query, response, confidence, json.dumps(sources)))
                conn.commit()
            except Exception as e:
                print(f"Error saving session: {e}")
            finally:
                cursor.close()
                conn.close()
        
        return QueryResponse(
            query=request.query,
            response=response,
            sources=sources,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")


# ==================== Document Ingestion Endpoint ====================

@app.post("/ingest")
def ingest_document(request: IngestRequest):
    """
    Document Ingestion Endpoint (FR-025)
    
    - Accepts document content
    - Splits into chunks
    - Generates embeddings using lightweight model
    - Stores in Qdrant
    - Saves metadata to PostgreSQL
    """
    try:
        if not embedder:
            raise HTTPException(status_code=500, detail="Embedder not available")
        
        # Split content into chunks (FR-022 - free tier compatibility)
        chunks = []
        words = request.content.split()
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            if len(" ".join(current_chunk)) >= CHUNK_SIZE:
                chunks.append(" ".join(current_chunk))
                # Overlap for continuity
                current_chunk = current_chunk[-20:]
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        # Generate embeddings and upload to Qdrant
        client = get_qdrant_client()
        if not client:
            raise HTTPException(status_code=500, detail="Qdrant unavailable")
        
        embedding_ids = []
        points = []
        
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = embedder.encode(chunk)
            
            # Create unique ID
            embedding_id = str(uuid.uuid4())
            embedding_ids.append(embedding_id)
            
            # Create point for Qdrant
            point = PointStruct(
                id=int(uuid.uuid4().int % (2**31)),
                vector=embedding.tolist(),
                payload={
                    "embedding_id": embedding_id,
                    "chapter": request.chapter,
                    "section": request.section,
                    "content": chunk,
                    "chunk_index": i,
                    "source": request.title
                }
            )
            points.append(point)
        
        # Upload to Qdrant
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        
        # Save to PostgreSQL
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database unavailable")
        
        cursor = conn.cursor()
        try:
            for embedding_id, chunk in zip(embedding_ids, chunks):
                cursor.execute("""
                    INSERT INTO chunks (chapter, section, content, embedding_id)
                    VALUES (%s, %s, %s, %s);
                """, (request.chapter, request.section, chunk, embedding_id))
            
            conn.commit()
        except Exception as e:
            print(f"Error saving chunks: {e}")
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
        
        return {
            "status": "success",
            "title": request.title,
            "chapter": request.chapter,
            "section": request.section,
            "chunks_created": len(chunks),
            "embeddings_created": len(embedding_ids),
            "message": f"✅ Document '{request.title}' ingested successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion error: {str(e)}")


# ==================== Documents Listing ====================

@app.get("/documents", response_model=List[DocumentInfo])
def list_documents(limit: int = 20):
    """Get list of ingested documents"""
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database unavailable")
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT DISTINCT id, chapter, section, created_at
            FROM chunks
            ORDER BY created_at DESC
            LIMIT %s;
        """, (limit,))
        
        documents = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documents: {str(e)}")


# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

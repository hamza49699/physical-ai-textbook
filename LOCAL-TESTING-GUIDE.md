# 🧪 Local Testing Guide - Physical AI Textbook

**Date:** December 7, 2025  
**Status:** Ready for local testing  

---

## ✅ Prerequisites

Before testing locally, ensure you have:

### 1. Python 3.9+ installed
```bash
python --version
# Should show Python 3.9.x or higher
```

### 2. Git (already have)
```bash
git --version
# Should show git version
```

### 3. PostgreSQL (optional for local testing)
For full local testing, you can use:
- **Neon free tier** (recommended) - https://neon.tech
- **Local PostgreSQL** - https://www.postgresql.org/download/windows/
- **Docker** - `docker run -e POSTGRES_PASSWORD=password -p 5432:5432 postgres`

### 4. Qdrant (optional for local testing)
```bash
# Option 1: Docker (recommended)
docker run -p 6333:6333 qdrant/qdrant

# Option 2: Cloud - https://cloud.qdrant.io (free tier)
```

---

## 🚀 Local Setup Steps

### Step 1: Navigate to Project
```bash
cd c:\Users\digital\claude_first\physical-ai-textbook
```

### Step 2: Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or for CMD:
.\venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
```bash
# Install Python backend dependencies
pip install -r backend/requirements.txt

# Install Node.js frontend dependencies (for Docusaurus)
npm install
```

### Step 4: Set Up Environment Variables

Create `.env.local` file in project root:
```bash
# Backend Configuration
DATABASE_URL=postgresql://localhost/textbook_rag
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
OPENAI_API_KEY=sk-your-key-here (optional for local testing)

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
NODE_ENV=development
```

### Step 5: Test Backend Locally

#### Option A: Without External Services (Mock Mode)

```bash
# Start backend (uses local defaults)
cd backend
python main.py

# Should show:
# ✅ Loaded embedding model: all-MiniLM-L6-v2
# ✅ Database initialized successfully
# ✅ Created Qdrant collection: physical-ai-textbook
# ✅ API startup complete
# Uvicorn running on http://127.0.0.1:8000
```

#### Option B: With Docker Qdrant + PostgreSQL

```bash
# Terminal 1: Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2: Start PostgreSQL
docker run -e POSTGRES_PASSWORD=password -p 5432:5432 postgres

# Terminal 3: Start backend
cd backend
python main.py
```

### Step 6: Test API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "ok",
#   "database": "connected",
#   "qdrant": "connected",
#   "embedding_model": "all-MiniLM-L6-v2",
#   "version": "1.0.0"
# }
```

#### API Documentation
```bash
# Open in browser:
http://localhost:8000/docs

# You'll see Swagger UI with all endpoints
```

#### Ingest a Document
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Chapter",
    "chapter": 1,
    "section": "Introduction",
    "content": "Physical AI combines robotics, artificial intelligence, and digital twins to create systems that can understand and interact with the physical world. This is a comprehensive guide to understanding physical AI concepts and their practical applications."
  }'

# Expected response:
# {
#   "status": "success",
#   "chunks_created": 1,
#   "embeddings_created": 1,
#   "message": "✅ Document 'Test Chapter' ingested successfully"
# }
```

#### Query the Chatbot
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Physical AI?"
  }'

# Expected response:
# {
#   "query": "What is Physical AI?",
#   "response": "Based on the textbook content:\n\nPhysical AI combines robotics, artificial intelligence, and digital twins to create systems that can understand and interact with the physical world. This is a comprehensive guide to understanding physical AI concepts and their practical applications.\n\nContext retrieved from: Chapter 1, Section: Introduction",
#   "sources": [
#     "Chapter 1, Section: Introduction"
#   ],
#   "confidence": 0.95
# }
```

#### List Documents
```bash
curl http://localhost:8000/documents

# Expected response:
# [
#   {
#     "id": 1,
#     "chapter": 1,
#     "section": "Introduction",
#     "created_at": "2025-12-07T10:30:00"
#   }
# ]
```

### Step 7: Test Frontend Locally

#### Build Docusaurus
```bash
npm run build

# Should show:
# ✅ Build success!
# ✅ Build time: XX seconds
# ✅ Output: ./build/
```

#### Start Docusaurus Dev Server
```bash
npm start

# Should show:
# [INFO] Docusaurus server started on http://localhost:3000
# 
# Open in browser: http://localhost:3000
```

#### Verify Frontend
- [ ] Homepage loads
- [ ] Sidebar shows all chapters
- [ ] Dark/light mode toggle works
- [ ] Search functionality works
- [ ] No console errors (F12)

---

## 🧪 Testing Checklist

### Backend Tests

**Health Checks:**
- [ ] `GET /health` returns 200 OK
- [ ] `GET /health/db` shows database status
- [ ] `GET /health/qdrant` shows vector DB status
- [ ] All services connected

**Document Ingestion:**
- [ ] `POST /ingest` accepts document
- [ ] Returns chunks_created > 0
- [ ] Returns embeddings_created > 0
- [ ] Data saved to PostgreSQL
- [ ] Embeddings stored in Qdrant

**Query Endpoint:**
- [ ] `POST /query` accepts queries
- [ ] Returns response with sources
- [ ] Confidence score >= 0
- [ ] Response time < 1 second
- [ ] Citations included

**Documentation:**
- [ ] `GET /docs` loads Swagger UI
- [ ] All endpoints documented
- [ ] Request/response schemas visible

### Frontend Tests

**Build:**
- [ ] `npm run build` succeeds
- [ ] Build time < 30 seconds
- [ ] No errors or warnings
- [ ] Output in `./build/` directory

**Dev Server:**
- [ ] `npm start` runs without errors
- [ ] Homepage loads at localhost:3000
- [ ] Sidebar navigation works
- [ ] All chapters visible
- [ ] Dark mode toggle functional
- [ ] No console errors

**Navigation:**
- [ ] Home page → Chapter 1 works
- [ ] Chapter navigation links work
- [ ] Search bar functional
- [ ] Blog section accessible
- [ ] Links not broken

---

## 📝 Sample Test Session

```bash
# 1. Start backend
cd backend
python main.py
# Keep this running in Terminal 1

# 2. In Terminal 2: Ingest sample content
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Chapter 1: Introduction to Physical AI",
    "chapter": 1,
    "section": "Fundamentals",
    "content": "Physical AI is a subfield of artificial intelligence that focuses on understanding and interacting with the physical world. It combines robotics, vision systems, and machine learning to enable machines to perceive, reason, and act in real environments. Key components include sensors for perception, actuators for action, and AI algorithms for decision-making."
  }'

# 3. Query the chatbot
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?"}'

# 4. List documents
curl http://localhost:8000/documents

# 5. View API docs
# Open http://localhost:8000/docs in browser
```

---

## 🔧 Troubleshooting

### Issue: "Module not found: sentence_transformers"
**Solution:**
```bash
pip install sentence-transformers
```

### Issue: "Connection refused" for PostgreSQL
**Solution:**
```bash
# Use cloud (Neon) or Docker:
docker run -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
```

### Issue: "Connection refused" for Qdrant
**Solution:**
```bash
# Start Qdrant with Docker:
docker run -p 6333:6333 qdrant/qdrant
```

### Issue: "embedding model download error"
**Solution:**
```bash
# First run downloads the model (~100MB)
# Internet connection required
# Model cached after first download
```

### Issue: "npm: command not found"
**Solution:**
```bash
# Install Node.js from https://nodejs.org/
# Then reinstall:
npm install
```

---

## 📊 Expected Performance

### Backend
- **Startup time:** 5-10 seconds (first run downloads embedding model)
- **Query latency:** 200-500ms (CPU-only)
- **Ingest latency:** 1-2 seconds (depends on content size)

### Frontend
- **Build time:** 10-30 seconds
- **Dev server startup:** 3-5 seconds
- **Page load:** < 2 seconds

---

## ✅ Ready for Local Testing!

You're all set! Follow the steps above to test locally.

**Next Steps After Local Testing:**
1. Verify all endpoints work
2. Test both backend and frontend
3. Fix any issues
4. Push to GitHub
5. Deploy to Railway/Neon

---

**Questions?** Check troubleshooting section or check logs carefully!

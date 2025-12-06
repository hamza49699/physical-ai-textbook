# Deployment Guide - Physical AI Textbook Backend

## Architecture
- **Frontend**: GitHub Pages (Docusaurus)
- **Backend**: Render.com (FastAPI)
- **Database**: Neon.tech (PostgreSQL)
- **Vector DB**: Qdrant Cloud (Free tier)

---

## Step 1: Setup Neon PostgreSQL

1. Go to https://neon.tech (free tier available)
2. Create new project
3. Get connection string: `postgresql://user:password@ep-xxxxx.us-east-1.neon.tech/textbook_rag`
4. Create tables:

```sql
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter INT,
    section VARCHAR(255),
    content TEXT,
    embedding_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query TEXT,
    response TEXT,
    confidence FLOAT,
    sources JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chapter ON chunks(chapter);
CREATE INDEX idx_created ON chat_sessions(created_at);
```

---

## Step 2: Setup Qdrant Cloud

1. Go to https://cloud.qdrant.io (free tier: 2,000 vectors)
2. Create new cluster
3. Get URL and API key
4. Note: Collection will be created automatically on first ingestion

---

## Step 3: Deploy Backend to Render

1. Go to https://render.com
2. Connect GitHub (hamza49699/physical-ai-textbook)
3. Create new Web Service:
   - **Name**: physical-ai-backend
   - **Root Directory**: `physical-ai-textbook/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     ```
     DATABASE_URL=postgresql://...  (from Neon)
     QDRANT_URL=https://...         (from Qdrant Cloud)
     QDRANT_API_KEY=...             (from Qdrant Cloud)
     FRONTEND_URL=https://hamza699.github.io/physical-ai-textbook
     PORT=8000
     ```
4. Deploy (takes ~2-3 min)
5. Get URL: `https://physical-ai-backend.onrender.com`

---

## Step 4: Update Frontend Chatbot

Update `src/components/Chatbot.tsx` line ~47:

```typescript
// Replace localhost with production URL
const response = await fetch('https://physical-ai-backend.onrender.com/query', {
```

Rebuild and push to trigger GitHub Pages deploy.

---

## Step 5: Ingest Documents

**Endpoint**: `POST https://physical-ai-backend.onrender.com/ingest`

**Example**:
```bash
curl -X POST "https://physical-ai-backend.onrender.com/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ROS 2 Fundamentals",
    "chapter": 1,
    "section": "What is ROS 2?",
    "content": "ROS 2 (Robot Operating System 2) is a middleware that..."
  }'
```

**Or use Python**:
```python
import requests

url = "https://physical-ai-backend.onrender.com/ingest"
docs = [
    {
        "title": "ROS 2 Basics",
        "chapter": 1,
        "section": "Introduction",
        "content": "Your textbook content here..."
    },
    # Add more documents
]

for doc in docs:
    requests.post(url, json=doc)
```

---

## Step 6: Test Chatbot

1. Go to https://hamza699.github.io/physical-ai-textbook
2. Click chatbot button (bottom-right 💬)
3. Ask a question about ingested content
4. Should see response with sources and confidence score

---

## Health Checks

- Backend health: `GET https://physical-ai-backend.onrender.com/health`
- API docs: `GET https://physical-ai-backend.onrender.com/docs`

---

## Troubleshooting

**"Could not reach chatbot service"**
- Verify Render backend is running: https://physical-ai-backend.onrender.com/health
- Check FRONTEND_URL is set correctly in Render env vars
- Check browser console for CORS errors

**"No documents found"**
- Use `/ingest` endpoint to add documents
- Verify documents in database: `SELECT COUNT(*) FROM chunks`

**"Qdrant connection failed"**
- Verify QDRANT_URL and QDRANT_API_KEY in Render env vars
- Check Qdrant Cloud cluster is active

---

## Free Tier Limits

- **Neon**: 5 GB storage, 1 shared CPU (generous free tier)
- **Qdrant Cloud**: 2,000 vectors (enough for ~20-30 documents)
- **Render**: 750 hours/month (free tier)
- Upgrade as needed

---

## Cost Estimate (All Free Tier)
- Total: **$0/month** during launch phase

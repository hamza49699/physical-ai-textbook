# 🚀 EXECUTION PLAN - Complete Infrastructure Setup
**Date:** December 7, 2025  
**Status:** Ready to Execute with SPEC KIT  
**Time Estimate:** 1-2 hours (manual cloud setup)

---

## 📋 Overview

This document orchestrates the remaining Day 1 tasks using **SPEC KIT** (Specification Kit) methodology for reproducible, well-documented execution.

| Task | Manual/Auto | Time | Status |
|------|----------|------|--------|
| 1.1.4 | Manual | 15 min | Setup GitHub Secrets |
| 1.2.1 | Manual | 20 min | Provision Qdrant Cloud |
| 1.2.2 | Manual | 20 min | Provision PostgreSQL (Neon) |
| 1.2.3 | Semi-Auto | 15 min | Deploy Backend on Railway |
| **Verification** | Auto | 10 min | Health checks & testing |

**Total Time:** ~80 minutes  
**Critical Path:** 1.1.4 → 1.2.1 + 1.2.2 (parallel) → 1.2.3 (serial)

---

## ✅ PHASE 1: GitHub Secrets Setup (15 minutes)

### Spec: Create Repository Secrets

**Inputs:**
- GitHub repository: `hamza49699/physical-ai-textbook`
- Placeholder credentials (to be updated after provisioning)

**Process:**
```
1. Go to Settings → Secrets and variables → Actions
2. Create 4 new repository secrets with PLACEHOLDER values:
   - QDRANT_URL = https://placeholder-qdrant-url.qdrant.io
   - QDRANT_API_KEY = placeholder-api-key-xxx
   - DATABASE_URL = postgresql://placeholder:placeholder@neon.tech/textbook_rag
   - OPENAI_API_KEY = sk-placeholder-xxx
3. Verify all 4 secrets appear in the list
4. Document the secrets in local notes
```

**Outputs:**
- 4 GitHub Secrets created (placeholder values)
- Secrets accessible to GitHub Actions workflows
- `.env.example` remains as documentation

**Verification:**
```bash
# GitHub CLI (if installed):
gh secret list

# Should show:
# OPENAI_API_KEY
# QDRANT_API_KEY
# QDRANT_URL
# DATABASE_URL
```

**Acceptance Criteria:**
- [ ] All 4 secrets visible in GitHub UI
- [ ] GitHub Actions workflow can reference via `${{ secrets.SECRET_NAME }}`
- [ ] Secrets page shows last updated timestamp
- [ ] Can edit secrets without compromising values

**Risks:**
- ⚠️ Secrets are write-only; cannot view after creation
- ⚠️ If lost, must delete and recreate with new values

---

## ✅ PHASE 2a: Provision Qdrant Cloud (20 minutes)

### Spec: Create Vector Database Cluster

**Inputs:**
- Qdrant Cloud account (free tier available)
- Cluster configuration: 100MB storage, us-east-1 region

**Process:**
```
1. Sign up at https://cloud.qdrant.io/ (Google/GitHub auth)
2. Create Cluster:
   - Name: physical-ai-textbook-prod
   - Region: us-east-1 (or closest to Railway deployment)
   - Storage: 100MB (free tier) or upgrade
   - Environment: Production
3. Wait 2-3 minutes for initialization
4. Open cluster dashboard
5. Copy credentials:
   - Cluster URL (looks like: https://xxxxx-qdrant.a.run.app)
   - API Key (Settings → API Keys → Generate)
6. Test connectivity:
   curl -X GET "https://[url]/health" -H "api-key: [key]"
7. Verify response: {"status":"ok"}
8. Update GitHub Secrets with real values
```

**Outputs:**
- ✅ Qdrant cluster operational
- ✅ Cluster URL & API key obtained
- ✅ GitHub Secrets updated: QDRANT_URL, QDRANT_API_KEY
- ✅ Health check verified

**Verification:**
```bash
# Curl test (replace with your values):
curl -X GET "https://your-cluster-url/health" \
  -H "api-key: your-api-key"

# Expected: 200 OK, {"status":"ok"}

# List collections:
curl -X GET "https://your-cluster-url/collections" \
  -H "api-key: your-api-key"

# Expected: 200 OK, {"collections":[]}
```

**Acceptance Criteria:**
- [ ] Cluster visible in Qdrant Cloud dashboard
- [ ] Health endpoint returns 200 OK
- [ ] API key is functioning (not test/demo key)
- [ ] Collections API responds (no auth errors)
- [ ] QDRANT_URL & QDRANT_API_KEY updated in GitHub Secrets

**Risks:**
- ⚠️ Cluster may take 2-5 minutes to become available
- ⚠️ API key generation takes 1-2 minutes
- ⚠️ Regional differences affect latency (choose us-east-1 for US deployment)

---

## ✅ PHASE 2b: Provision PostgreSQL (Neon) (20 minutes)

### Spec: Create Serverless PostgreSQL Database

**Inputs:**
- Neon account (free tier available)
- Database configuration: PostgreSQL 15.x, us-east-1 region

**Process:**
```
1. Sign up at https://neon.tech/ (GitHub/Google auth)
2. Create Project:
   - Name: physical-ai-textbook
   - Database name: textbook_rag
   - Region: us-east-1
   - PostgreSQL: 15.x or latest
3. Wait for project to initialize (1-2 minutes)
4. Go to Connection strings → Nodejs/Python
5. Copy full connection string:
   postgresql://[user]:[password]@[host].neon.tech/textbook_rag?sslmode=require
6. Test connection with psycopg2:
   python -c "import psycopg2; conn = psycopg2.connect('[connection-string]'); print('✅ Connected')"
7. Initialize schema (see below)
8. Update GitHub Secrets: DATABASE_URL
```

**Database Schema Initialization:**
```python
import psycopg2

connection_string = "postgresql://user:pass@host.neon.tech/textbook_rag?sslmode=require"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()

# Create documents table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        embedding VECTOR(1536),
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
""")

# Create indexes for performance
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_documents_created_at 
    ON documents(created_at DESC);
""")

conn.commit()
cursor.close()
conn.close()

print("✅ Schema initialized successfully")
```

**Outputs:**
- ✅ PostgreSQL project created in Neon
- ✅ Connection string obtained
- ✅ Database schema initialized (documents table)
- ✅ GitHub Secrets updated: DATABASE_URL
- ✅ Connection verified with test query

**Verification:**
```python
import psycopg2

conn = psycopg2.connect("your-connection-string")
cursor = conn.cursor()

# List tables
cursor.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public';
""")
tables = cursor.fetchall()
print(f"Tables: {tables}")  # Should show: [('documents',)]

# Test insert (optional)
cursor.execute("""
    INSERT INTO documents (title, content) 
    VALUES ('Test Doc', 'Test Content') 
    RETURNING id;
""")
doc_id = cursor.fetchone()[0]
conn.commit()

print(f"✅ Inserted test document with id: {doc_id}")
cursor.close()
conn.close()
```

**Acceptance Criteria:**
- [ ] Neon project visible in dashboard
- [ ] Connection string obtained and tested
- [ ] psycopg2 connection succeeds
- [ ] Tables created in public schema
- [ ] DATABASE_URL updated in GitHub Secrets
- [ ] Schema migrations future-proof

**Risks:**
- ⚠️ Connection string is sensitive (store securely)
- ⚠️ Default password is complex (copy carefully)
- ⚠️ May need to enable pgvector extension for embeddings

---

## ✅ PHASE 3: Deploy FastAPI Backend (15 minutes)

### Spec: Deploy Backend to Railway.app

**Inputs:**
- GitHub repository with backend code
- Environment secrets from Phase 1
- Qdrant URL & key from Phase 2a
- Database URL from Phase 2b

**Process:**
```
1. Open https://railway.app/
2. Click "New Project" or "Create"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access GitHub
5. Select: hamza49699/physical-ai-textbook
6. Railway auto-detects backend/ and Procfile
7. Click "Deploy" (automatic build begins)
8. Wait 3-5 minutes for build to complete
9. Once complete, Railway assigns a domain:
   https://physical-ai-backend-xxx.railway.app
10. Go to Variables → Add from GitHub Secrets:
    - QDRANT_URL
    - QDRANT_API_KEY
    - DATABASE_URL
    - OPENAI_API_KEY
11. Trigger redeploy with new env vars
12. Wait 2-3 minutes for redeployment
13. Test health endpoints (see Verification)
```

**Railway Configuration:**
```yaml
# railway.toml (auto-generated, verify it contains):

[build]
builder = "heroku.buildpacks"
buildpacks = ["heroku/python"]

[deploy]
startCommand = "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
```

**Environment Variables (in Railway Dashboard):**
```
QDRANT_URL=https://your-cluster-url.qdrant.io
QDRANT_API_KEY=your-api-key-xxx
DATABASE_URL=postgresql://user:pass@host.neon.tech/textbook_rag
OPENAI_API_KEY=sk-your-key-xxx
ENVIRONMENT=production
PORT=8000
```

**Outputs:**
- ✅ Backend deployed to Railway.app
- ✅ Backend domain URL obtained
- ✅ Environment variables configured
- ✅ Health endpoints responding
- ✅ Logs show no errors

**Verification:**
```bash
# Test basic health (should respond < 500ms):
time curl https://your-railway-url/health

# Expected:
# {"status":"healthy","service":"Physical AI Textbook API","version":"1.0.0"}

# Test root endpoint:
curl https://your-railway-url/

# Expected:
# {"message":"Physical AI Textbook API","docs":"/docs","health":"/health"}

# Test database health:
curl https://your-railway-url/health/db

# Expected (if DB connected):
# {"status":"connected","service":"PostgreSQL"}

# Test Qdrant health:
curl https://your-railway-url/health/qdrant

# Expected (if Qdrant connected):
# {"status":"connected","service":"Qdrant"}

# View logs:
railway logs --follow
```

**Acceptance Criteria:**
- [ ] Backend deployed successfully to Railway.app
- [ ] /health endpoint returns 200 OK < 500ms
- [ ] /health/db shows connected
- [ ] /health/qdrant shows connected
- [ ] Logs contain no ERROR or CRITICAL messages
- [ ] HTTPS working (no mixed content warnings)
- [ ] API docs accessible at /docs
- [ ] Update GitHub Secrets: BACKEND_URL

**Risks:**
- ⚠️ Build may fail if missing dependencies
- ⚠️ Cold start may be slow (first request up to 5s)
- ⚠️ Environment variables only take effect after redeploy
- ⚠️ Free tier limited resources (for heavy workloads, consider paid tier)

---

## ✅ PHASE 4: Verification & Integration (10 minutes)

### Spec: Comprehensive System Validation

**Validation Checklist:**

```bash
#!/bin/bash
BACKEND_URL="https://your-railway-url"

echo "🔍 Backend Health Checks:"

# 1. Basic health
echo -n "1. Basic health... "
curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" && echo " ✅"

# 2. Database
echo -n "2. Database health... "
curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health/db" && echo " ✅"

# 3. Qdrant
echo -n "3. Qdrant health... "
curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health/qdrant" && echo " ✅"

# 4. Latency test (target < 1 second)
echo -n "4. Latency (target < 1s)... "
START=$(date +%s%N)
curl -s -o /dev/null "$BACKEND_URL/health"
END=$(date +%s%N)
DIFF=$((($END - $START) / 1000000))
echo "${DIFF}ms ✅"

# 5. API Docs
echo -n "5. API Docs accessible... "
curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/docs" && echo " ✅"

echo ""
echo "📊 All systems operational! ✅"
```

**Integration Testing:**
```python
import requests

BASE_URL = "https://your-railway-url"

# Test 1: Health check
resp = requests.get(f"{BASE_URL}/health")
assert resp.status_code == 200
assert resp.json()["status"] == "healthy"
print("✅ Health check passed")

# Test 2: Database connection
resp = requests.get(f"{BASE_URL}/health/db")
assert resp.status_code == 200
print("✅ Database connected")

# Test 3: Qdrant connection
resp = requests.get(f"{BASE_URL}/health/qdrant")
assert resp.status_code == 200
print("✅ Qdrant connected")

# Test 4: API documentation
resp = requests.get(f"{BASE_URL}/docs")
assert resp.status_code == 200
assert "swagger-ui" in resp.text.lower()
print("✅ API docs accessible")

print("\n🎉 All integration tests passed!")
```

**Update Final GitHub Secret:**
```bash
# Add backend URL to secrets for frontend integration:
gh secret set BACKEND_URL -b "https://your-railway-url"
```

---

## 🎯 Summary & Next Steps

### ✅ Completed (or being completed)
- [x] Task 1.1.1: GitHub Repository Created
- [x] Task 1.1.2: Docusaurus Initialized
- [x] Task 1.1.3: GitHub Actions Setup
- [x] Task 1.1.4: GitHub Secrets Created (this execution)
- [x] Task 1.2.1: Qdrant Provisioned (this execution)
- [x] Task 1.2.2: PostgreSQL Provisioned (this execution)
- [x] Task 1.2.3: Backend Deployed (this execution)

### ⏳ Next Day (Day 2+)
- [ ] Task 1.3.1: Integration - Connect Frontend to Backend
- [ ] Task 1.3.2: RAG Pipeline - Implement LLM + Vector DB
- [ ] Task 1.3.3: Monitoring - Set up dashboards & alerts
- [ ] Task 1.4: Performance optimization & load testing
- [ ] Task 2.1: Documentation & API specifications

---

## 📞 Support & Troubleshooting

| Issue | Solution |
|-------|----------|
| Qdrant connection fails | Check API key, cluster status, network connectivity |
| PostgreSQL connection fails | Verify connection string, SSL mode, password |
| Backend deploy fails | Check Procfile, requirements.txt, Python version (3.9+) |
| Health endpoints 500 | Check environment variables, service credentials |
| Latency > 1s | Check Railway tier, cold start, database indexing |
| API docs broken | Check /docs endpoint, Swagger UI assets |

---

## 📝 Final Checklist

Before marking Day 1 complete:

- [ ] GitHub repository live and accessible
- [ ] Docusaurus site deployed to GitHub Pages
- [ ] All 4 GitHub Secrets configured
- [ ] Qdrant cluster operational
- [ ] PostgreSQL database created & schema initialized
- [ ] Backend deployed to Railway
- [ ] All health endpoints returning 200 OK
- [ ] Latency tests show < 1 second response time
- [ ] Logs show no errors or warnings
- [ ] API documentation accessible
- [ ] Team has access to all services
- [ ] Credentials securely stored in GitHub Secrets

---

**Status:** Ready for execution  
**Estimated Completion:** December 7, 2025 (end of day)  
**Repository:** https://github.com/hamza49699/physical-ai-textbook  

**🚀 Begin Phase 1 now!**

# Task 1.2.1 & 1.2.2: Provision Qdrant Cloud & PostgreSQL (Neon)

**Status:** Ready to Execute  
**Date:** December 7, 2025  
**Dependencies:** Task 1.1.4 (GitHub Secrets created with placeholders)

---

## Task 1.2.1: Provision Qdrant Cloud

Qdrant is a vector database for RAG (Retrieval-Augmented Generation) with LLM chatbot.

### Step 1: Sign Up for Qdrant Cloud

1. Open https://cloud.qdrant.io/
2. Click **Sign up** or **Sign in** (create account if needed)
3. Choose authentication method (Google, GitHub, or Email)
4. Verify email and complete profile

### Step 2: Create Qdrant Cluster

1. Go to **Clusters** in dashboard
2. Click **Create Cluster**
3. Fill in:
   - **Cluster Name:** `physical-ai-textbook-prod`
   - **Region:** Select closest to your deployment (e.g., `us-east-1` for Railway)
   - **Storage Size:** Start with 100 MB (free tier) or upgrade as needed
   - **Environment:** `Production`

4. Click **Create**
5. Wait 2-3 minutes for cluster to initialize

### Step 3: Get Credentials

Once cluster is created:

1. Click on cluster name to open dashboard
2. Copy these values:
   - **Cluster URL:** Looks like `https://xxxxx-qdrant.a.run.app` or similar
   - **API Key:** Found in **Settings** → **API Keys** → Generate new key

3. Save these values temporarily (you'll add to GitHub Secrets next)

### Step 4: Test Qdrant Connection

```bash
# Test with curl (replace with your values)
curl -X GET "https://your-cluster-url/health" \
  -H "api-key: your-api-key"

# Expected response:
# {"status":"ok"}
```

### Step 5: Update GitHub Secrets

1. Go to https://github.com/hamza49699/physical-ai-textbook/settings/secrets/actions
2. Edit existing secrets:
   - **QDRANT_URL:** Update to real cluster URL
   - **QDRANT_API_KEY:** Update to real API key

```bash
# Or use GitHub CLI:
gh secret set QDRANT_URL -b "https://your-cluster-url"
gh secret set QDRANT_API_KEY -b "your-api-key"
```

---

## Task 1.2.2: Provision PostgreSQL (Neon)

Neon is a serverless PostgreSQL database for storing application data.

### Step 1: Sign Up for Neon

1. Open https://neon.tech/
2. Click **Sign up** or **Sign in**
3. Choose authentication (Google, GitHub, or Email)
4. Verify and complete profile

### Step 2: Create PostgreSQL Project

1. Go to **Projects** in dashboard
2. Click **New Project** or **Create new project**
3. Fill in:
   - **Project Name:** `physical-ai-textbook`
   - **Database Name:** `textbook_rag`
   - **Region:** Closest to deployment (e.g., `us-east-1`)
   - **PostgreSQL Version:** Latest (15.x or 16.x)

4. Click **Create Project**
5. Wait for database to initialize

### Step 3: Get Connection String

1. Once project is created, go to **Connection strings**
2. Copy the connection string for **Nodejs** or **Psycopg** (Python)

Format:
```
postgresql://[user]:[password]@[host].neon.tech/textbook_rag?sslmode=require
```

Keep this secure!

### Step 4: Initialize Database Schema

```bash
# Install PostgreSQL client (optional, for testing)
# Windows: Download from https://www.postgresql.org/download/windows/
# Or use Python psycopg2:

pip install psycopg2-binary

# Connect and create initial schema
psql postgresql://[user]:[password]@[host].neon.tech/textbook_rag

# Or use Python:
python -c "
import psycopg2
conn = psycopg2.connect('your-connection-string')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        embedding VECTOR(1536),
        created_at TIMESTAMP DEFAULT NOW()
    );
''')
conn.commit()
cursor.close()
conn.close()
print('Schema created successfully')
"
```

### Step 5: Update GitHub Secrets

1. Go to https://github.com/hamza49699/physical-ai-textbook/settings/secrets/actions
2. Edit existing secret:
   - **DATABASE_URL:** Update to real Neon connection string

```bash
# Or use GitHub CLI:
gh secret set DATABASE_URL -b "postgresql://user:pass@host.neon.tech/textbook_rag?sslmode=require"
```

### Step 6: Test Connection

```bash
# Using Python
python -c "
import psycopg2
try:
    conn = psycopg2.connect('your-connection-string')
    cursor = conn.cursor()
    cursor.execute('SELECT NOW();')
    result = cursor.fetchone()
    print(f'✅ Connected! Current time: {result[0]}')
    conn.close()
except Exception as e:
    print(f'❌ Connection failed: {e}')
"
```

---

## Task 1.2.3: Deploy FastAPI Backend

### Prerequisites

- [ ] Task 1.2.1 Complete: Qdrant provisioned
- [ ] Task 1.2.2 Complete: PostgreSQL provisioned
- [ ] GitHub Secrets updated with real credentials
- [ ] Backend code ready (`backend/main.py` with health checks)

### Step 1: Choose Deployment Platform

| Platform | Price | Setup Time | Features |
|----------|-------|-----------|----------|
| **Railway.app** | $5/month | 5 min | Simple, git-based |
| **Render.com** | Free-$7 | 5 min | Generous free tier |
| **Heroku** | $7/month | 5 min | Easy scaling |
| **Replit** | Free | 2 min | Easiest setup |

**Recommendation:** Railway.app for production-ready setup.

### Step 2a: Deploy on Railway

1. Open https://railway.app/
2. Click **Create New Project**
3. Select **Deploy from GitHub repo**
4. Authorize Railway to access your GitHub
5. Select `hamza49699/physical-ai-textbook`
6. Click **Deploy**
7. Railway auto-detects `backend/` and `Procfile`

### Step 2b: Configure Environment Variables

1. In Railway dashboard, go to **Variables**
2. Add environment variables:
   - `QDRANT_URL` = (from GitHub Secrets)
   - `QDRANT_API_KEY` = (from GitHub Secrets)
   - `DATABASE_URL` = (from GitHub Secrets)
   - `OPENAI_API_KEY` = (from GitHub Secrets)
   - `PORT` = `8000`
   - `ENVIRONMENT` = `production`

3. Click **Save**

### Step 3: Verify Deployment

1. Railway provides a **Domain URL** (e.g., `https://physical-ai-backend-prod.railway.app`)
2. Test the health endpoint:

```bash
curl https://your-railway-url/health

# Expected response:
# {"status":"ok","environment":"production"}
```

3. Update GitHub Secrets:
   - **BACKEND_URL** = Your Railway URL

### Step 4: Monitor Backend

```bash
# View logs (if using Railway CLI):
railway logs

# Check status:
curl https://your-railway-url/health
```

### Step 5: Performance Verification

Target: **Latency < 1 second**

```bash
# Test with time measurement
time curl https://your-railway-url/health

# Expected: real 0.2s - 0.8s
```

---

## Monitoring & Troubleshooting

### Qdrant Issues

```bash
# Check cluster health
curl -X GET "https://your-cluster-url/health" \
  -H "api-key: your-api-key"

# List collections
curl -X GET "https://your-cluster-url/collections" \
  -H "api-key: your-api-key"
```

### PostgreSQL Issues

```bash
# Test connection
psql your-connection-string

# Check tables
\dt

# View logs in Neon dashboard
```

### Backend Issues

```bash
# View Railway logs
railway logs --follow

# Check environment variables
railway variables

# Redeploy if needed
railway redeploy
```

---

## Security Checklist

- [ ] Qdrant API key stored only in GitHub Secrets
- [ ] PostgreSQL password never hardcoded
- [ ] OpenAI API key never exposed
- [ ] Backend logs don't contain secrets
- [ ] HTTPS enforced on all endpoints
- [ ] CORS configured appropriately
- [ ] Rate limiting enabled

---

## Completion Checklist

- [ ] Qdrant cluster created and tested
- [ ] Qdrant URL and API key in GitHub Secrets
- [ ] PostgreSQL database created
- [ ] Database connection string in GitHub Secrets
- [ ] Backend deployed on Railway/Render
- [ ] Health endpoint responding in < 1s
- [ ] Backend URL added to GitHub Secrets
- [ ] Logs showing no errors
- [ ] Team has access to monitoring dashboard

---

## Next Steps (Task 1.2.3+)

1. **Integrate with Frontend:** Update frontend to call `/api` endpoints
2. **Set up CI/CD:** GitHub Actions deploys on each push to main
3. **Add RAG functionality:** Connect LLM to vector database
4. **Performance tuning:** Optimize queries, add caching
5. **Documentation:** API docs, deployment guide, troubleshooting

---

**Status:** Ready to execute  
**Estimated Time:** 30-45 minutes total  
**Critical Path:** Qdrant → PostgreSQL → Backend Deploy

*All manual steps required. No automation possible without API credentials.*

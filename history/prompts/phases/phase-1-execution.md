j# Phase 1: Foundation & Setup Execution Guide

**Project:** Physical AI & Humanoid Robotics — Essentials  
**Phase:** 1 (Week 1)  
**Status:** ACTIVE - Begin Immediately  
**Duration:** 7 days (2025-12-05 to 2025-12-12)  

---

## Phase 1 Overview

**Objective:** Establish production-ready infrastructure and CI/CD pipeline  

**Deliverables:**
- ✅ GitHub repository with proper configuration
- ✅ Docusaurus project initialized
- ✅ GitHub Actions CI/CD pipeline automated
- ✅ Environment variables and secrets configured
- ✅ Qdrant vector database provisioned
- ✅ PostgreSQL database ready
- ✅ FastAPI backend server deployed
- ✅ Health check endpoints verified
- ✅ Team ready to begin Phase 2

**Success Criteria:**
- All 7 tasks completed on schedule
- All health checks passing (green)
- Zero security vulnerabilities
- Zero build errors

---

## Daily Execution Schedule

### **Day 1: Monday, December 5 (TODAY)**

**Timeframe:** 3–5 hours  
**Tasks:** 1.1.1, 1.1.2, 1.1.3

#### Task 1.1.1 🔴 P0: Create GitHub Repository (30 min)

**Objective:** Initialize GitHub repository with proper structure

**Step-by-Step:**

1. **Create repository on GitHub:**
   ```bash
   # Via GitHub web interface:
   # 1. Click "New" button
   # 2. Repository name: physical-ai-textbook
   # 3. Description: "AI-native textbook with RAG chatbot for Physical AI and Humanoid Robotics"
   # 4. Visibility: Public
   # 5. Add README
   # 6. Choose license: Creative Commons Attribution 4.0 (CC-BY-4.0)
   # 7. Create repository
   ```

2. **Configure repository settings:**
   ```
   Settings → General:
   - Default branch: main ✓
   - Branch protection rules → Add rule for main:
     - Require pull request reviews: 1
     - Require status checks: Yes
     - Do not allow bypassing
   ```

3. **Enable GitHub Pages:**
   ```
   Settings → Pages:
   - Source: Deploy from a branch
   - Branch: gh-pages / root
   - HTTPS: ✓ Enforced
   ```

4. **Clone locally and set up:**
   ```bash
   cd /path/to/workspace
   git clone https://github.com/YOUR_USERNAME/physical-ai-textbook.git
   cd physical-ai-textbook
   
   # Create initial folder structure
   mkdir -p {.github/workflows,backend/tests,docs/chapters,src/components,static/diagrams}
   touch {.gitignore,.env.example}
   ```

5. **Add `.gitignore`:**
   ```bash
   # Copy from deployment guide .gitignore section
   # Paste into .gitignore file
   # Commit
   git add .gitignore
   git commit -m "chore: add gitignore"
   git push origin main
   ```

**Verification:**
- [ ] Repository exists at https://github.com/YOUR_USERNAME/physical-ai-textbook
- [ ] Public and accessible
- [ ] .gitignore committed
- [ ] GitHub Pages enabled
- [ ] HTTPS enforced

**Owner:** DevOps Engineer  
**Effort:** 30 minutes

---

#### Task 1.1.2 🟡 P1: Initialize Docusaurus Project (1 hour)

**Objective:** Set up Docusaurus v3 with clean configuration

**Step-by-Step:**

1. **Create Docusaurus project:**
   ```bash
   cd /path/to/workspace/physical-ai-textbook
   
   # Run Docusaurus scaffolder
   npx create-docusaurus@latest . classic --typescript
   
   # Answer prompts:
   # - Project name: Physical AI & Humanoid Robotics
   # - Folder name: . (current directory)
   # - Template: classic
   # - TypeScript: yes
   ```

2. **Install additional dependencies:**
   ```bash
   npm install docusaurus-plugin-search-local --save
   npm install @docusaurus/preset-classic --save
   npm install clsx --save
   ```

3. **Update `docusaurus.config.ts`:**
   ```bash
   # Replace content with config from deployment guide section 1.2
   # Key settings:
   # - url: https://YOUR_USERNAME.github.io
   # - baseUrl: /physical-ai-textbook/
   # - organizationName: YOUR_USERNAME
   # - projectName: physical-ai-textbook
   # - deploymentBranch: gh-pages
   ```

4. **Update `sidebars.ts`:**
   ```bash
   # Replace with sidebar config from deployment guide section 1.5
   # Defines all 6 chapters in navigation
   ```

5. **Test build locally:**
   ```bash
   npm run build
   
   # Verify:
   # - Build succeeds without errors
   # - Output in ./build/ directory
   # - Build time < 30 seconds
   # - No console warnings
   ```

6. **Test local server:**
   ```bash
   npm run start
   
   # Verify:
   # - Server runs on localhost:3000
   # - Can access homepage
   # - Dark/light mode toggle works
   # - Sidebar navigation appears
   # - No console errors
   ```

7. **Commit to git:**
   ```bash
   git add .
   git commit -m "feat: initialize Docusaurus v3 project"
   git push origin main
   ```

**Verification:**
- [ ] `npm run build` succeeds in < 30 seconds
- [ ] `npm run start` runs without errors
- [ ] Homepage loads on localhost:3000
- [ ] Sidebar navigation structure correct
- [ ] Dark mode toggle functional

**Owner:** Frontend Engineer  
**Effort:** 1 hour

---

#### Task 1.1.3 🟡 P1: Set Up GitHub Actions Deployment Workflow (1 hour)

**Objective:** Create automated CI/CD pipeline for Docusaurus build and GitHub Pages deployment

**Step-by-Step:**

1. **Create workflow file:**
   ```bash
   mkdir -p .github/workflows
   touch .github/workflows/deploy.yml
   ```

2. **Add workflow content:**
   ```bash
   # Copy full workflow from deployment guide section 1.4
   # File: .github/workflows/deploy.yml
   # Contains:
   # - build-frontend job (Docusaurus build)
   # - ingest-backend job (content ingestion)
   # - deploy-frontend job (GitHub Pages)
   # - test-backend job (integration tests)
   ```

3. **Commit workflow:**
   ```bash
   git add .github/workflows/deploy.yml
   git commit -m "ci: add GitHub Actions deployment workflow"
   git push origin main
   ```

4. **Verify workflow triggers:**
   ```bash
   # Go to repository → Actions tab
   # Should see "Deploy to GitHub Pages (Production)" workflow running
   # Wait for build to complete (should be green ✓)
   ```

5. **Check build output:**
   ```bash
   # In Actions tab:
   # - build-frontend: ✓ PASSED
   # - deploy-frontend: ✓ DEPLOYED
   # - Artifacts uploaded
   ```

6. **Verify GitHub Pages deployment:**
   ```bash
   # Open: https://YOUR_USERNAME.github.io/physical-ai-textbook/
   # Should see Docusaurus homepage
   # Check for any errors in browser console
   ```

**Verification:**
- [ ] GitHub Actions workflow file created
- [ ] Workflow runs successfully on main push
- [ ] Build completes in < 30 seconds
- [ ] GitHub Pages deployment successful
- [ ] Site accessible at GitHub Pages URL

**Owner:** DevOps Engineer  
**Effort:** 1 hour

---

### **Day 2: Tuesday, December 6**

**Timeframe:** 2–3 hours  
**Tasks:** 1.1.4 (Environment Setup)

#### Task 1.1.4 🟡 P1: Configure Environment Variables & Secrets (30 min)

**Objective:** Set up GitHub Secrets for API keys and database credentials

**Step-by-Step:**

1. **Create `.env.example` locally:**
   ```bash
   cat > .env.example << 'EOF'
   # Qdrant Vector Database
   QDRANT_URL=https://your-cluster-url.qdrant.io
   QDRANT_API_KEY=your-api-key
   
   # Neon PostgreSQL
   DATABASE_URL=postgresql://user:password@neon.tech/textbook_rag
   
   # OpenAI API
   OPENAI_API_KEY=sk-your-key
   OPENAI_MODEL=gpt-4o-mini
   
   # Backend
   BACKEND_URL=https://physical-ai-rag.railway.app
   BACKEND_PORT=8000
   
   # Frontend
   REACT_APP_API_URL=https://physical-ai-rag.railway.app/api
   NODE_ENV=production
   EOF
   ```

2. **Commit `.env.example`:**
   ```bash
   git add .env.example
   git commit -m "docs: add environment variables example"
   git push origin main
   ```

3. **Add GitHub Secrets:**
   ```
   Repository → Settings → Secrets and variables → Actions
   
   Click "New repository secret" and add each:
   
   Secret 1: QDRANT_URL
   Value: (will get from Qdrant setup)
   
   Secret 2: QDRANT_API_KEY
   Value: (will get from Qdrant setup)
   
   Secret 3: DATABASE_URL
   Value: (will get from PostgreSQL setup)
   
   Secret 4: OPENAI_API_KEY
   Value: (your OpenAI API key)
   ```

4. **Verify secrets added:**
   ```
   Settings → Secrets and variables → Actions
   Should show all 4 secrets (values hidden)
   ```

**Verification:**
- [ ] `.env.example` committed to repository
- [ ] All 4 GitHub Secrets created
- [ ] Secrets visible in Settings
- [ ] Workflow can access secrets

**Owner:** DevOps Engineer  
**Effort:** 30 minutes

---

### **Days 3–4: Wednesday & Thursday, December 6–7**

**Timeframe:** 3–4 hours  
**Tasks:** 1.2.1, 1.2.2 (Infrastructure)

#### Task 1.2.1 🟡 P1: Provision Qdrant Cloud Instance (30 min)

**Objective:** Set up Qdrant vector database for RAG embeddings

**Step-by-Step:**

1. **Sign up for Qdrant Cloud:**
   - Visit https://cloud.qdrant.io
   - Create account (free tier)
   - Verify email

2. **Create cluster:**
   ```
   Dashboard → Create Cluster
   - Name: physical-ai-textbook-prod
   - Tier: Free tier
   - Region: US-East-1 (or closest)
   - Create
   ```

3. **Get cluster credentials:**
   ```
   Cluster → Connection Details
   - Copy "REST API URL" (e.g., https://xxx-qdrant.a.run.app)
   - Copy "API Key"
   ```

4. **Add to GitHub Secrets:**
   ```bash
   # In GitHub Settings → Secrets:
   
   QDRANT_URL = https://xxx-qdrant.a.run.app
   QDRANT_API_KEY = your-api-key
   ```

5. **Test connection locally:**
   ```bash
   pip install qdrant-client
   
   python << 'EOF'
   from qdrant_client import QdrantClient
   import os
   
   client = QdrantClient(
       url=os.getenv('QDRANT_URL'),
       api_key=os.getenv('QDRANT_API_KEY')
   )
   
   # Test connection
   collections = client.get_collections()
   print(f"✅ Qdrant connected! Collections: {len(collections.collections)}")
   EOF
   ```

**Verification:**
- [ ] Qdrant cluster created
- [ ] Credentials obtained
- [ ] GitHub Secrets updated
- [ ] Connection test successful

**Owner:** DevOps Engineer  
**Effort:** 30 minutes

---

#### Task 1.2.2 🟡 P1: Provision Neon PostgreSQL Instance (45 min)

**Objective:** Set up PostgreSQL database for metadata and chat history

**Step-by-Step:**

1. **Sign up for Neon:**
   - Visit https://neon.tech
   - Create account (free tier)
   - Verify email

2. **Create project:**
   ```
   Dashboard → Create Project
   - Name: physical-ai-textbook
   - Region: US-East
   - Create
   ```

3. **Create database:**
   ```
   Project → Databases → Create Database
   - Database name: textbook_rag
   - Create
   ```

4. **Get connection string:**
   ```
   Connection String (copy):
   postgresql://user:password@neon.tech/textbook_rag
   ```

5. **Create schema:**
   ```bash
   # Connect via psql or Neon web console
   psql "postgresql://user:password@neon.tech/textbook_rag"
   
   # Run SQL:
   CREATE TABLE chunks (
     id SERIAL PRIMARY KEY,
     chapter INT NOT NULL,
     section VARCHAR(255) NOT NULL,
     content TEXT NOT NULL,
     embedding_id VARCHAR(255),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE TABLE chat_sessions (
     id SERIAL PRIMARY KEY,
     query TEXT NOT NULL,
     response TEXT NOT NULL,
     confidence FLOAT,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE INDEX idx_chapter ON chunks(chapter);
   CREATE INDEX idx_section ON chunks(section);
   
   \q
   ```

6. **Test connection:**
   ```bash
   pip install psycopg2-binary
   
   python << 'EOF'
   import psycopg2
   
   conn = psycopg2.connect(
       "postgresql://user:password@neon.tech/textbook_rag"
   )
   cursor = conn.cursor()
   cursor.execute("SELECT COUNT(*) FROM chunks;")
   print(f"✅ PostgreSQL connected! Chunks: {cursor.fetchone()[0]}")
   conn.close()
   EOF
   ```

7. **Add to GitHub Secrets:**
   ```bash
   # In GitHub Settings → Secrets:
   DATABASE_URL = postgresql://user:password@neon.tech/textbook_rag
   ```

**Verification:**
- [ ] Neon project created
- [ ] Database and tables created
- [ ] Schema tables visible
- [ ] Connection test successful
- [ ] GitHub Secrets updated

**Owner:** DevOps Engineer  
**Effort:** 45 minutes

---

### **Days 5–6: Friday & Saturday, December 8–9**

**Timeframe:** 2–3 hours  
**Tasks:** 1.2.3 (Backend Deployment)

#### Task 1.2.3 🟡 P1: Deploy FastAPI Backend Server (1 hour)

**Objective:** Set up and deploy FastAPI backend on Railway or Render

**Step-by-Step:**

1. **Choose platform:** Railway (recommended for ease) or Render

2. **Prepare backend code:**
   ```bash
   # Create backend files locally:
   cd /path/to/physical-ai-textbook
   
   # Create backend/app.py from implementation guide section 4.1
   # Create backend/ingest.py from implementation guide section 4.2
   # Create backend/requirements.txt from implementation guide section 4.3
   # Create backend/tests/test_integration.py from implementation guide section 6.1
   
   git add backend/
   git commit -m "feat: add FastAPI backend application"
   git push origin main
   ```

3. **Deploy on Railway:**
   ```
   1. Visit https://railway.app
   2. Sign up (connect GitHub)
   3. New Project → Deploy from GitHub
   4. Select: physical-ai-textbook repository
   5. Configure:
      - Root directory: backend/
      - Build command: pip install -r requirements.txt
      - Start command: uvicorn app:app --host 0.0.0.0 --port $PORT
   6. Environment variables (Railway UI):
      - QDRANT_URL: [from secrets]
      - QDRANT_API_KEY: [from secrets]
      - DATABASE_URL: [from secrets]
      - OPENAI_API_KEY: [from secrets]
   7. Deploy
   ```

4. **OR Deploy on Render:**
   ```
   1. Visit https://render.com
   2. Sign up (connect GitHub)
   3. New Web Service
   4. Select: physical-ai-textbook repository
   5. Configure:
      - Name: physical-ai-rag
      - Environment: Python 3.11
      - Root: backend/
      - Build: pip install -r requirements.txt
      - Start: uvicorn app:app --host 0.0.0.0 --port $PORT
      - Plan: Free tier
   6. Environment variables (add same as Railway)
   7. Deploy
   ```

5. **Wait for deployment:**
   ```bash
   # Check deployment status in Railway/Render dashboard
   # Should show "✓ Running" after 2-5 minutes
   ```

6. **Get deployment URL:**
   ```bash
   # Railway: https://physical-ai-rag-production.up.railway.app
   # Render: https://physical-ai-rag.onrender.com
   
   # Add to GitHub Secrets as BACKEND_URL
   ```

7. **Test health endpoint:**
   ```bash
   curl https://physical-ai-rag.railway.app/health
   
   # Should return:
   # {
   #   "status": "ok",
   #   "qdrant": "connected",
   #   "database": "connected"
   # }
   ```

8. **Update workflow with backend URL:**
   ```bash
   # Edit .github/workflows/deploy.yml
   # Update BACKEND_URL environment variable
   
   git add .github/
   git commit -m "ci: update backend URL"
   git push origin main
   ```

**Verification:**
- [ ] Backend deployed successfully
- [ ] Health endpoint responds 200 OK
- [ ] Qdrant connection verified
- [ ] PostgreSQL connection verified
- [ ] GitHub Secrets updated with BACKEND_URL

**Owner:** Backend Engineer  
**Effort:** 1 hour

---

### **Day 7: Sunday, December 10** 

**Timeframe:** 2–3 hours  
**Tasks:** Final verification and sign-off

#### Phase 1 Final Verification Checklist

**Frontend (Docusaurus):**

```bash
# Test build locally
npm run build

# Verify
✓ Build succeeds
✓ Build time < 30 seconds
✓ No console errors
✓ build/ directory created
✓ Lighthouse score ≥ 90
```

**GitHub Actions:**

```bash
# Check Actions tab
✓ Latest workflow passed
✓ All jobs completed
✓ build-frontend: PASSED
✓ deploy-frontend: DEPLOYED
✓ Site accessible at GitHub Pages URL
```

**Backend API:**

```bash
# Test endpoints
curl https://physical-ai-rag.railway.app/health
✓ Returns 200 OK
✓ All services connected

curl https://physical-ai-rag.railway.app/api/docs
✓ Returns API documentation
```

**Infrastructure:**

```bash
✓ Qdrant cluster: healthy
✓ PostgreSQL database: accessible
✓ OpenAI API: connected
✓ GitHub Secrets: all configured
✓ HTTPS: enforced everywhere
```

**Security:**

```bash
✓ No API keys in code
✓ No secrets in git history
✓ .env.local in .gitignore
✓ GitHub Secrets stored securely
✓ Rate limiting enabled
✓ CORS configured
```

---

## Phase 1 Sign-Off

**Phase Lead Checklist:**

- [ ] All 7 tasks completed
- [ ] All verification items pass
- [ ] No blocking issues
- [ ] Team ready for Phase 2
- [ ] Documentation updated

**Sign-Off Template:**

```
Phase 1 Completion Report
Date: [DATE]
Completed by: [NAME]

✅ Task 1.1.1: GitHub Repository - COMPLETED
✅ Task 1.1.2: Docusaurus Init - COMPLETED
✅ Task 1.1.3: GitHub Actions - COMPLETED
✅ Task 1.1.4: Environment Setup - COMPLETED
✅ Task 1.2.1: Qdrant Cloud - COMPLETED
✅ Task 1.2.2: PostgreSQL - COMPLETED
✅ Task 1.2.3: FastAPI Backend - COMPLETED

All systems operational ✓
Ready to begin Phase 2 ✓

Approved by: [PROJECT LEAD]
```

---

## Phase 1 → Phase 2 Transition

**On Phase 1 Completion:**

1. Update `tasks.md` - Mark Phase 1 tasks as completed
2. Team standup - Discuss Phase 2 readiness
3. **BEGIN PHASE 2: Content Creation (Weeks 2-4)**

**Phase 2 Will Cover:**
- Content outline creation
- 6 chapters writing (1,000-1,500 words each)
- 12-16 diagrams creation
- Peer review process

---

## Support During Phase 1

**If issues occur:**

1. **Build fails:** Check GitHub Actions logs for errors
2. **Qdrant connection fails:** Verify credentials in GitHub Secrets
3. **Database connection fails:** Check Neon connection string format
4. **Backend won't deploy:** Check Railway/Render logs
5. **GitHub Pages not updating:** Wait 2-3 minutes after push

**Emergency contacts:**
- GitHub Support: https://support.github.com
- Railway Support: https://railway.app/support
- Qdrant Support: https://qdrant.io/support

---

**Phase 1 Status:** 🚀 READY TO BEGIN  
**Start Date:** 2025-12-05 (TODAY)  
**Target Completion:** 2025-12-12  
**Next Phase:** Phase 2 - Content Creation

---

**LET'S BUILD! 🚀**

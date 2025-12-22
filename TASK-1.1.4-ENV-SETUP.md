# Task 1.1.4: Configure Environment Variables & GitHub Secrets

**Status:** In Progress  
**Date:** December 7, 2025  
**Repository:** https://github.com/hamza49699/physical-ai-textbook

---

## Overview

This task involves:
1. Creating GitHub Secrets for CI/CD pipeline
2. Setting up placeholders for external services (Qdrant, PostgreSQL, OpenAI)
3. Preparing backend environment configuration

---

## Required Environment Variables

Based on `.env.example`, you need:

| Variable | Required | Where to Get | Format |
|----------|----------|-------------|--------|
| `QDRANT_URL` | Yes | Qdrant Cloud | `https://your-cluster-url.qdrant.io` |
| `QDRANT_API_KEY` | Yes | Qdrant Cloud | API Key from dashboard |
| `DATABASE_URL` | Yes | Neon PostgreSQL | `postgresql://user:password@neon.tech/db` |
| `OPENAI_API_KEY` | Yes | OpenAI Platform | `sk-...` |
| `OPENAI_MODEL` | No | Hardcoded | Default: `gpt-4o-mini` |
| `BACKEND_URL` | Yes | Railway/Render | Backend deployment URL |
| `BACKEND_PORT` | No | Hardcoded | Default: `8000` |
| `REACT_APP_API_URL` | Yes | Same as BACKEND_URL | With `/api` suffix |

---

## Step 1: Create GitHub Secrets (MANUAL)

1. Open your repository: https://github.com/hamza49699/physical-ai-textbook
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Create these 4 secrets with placeholder values (we'll update later):

### Secret 1: QDRANT_URL
```
Name: QDRANT_URL
Value: https://placeholder-qdrant-url.qdrant.io
```

### Secret 2: QDRANT_API_KEY
```
Name: QDRANT_API_KEY
Value: placeholder-api-key-will-update-after-provisioning
```

### Secret 3: DATABASE_URL
```
Name: DATABASE_URL
Value: postgresql://placeholder:placeholder@placeholder.neon.tech/textbook_rag
```

### Secret 4: OPENAI_API_KEY
```
Name: OPENAI_API_KEY
Value: sk-placeholder-will-update-with-real-key
```

**After adding all 4 secrets, verify they appear in the Secrets list.**

---

## Step 2: Verify GitHub Actions Can Access Secrets

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will use these secrets:

```yaml
env:
  QDRANT_URL: ${{ secrets.QDRANT_URL }}
  QDRANT_API_KEY: ${{ secrets.QDRANT_API_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

---

## Step 3: Update Backend to Use Secrets

The backend (`backend/main.py`) should read from environment:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Load from environment
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/textbook_rag")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
```

---

## Step 4: Document Secrets for Team

Create `.env.secrets` (DO NOT COMMIT):
```
# This file is for local development only
# Copy values from GitHub Secrets after they're created

QDRANT_URL=https://[get-from-qdrant-cloud].qdrant.io
QDRANT_API_KEY=[get-from-qdrant-dashboard]
DATABASE_URL=postgresql://[user]:[password]@[host].neon.tech/textbook_rag
OPENAI_API_KEY=sk-[get-from-openai-platform]
```

---

## Step 5: Next Tasks (Dependent)

- **Task 1.2.1:** Provision Qdrant Cloud → Get real `QDRANT_URL` and `QDRANT_API_KEY`
- **Task 1.2.2:** Provision PostgreSQL → Get real `DATABASE_URL`
- **Task 1.2.3:** Deploy FastAPI Backend → Use secrets in deployment

---

## Checklist

- [ ] Logged into https://github.com/hamza49699/physical-ai-textbook
- [ ] Navigated to Settings → Secrets and variables → Actions
- [ ] Created 4 repository secrets (all with placeholder values)
- [ ] Verified secrets appear in the list
- [ ] `.env.example` exists locally
- [ ] Ready to proceed to Task 1.2.1

---

## Security Notes

⚠️ **DO NOT:**
- Hardcode secrets in code
- Commit `.env` files to git
- Share API keys publicly
- Use the same key for multiple environments

✅ **DO:**
- Rotate keys regularly
- Use GitHub Secrets for all sensitive data
- Use environment-specific variables (dev, staging, prod)
- Audit secret access in GitHub

---

## Commands for Next Steps

```bash
# After provisioning services, update secrets on GitHub via API:
# (Requires GitHub CLI)

# gh secret set QDRANT_URL -b "https://your-real-url.qdrant.io"
# gh secret set QDRANT_API_KEY -b "your-real-key"
# gh secret set DATABASE_URL -b "postgresql://real:url@host/db"
# gh secret set OPENAI_API_KEY -b "sk-real-key"

# View secrets (values are hidden):
# gh secret list
```

---

**Status:** Ready for manual GitHub Secrets creation  
**Next:** Task 1.2.1 - Provision Qdrant Cloud

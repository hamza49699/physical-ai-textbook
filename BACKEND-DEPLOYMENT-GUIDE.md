# 🚀 Backend Deployment & Frontend Connection Guide

## ✅ Backend Deployed Successfully!

Your backend is now live at: **https://hamzakhan123-physical-ai-textbook.hf.space**

---

## 📋 Step 1: Verify Backend APIs

### Test the Backend Endpoints

Run this PowerShell script to test all endpoints:

```powershell
cd c:\Users\digital\claude_first
powershell -ExecutionPolicy Bypass -File test_deployed_backend.ps1
```

Or test manually in browser:
- Root: https://hamzakhan123-physical-ai-textbook.hf.space/
- Health: https://hamzakhan123-physical-ai-textbook.hf.space/health
- Docs: https://hamzakhan123-physical-ai-textbook.hf.space/docs

Expected response from `/health`:
```json
{
  "status": "healthy",
  "database": "connected",
  "qdrant": "connected",
  "timestamp": "2025-12-19T..."
}
```

---

## 🔗 Step 2: Connect Frontend to Backend

### Environment Configuration (Already Done ✓)

I've updated your environment files:

**`.env.production`** - For GitHub Pages deployment:
```env
REACT_APP_BACKEND_URL=https://hamzakhan123-physical-ai-textbook.hf.space
```

**`.env.local`** - For local testing:
```env
REACT_APP_BACKEND_URL=http://localhost:8000
# Or uncomment to test with deployed backend:
# REACT_APP_BACKEND_URL=https://hamzakhan123-physical-ai-textbook.hf.space
```

---

## 🌐 Step 3: Deploy to GitHub Pages

### Option A: Quick Deploy (Recommended)

```powershell
cd physical-ai-textbook
npm run build
npm run deploy
```

This will:
1. Build your site with production environment variables
2. Deploy to GitHub Pages at: **https://hamza49699.github.io/physical-ai-textbook/**

### Option B: Manual Deploy with GitHub Actions

1. **Create `.github/workflows/deploy.yml`:**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: npm
          cache-dependency-path: physical-ai-textbook/package-lock.json
      
      - name: Install dependencies
        working-directory: physical-ai-textbook
        run: npm ci
      
      - name: Build website
        working-directory: physical-ai-textbook
        env:
          REACT_APP_BACKEND_URL: https://hamzakhan123-physical-ai-textbook.hf.space
        run: npm run build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: physical-ai-textbook/build
          user_name: github-actions[bot]
          user_email: github-actions[bot]@users.noreply.github.com
```

2. **Push to GitHub:**
```powershell
cd c:\Users\digital\claude_first\physical-ai-textbook
git add .
git commit -m "Connect frontend to Hugging Face backend"
git push origin main
```

---

## 🧪 Step 4: Test the Complete Integration

### Local Testing (Optional)

Test with deployed backend before deploying:

```powershell
cd physical-ai-textbook

# Update .env.local to use deployed backend
# REACT_APP_BACKEND_URL=https://hamzakhan123-physical-ai-textbook.hf.space

npm start
```

Then open http://localhost:3000 and test the chatbot.

### Live Testing

After deployment:

1. Visit: https://hamza49699.github.io/physical-ai-textbook/
2. Click the chatbot button (💬) in bottom right
3. Ask: "What is ROS2?"
4. The response should come from your Hugging Face backend

---

## 🔍 Troubleshooting

### CORS Issues

If you see CORS errors, verify backend allows your frontend URL:

In `backend/main.py`, check:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hamza49699.github.io",  # Your GitHub Pages
        "http://localhost:3000"           # Local dev
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend Not Responding

1. Check Hugging Face Space status: https://huggingface.co/spaces/hamzakhan123/physical-ai-textbook
2. View logs in Hugging Face Space settings
3. Verify all environment variables are set correctly

### Chatbot Not Working

1. Open browser DevTools (F12) → Console
2. Look for network errors
3. Check the fetch request is going to correct URL
4. Verify backend health endpoint responds

---

## 📊 API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root welcome message |
| `/health` | GET | Overall health check |
| `/health/db` | GET | Database connection check |
| `/health/qdrant` | GET | Vector DB check |
| `/query` | POST | RAG chatbot query |
| `/documents` | GET | List ingested documents |
| `/ingest` | POST | Ingest new documents |
| `/docs` | GET | API documentation (Swagger) |

---

## 🎯 Next Steps

1. **Test Backend APIs** (Step 1)
   ```powershell
   powershell -ExecutionPolicy Bypass -File test_deployed_backend.ps1
   ```

2. **Deploy Frontend** (Step 3)
   ```powershell
   cd physical-ai-textbook
   npm run build
   npm run deploy
   ```

3. **Test Live Site** (Step 4)
   - Visit: https://hamza49699.github.io/physical-ai-textbook/
   - Test chatbot functionality

---

## 🔐 Security Checklist

✅ Environment variables set in Hugging Face Secrets  
✅ No API keys in frontend code  
✅ CORS configured for specific origins  
✅ Database connection uses SSL  
✅ Production environment variables configured  

---

## 📝 Quick Commands

```powershell
# Test backend
powershell -ExecutionPolicy Bypass -File test_deployed_backend.ps1

# Build and deploy frontend
cd physical-ai-textbook
npm run build
npm run deploy

# Local development
npm start

# View build output
npm run serve
```

---

## 🌟 Your Live URLs

- **Frontend (GitHub Pages):** https://hamza49699.github.io/physical-ai-textbook/
- **Backend (Hugging Face):** https://hamzakhan123-physical-ai-textbook.hf.space
- **API Docs:** https://hamzakhan123-physical-ai-textbook.hf.space/docs
- **Health Check:** https://hamzakhan123-physical-ai-textbook.hf.space/health

---

**Ready to deploy!** 🚀 Let me know if you encounter any issues.

# 🔧 Backend Configuration & Deployment Fix Guide

## ✅ Issues Fixed

### 1. Qdrant 403 Forbidden Error
**Problem**: QdrantClient wasn't properly authenticating with API key

**Solution Applied**:
- Updated `get_qdrant_client()` in `backend/main.py`
- Added proper API key validation
- Set `prefer_grpc=False` and `timeout=60` for better compatibility
- Added error logging for missing API key

### 2. Port Mismatch (8000 vs 7860)
**Problem**: Frontend expected backend on port 8000, but Hugging Face runs on 7860

**Solution Applied**:
- Changed default `PORT=7860` in `backend/.env`
- Updated `backend/main.py` to use PORT 7860 by default
- Updated frontend `.env.local` to use `http://localhost:7860`
- Frontend production uses Hugging Face URL (no port issue)

### 3. CORS Configuration
**Problem**: Backend might block requests from frontend origins

**Solution Applied**:
- Updated CORS middleware to explicitly allow:
  - `http://localhost:3000` (local dev)
  - `http://localhost:7860` (same-origin local)
  - `http://0.0.0.0:7860` (Hugging Face internal)
  - `https://hamza49699.github.io` (production frontend)
  - `https://hamzakhan123-physical-ai-textbook.hf.space` (backend itself)

## 🔐 Required Environment Variables

### For Hugging Face Deployment

Go to your Space settings and ensure these secrets are set:

#### 1. Database (PostgreSQL - Neon)
```bash
DATABASE_URL=postgresql://neondb_owner:npg_zQx1JBHe0smZ@ep-jolly-pine-ahnhc5wu-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

#### 2. Qdrant Vector Database
```bash
QDRANT_URL=https://e400d56e-2ba5-492d-b6c5-2eb42dce887d.us-east4-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.so4BVvY3wHPVAk3g2deqJ2oRLcf0cY17DmTxTaSf5vo
```

#### 3. Cohere API (for AI responses)
```bash
COHERE_API_KEY=fQMs9QIQO3ZckqX7FpEeM2u7fRGuhHfUxIhPUFKH
COHERE_MODEL=command-r-plus
```

#### 4. Port Configuration
```bash
PORT=7860
```

#### 5. Frontend URL (for CORS)
```bash
FRONTEND_URL=https://hamza49699.github.io
```

### For Local Development

Your `backend/.env` file should have:

```bash
# PostgreSQL (Neon)
DATABASE_URL=postgresql://neondb_owner:npg_zQx1JBHe0smZ@ep-jolly-pine-ahnhc5wu-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require

# Qdrant
QDRANT_URL=https://e400d56e-2ba5-492d-b6c5-2eb42dce887d.us-east4-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.so4BVvY3wHPVAk3g2deqJ2oRLcf0cY17DmTxTaSf5vo

# Cohere
COHERE_API_KEY=fQMs9QIQO3ZckqX7FpEeM2u7fRGuhHfUxIhPUFKH
COHERE_MODEL=command-r-plus

# Backend
PORT=7860
NODE_ENV=development
FRONTEND_URL=http://localhost:3000
```

## 🚀 How to Deploy/Update

### 1. Update Hugging Face Space

1. **Go to Space Settings**: https://huggingface.co/spaces/hamzakhan123/physical-ai-textbook/settings

2. **Update Environment Variables** (Settings → Variables and secrets):
   - Add/update all variables listed above
   - Make sure `QDRANT_API_KEY` is correctly set (this fixes the 403 error)

3. **Push Updated Code**:
   ```powershell
   cd physical-ai-textbook/backend
   git add main.py .env
   git commit -m "Fix Qdrant auth and CORS configuration"
   git push
   ```

4. **Restart Space**: Settings → Factory reboot

### 2. Deploy Updated Frontend

```powershell
cd physical-ai-textbook
npm run build
npm run deploy
```

## 🧪 Testing

### Test Backend Health
```powershell
$response = Invoke-RestMethod -Uri "https://hamzakhan123-physical-ai-textbook.hf.space/health" -Method Get
$response | ConvertTo-Json
```

**Expected Output**:
```json
{
  "status": "ok",
  "database": "connected",
  "qdrant": "connected",
  "embedding_model": "all-MiniLM-L6-v2",
  "version": "1.0.0"
}
```

### Test Query Endpoint
```powershell
$body = @{ query = "What is ROS2?" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "https://hamzakhan123-physical-ai-textbook.hf.space/query" -Method Post -Body $body -ContentType "application/json"
$response.response
```

### Test Local Backend
```powershell
cd physical-ai-textbook/backend
python main.py
```

Then visit: http://localhost:7860/docs

## 📊 Port Configuration Summary

| Environment | Backend Port | Frontend Dev | Frontend Prod |
|-------------|--------------|--------------|---------------|
| Local Dev   | 7860         | localhost:3000 | N/A |
| Hugging Face| 7860         | N/A          | github.io |

## ⚠️ Common Issues & Solutions

### Issue 1: "403 Forbidden" from Qdrant
**Cause**: Missing or incorrect `QDRANT_API_KEY`
**Solution**: Verify the API key in Hugging Face secrets matches your Qdrant dashboard

### Issue 2: CORS Error in Browser
**Cause**: Frontend origin not in CORS allowed list
**Solution**: Backend now includes all necessary origins. Restart the backend.

### Issue 3: "Connection Refused" on port 8000
**Cause**: Backend running on 7860, not 8000
**Solution**: Already fixed - all configs now use 7860

### Issue 4: Database Connection Error
**Cause**: Neon database might be in sleep mode (free tier)
**Solution**: 
1. Visit https://console.neon.tech
2. Wake up the database by accessing it
3. Check connection string includes `?sslmode=require`

## 🎯 Verification Checklist

After deploying, verify:

- [ ] Hugging Face Space is running (green status)
- [ ] Health endpoint returns all "connected" status
- [ ] Query endpoint responds without 500 error
- [ ] Frontend chatbot can send messages
- [ ] No CORS errors in browser console
- [ ] Database queries work (check logs)

## 📝 Next Steps

1. **Push backend changes** to Hugging Face
2. **Update environment variables** in Hugging Face settings
3. **Restart the Space**
4. **Test the health endpoint**
5. **Deploy frontend** with `npm run deploy`
6. **Test on live site**: https://hamza49699.github.io/physical-ai-textbook/

---

**Updated**: December 19, 2025
**Status**: Ready for deployment

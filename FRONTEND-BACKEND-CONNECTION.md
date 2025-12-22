# Frontend-Backend Connection Guide

## ✅ Backend Status (Hugging Face)

Your backend is deployed at: **https://hamzakhan123-physical-ai-textbook.hf.space**

### Health Check Results:
- ✅ Status: OK
- ❌ Database: ERROR (needs fix)
- ✅ Qdrant: Connected
- ✅ Embedding Model: all-MiniLM-L6-v2

## 🔧 Frontend Configuration Complete

I've updated the following files to connect your website to the deployed backend:

### 1. Environment Configuration
- **File**: `.env.production`
- **Backend URL**: `https://hamzakhan123-physical-ai-textbook.hf.space`

### 2. Docusaurus Config
- **File**: `docusaurus.config.ts`
- Added `customFields.backendUrl` for backend API access

### 3. Chatbot Component
- **File**: `src/components/Chatbot.tsx`
- Updated to use Docusaurus config for backend URL
- Improved error handling

## 🚀 Deploy to GitHub Pages

Run these commands to deploy your updated website:

```powershell
# Build the website
npm run build

# Deploy to GitHub Pages
npm run deploy
```

Or use the combined command:
```powershell
npm run build; npm run deploy
```

## 🔍 Testing After Deployment

Once deployed, your chatbot at **https://hamza49699.github.io/physical-ai-textbook/** will automatically connect to the Hugging Face backend.

### Test the chatbot:
1. Visit your live website
2. Click the chatbot icon (bottom right)
3. Ask a question like "What is ROS2?"

## ⚠️ Known Issues

### Database Connection Error
The backend health check shows `"database": "error"`. This needs to be fixed:

**Possible causes:**
1. DATABASE_URL environment variable might be incorrect in Hugging Face
2. Neon PostgreSQL database might be sleeping (free tier limitation)
3. Network connectivity issue between Hugging Face and Neon

**Quick Fix:**
1. Go to Hugging Face Space settings
2. Verify the DATABASE_URL secret is correct
3. Check if Neon database is active (visit neon.tech dashboard)
4. Restart the Hugging Face Space

### Query API Returns 500 Error
The `/query` endpoint returns 500 error, likely due to the database connection issue.

## 🔐 CORS Configuration

The backend is already configured to allow requests from your GitHub Pages domain:
- `https://hamza49699.github.io`
- `https://*.github.io`

## 📊 Monitoring

To check backend status anytime, run:
```powershell
$response = Invoke-RestMethod -Uri "https://hamzakhan123-physical-ai-textbook.hf.space/health" -Method Get -ContentType "application/json"
$response | ConvertTo-Json
```

## 🎯 Next Steps

1. ✅ Frontend code updated
2. ⏳ Fix database connection in Hugging Face
3. ⏳ Deploy frontend to GitHub Pages
4. ⏳ Test chatbot on live site

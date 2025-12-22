# 🧪 Local Testing - Quick Start

**Ready to test locally?** Follow these simple steps:

---

## ⚡ Quick Start (5 minutes)

### Windows PowerShell
```powershell
cd c:\Users\digital\claude_first\physical-ai-textbook
.\setup-local.ps1
```

### Windows CMD
```bash
cd c:\Users\digital\claude_first\physical-ai-textbook
setup-local.bat
```

### Linux/macOS
```bash
cd ~/claude_first/physical-ai-textbook
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
npm install
```

---

## 🚀 Run Backend & Frontend

**Terminal 1: Start Backend**
```bash
cd backend
python main.py

# You should see:
# ✅ Loaded embedding model: all-MiniLM-L6-v2
# ✅ API startup complete
# Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2: Start Frontend**
```bash
npm start

# You should see:
# [INFO] Docusaurus server started on http://localhost:3000
```

---

## ✅ Test What Works

### API Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
Open in browser: **http://localhost:8000/docs**

### Frontend
Open in browser: **http://localhost:3000**

---

## 📝 Ingest & Query Example

### Add a Document
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Chapter 1: Physical AI",
    "chapter": 1,
    "section": "Introduction",
    "content": "Physical AI combines robotics, artificial intelligence, and digital twins to create systems that understand and interact with the physical world."
  }'
```

### Query the Chatbot
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?"}'
```

---

## 📖 Full Testing Guide

For detailed testing instructions, see: **`LOCAL-TESTING-GUIDE.md`**

---

## 🐛 Issues?

### Python/Node not found?
- Install Python: https://www.python.org/
- Install Node.js: https://nodejs.org/

### venv activation fails?
```bash
# Use full path:
c:\Users\digital\claude_first\physical-ai-textbook\venv\Scripts\activate
```

### Can't install packages?
```bash
# Upgrade pip:
python -m pip install --upgrade pip
```

---

**Ready? Start with Terminal 1 above!** 🚀

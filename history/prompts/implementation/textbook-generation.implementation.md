# Implementation Guide: Textbook Generation

**Feature:** Physical AI & Humanoid Robotics — Essentials  
**Project:** textbook-generation  
**Created:** 2025-12-05  
**Status:** Code Generation Phase  
**Objective:** Full source code generation and deployment scaffolding

---

## I. Project Repository Structure

```
physical-ai-textbook/
├── .github/
│   └── workflows/
│       └── deploy.yml                    # GitHub Actions CI/CD pipeline
├── backend/
│   ├── app.py                            # FastAPI main application
│   ├── ingest.py                         # Content ingestion script
│   ├── models.py                         # Pydantic data models
│   ├── rag.py                            # RAG query logic
│   ├── validation.py                     # Response validation
│   ├── requirements.txt                  # Python dependencies
│   └── tests/
│       ├── test_integration.py           # End-to-end tests
│       └── test_queries.py               # Query tests
├── docs/
│   ├── intro.md                          # Textbook intro
│   └── chapters/
│       ├── ch1-physical-ai.md            # Chapter 1
│       ├── ch2-humanoid-robotics.md      # Chapter 2
│       ├── ch3-ros2.md                   # Chapter 3
│       ├── ch4-digital-twin.md           # Chapter 4
│       ├── ch5-vla.md                    # Chapter 5
│       └── ch6-capstone.md               # Chapter 6
├── src/
│   ├── components/
│   │   ├── ChatbotWidget.tsx             # Main chatbot widget
│   │   ├── ChatbotWidget.module.css      # Widget styles
│   │   ├── CitationBlock.tsx             # Citation display
│   │   └── CitationBlock.module.css      # Citation styles
│   ├── css/
│   │   └── custom.css                    # Custom Docusaurus styles
│   └── pages/
│       └── index.tsx                     # Homepage
├── static/
│   └── diagrams/                         # Chapter diagrams
├── .env.example                          # Environment template
├── .gitignore                            # Git ignore rules
├── docusaurus.config.ts                  # Docusaurus configuration
├── sidebars.ts                           # Navigation sidebar config
├── package.json                          # Node.js dependencies
├── tsconfig.json                         # TypeScript configuration
├── README.md                             # Project documentation
├── CONTRIBUTING.md                       # Contribution guidelines
├── STYLE_GUIDE.md                        # Content style guide
├── ARCHITECTURE.md                       # System architecture
└── LICENSE                               # MIT License
```

---

## II. Phase 1: Foundation Code Generation (Week 1)

### 2.1 GitHub Actions Deployment Workflow

**File:** `.github/workflows/deploy.yml`

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build Docusaurus
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.BACKEND_URL }}
      
      - name: Test build output
        run: |
          if [ ! -d "build" ]; then
            echo "Build directory not found"
            exit 1
          fi
          echo "Build successful: $(du -sh build)"
      
      - name: Setup Python for ingestion
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install backend dependencies
        run: |
          pip install --upgrade pip
          pip install -r backend/requirements.txt
      
      - name: Ingest chapters to RAG
        run: python backend/ingest.py
        env:
          QDRANT_URL: ${{ secrets.QDRANT_URL }}
          QDRANT_API_KEY: ${{ secrets.QDRANT_API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
          cname: textbook.physical-ai.org

  api-deployment:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Deploy backend (if using Vercel)
        run: |
          npm install -g vercel
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

### 2.2 Environment Configuration

**File:** `.env.example`

```bash
# Qdrant Vector Database
QDRANT_URL=https://your-cluster-url.qdrant.io
QDRANT_API_KEY=your-api-key

# Neon PostgreSQL
DATABASE_URL=postgresql://user:password@neon.tech/textbook_rag

# OpenAI API
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4o-mini

# Backend Server
BACKEND_URL=https://physical-ai-rag.vercel.app
BACKEND_PORT=8000

# Frontend
REACT_APP_API_URL=https://physical-ai-rag.vercel.app/api
NODE_ENV=production
```

---

### 2.3 Git Configuration

**File:** `.gitignore`

```
# Dependencies
node_modules/
venv/
__pycache__/
*.pyc

# Environment
.env
.env.local
.env.*.local

# Build outputs
build/
dist/
.next/
out/
.docusaurus/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
.coverage
htmlcov/
.pytest_cache/

# Temporary
temp/
tmp/
*.tmp
```

---

### 2.4 Docusaurus Configuration

**File:** `docusaurus.config.ts`

```typescript
import {Config} from '@docusaurus/types';
import * as preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Essentials - An AI-native textbook with RAG chatbot',
  favicon: 'img/favicon.ico',
  url: 'https://org.github.io',
  baseUrl: '/physical-ai-textbook/',
  organizationName: 'org',
  projectName: 'physical-ai-textbook',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/org/physical-ai-textbook/tree/main/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/org/physical-ai-textbook/tree/main/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } as preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/textbook-social-card.jpg',
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          href: 'https://github.com/org/physical-ai-textbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Resources',
          items: [
            {
              label: 'Textbook',
              to: '/docs/intro',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/org/physical-ai-textbook',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. CC-BY-4.0 License.`,
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
    },
  } as any,

  plugins: [
    [
      'search-local',
      {
        language: ['en'],
        hashing: true,
        indexBlog: false,
      },
    ],
  ],
};

export default config;
```

---

### 2.5 Sidebar Navigation

**File:** `sidebars.ts`

```typescript
import type {SidebarsConfig} from '@docusaurus/types';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '📖 Introduction',
    },
    {
      type: 'category',
      label: '📚 Chapters',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'chapters/ch1-physical-ai',
          label: 'Chapter 1: Introduction to Physical AI',
        },
        {
          type: 'doc',
          id: 'chapters/ch2-humanoid-robotics',
          label: 'Chapter 2: Basics of Humanoid Robotics',
        },
        {
          type: 'doc',
          id: 'chapters/ch3-ros2',
          label: 'Chapter 3: ROS 2 Fundamentals',
        },
        {
          type: 'doc',
          id: 'chapters/ch4-digital-twin',
          label: 'Chapter 4: Digital Twin Simulation',
        },
        {
          type: 'doc',
          id: 'chapters/ch5-vla',
          label: 'Chapter 5: Vision-Language-Action Systems',
        },
        {
          type: 'doc',
          id: 'chapters/ch6-capstone',
          label: 'Chapter 6: Capstone Project',
        },
      ],
    },
  ],
};

export default sidebars;
```

---

### 2.6 Package Configuration

**File:** `package.json`

```json
{
  "name": "physical-ai-textbook",
  "version": "1.0.0",
  "description": "AI-native textbook with RAG chatbot for Physical AI and Humanoid Robotics",
  "private": true,
  "scripts": {
    "docusaurus": "docusaurus",
    "start": "docusaurus start",
    "build": "docusaurus build",
    "swizzle": "docusaurus swizzle",
    "deploy": "docusaurus deploy",
    "clear": "docusaurus clear",
    "serve": "docusaurus serve",
    "write-translations": "docusaurus write-translations",
    "write-heading-ids": "docusaurus write-heading-ids",
    "typecheck": "tsc",
    "lint": "eslint src --ext .ts,.tsx",
    "format": "prettier --write 'src/**/*.{ts,tsx,css}'"
  },
  "dependencies": {
    "@docusaurus/core": "^3.0.0",
    "@docusaurus/preset-classic": "^3.0.0",
    "@docusaurus/plugin-search-local": "^0.41.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "prism-react-renderer": "^2.1.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@docusaurus/types": "^3.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "prettier": "^3.0.0",
    "eslint": "^8.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0"
  },
  "engines": {
    "node": ">=18.0"
  }
}
```

---

## III. Phase 2: Content Creation Code (Weeks 2–4)

### 3.1 Textbook Introduction

**File:** `docs/intro.md`

```markdown
# Physical AI & Humanoid Robotics — Essentials

Welcome to a concise, AI-native textbook on Physical AI and Humanoid Robotics. This open-source resource is designed for beginners to intermediate learners interested in building intelligent robots.

## What is Physical AI?

Physical AI refers to artificial intelligence systems that can perceive, reason, and act in the physical world. Unlike purely digital AI, physical AI systems are embodied—they have sensors to perceive their environment and actuators to perform actions.

## Why Humanoid Robotics?

Humanoid robots offer a compelling testbed for physical AI research. With their two arms, two legs, and head, humanoid robots can interact with environments designed for humans, enabling practical applications in manufacturing, healthcare, and research.

## Textbook Structure

This textbook is organized into 6 chapters covering the essentials:

1. **Introduction to Physical AI** - Foundational concepts and scope
2. **Basics of Humanoid Robotics** - Robot anatomy and kinematics
3. **ROS 2 Fundamentals** - Robot Operating System basics
4. **Digital Twin Simulation** - Gazebo and physics-based simulation
5. **Vision-Language-Action Systems** - End-to-end AI for robotics
6. **Capstone Project** - Building a complete AI→Robot pipeline

## Interactive Learning

Each chapter includes:
- 📖 Comprehensive explanations (1,000–1,500 words)
- 🎨 Diagrams and visualizations
- 💻 Code examples and implementation tips
- 🤖 Practical AI applications
- ❓ Ask the AI Chatbot (bottom-right) for clarifications

## Getting Started

1. **Read Chapters** - Start with Chapter 1 and progress sequentially
2. **Ask Questions** - Use the chatbot (powered by RAG) to clarify concepts
3. **Code Along** - Try implementing examples from each chapter
4. **Build Capstone** - Create your own AI→Robot system in Chapter 6

## Free & Open-Source

This textbook is:
- 📖 Completely free
- 🔓 Open-source (CC-BY-4.0)
- 🤝 Community-driven
- 🚀 Continuously improved

## Who This Is For

- 👨‍💻 Computer science students
- 🤖 Robotics enthusiasts
- 🧠 AI researchers exploring embodied intelligence
- 💡 Engineers building physical systems

## Technology Stack

- **Frontend:** Docusaurus (React)
- **Textbook Hosting:** GitHub Pages
- **RAG Backend:** FastAPI + Qdrant + OpenAI
- **Deployment:** GitHub Actions + Vercel

---

**Ready to learn? Start with [Chapter 1: Introduction to Physical AI](/docs/chapters/ch1-physical-ai)**

**Questions? Ask the 💬 chatbot on any page!**
```

---

### 3.2 Chapter Template

**File:** `docs/chapters/TEMPLATE.md`

```markdown
# Chapter N: [Chapter Title]

**Learning Outcomes:**
After reading this chapter, you will understand:
- [ ] Learning outcome 1
- [ ] Learning outcome 2
- [ ] Learning outcome 3

---

## N.1 [Section Title]

[Content: 250-350 words explaining the concept clearly]

```python
# Code example (if applicable)
def example_function():
    """Brief docstring"""
    pass
```

**Key Concepts:**
- Concept 1: Definition
- Concept 2: Definition
- Concept 3: Definition

---

## N.2 [Section Title]

[Content: 250-350 words]

![Diagram Caption](../../../static/diagrams/chapter-N-diagram-1.svg)

---

## N.3 [Section Title]

[Content: 250-350 words]

---

## N.4 [Section Title]

[Content: 250-350 words]

---

## Summary

[1-2 paragraph summary of chapter key points]

## Next Steps

- Proceed to [Next Chapter] for [topic]
- Try implementing: [practical exercise]
- Explore: [external resource link]

## Further Reading

- Resource 1: [Link]
- Resource 2: [Link]

---

**Questions?** 💬 Ask the AI chatbot (bottom-right) for clarifications!
```

---

## IV. Phase 3: RAG Backend Code (Weeks 5–6)

### 4.1 FastAPI Main Application

**File:** `backend/app.py`

```python
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import psycopg2
from dotenv import load_dotenv
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI RAG Textbook",
    description="RAG-powered chatbot for Physical AI textbook",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Initialize clients
model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY')
)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database connection
def get_db():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    return conn

# Pydantic models
class QueryRequest(BaseModel):
    q: str = Query(..., max_length=500)
    difficulty: str = Query("normal", regex="^(basic|normal|advanced)$")
    role: str = Query("student", regex="^(student|educator|researcher)$")

class Source(BaseModel):
    chapter: int
    section: str
    quote: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    confidence: float

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Qdrant connection
        qdrant_client.get_collections()
        
        # Check PostgreSQL connection
        conn = get_db()
        conn.close()
        
        return {
            "status": "ok",
            "qdrant": "connected",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

# Main query endpoint
@app.post("/api/query", response_model=QueryResponse)
@limiter.limit("100/minute")
async def query_rag(request: QueryRequest):
    """
    RAG query endpoint
    
    Accepts a question and returns an answer grounded in the textbook,
    along with citations to specific chapters and sections.
    """
    try:
        # 1. Embed query
        logger.info(f"Processing query: {request.q[:50]}...")
        query_embedding = model.encode(request.q).tolist()
        
        # 2. Search Qdrant (top-3 chunks)
        search_results = qdrant_client.search(
            collection_name="textbook_chapters",
            query_vector=query_embedding,
            limit=3
        )
        
        if not search_results:
            return QueryResponse(
                answer="I couldn't find relevant information in the textbook. Please try a different question.",
                sources=[],
                confidence=0.0
            )
        
        # 3. Prepare context
        context = "\n".join([
            f"[Chapter {result.payload.get('chapter', 'N/A')}, Section: {result.payload.get('section', 'N/A')}]\n{result.payload.get('content', '')}"
            for result in search_results
        ])
        
        # 4. Generate response via OpenAI
        system_prompt = f"""You are a helpful textbook assistant for "Physical AI & Humanoid Robotics — Essentials".
        
Your role: {request.role}
Difficulty level: {request.difficulty}

IMPORTANT RULES:
1. Answer ONLY using the provided textbook excerpts below
2. If the information is not in the textbook, say so explicitly
3. Always cite your sources with chapter and section
4. Be concise (2-3 paragraphs maximum)
5. Use simple language for 'basic' difficulty, technical terms for 'advanced'

Textbook Excerpts:
{context}"""
        
        response = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.q}
            ],
            temperature=0.2,  # Low for deterministic responses
            max_tokens=500
        )
        
        answer = response.choices[0].message['content']
        
        # 5. Format response with citations
        sources = [
            Source(
                chapter=result.payload.get('chapter', 0),
                section=result.payload.get('section', 'Unknown'),
                quote=result.payload.get('content', '')[:200]
            )
            for result in search_results
        ]
        
        confidence = float(search_results[0].score) if search_results else 0.0
        
        # 6. Log to database
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO chat_sessions (query, response, confidence) VALUES (%s, %s, %s)",
            (request.q, answer, confidence)
        )
        conn.commit()
        conn.close()
        
        logger.info(f"Query processed successfully with confidence: {confidence:.2f}")
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# OpenAPI/Swagger documentation
@app.get("/api/docs", tags=["Documentation"])
async def api_docs():
    """API documentation"""
    return {
        "endpoints": {
            "POST /api/query": {
                "description": "Query the RAG system",
                "parameters": {
                    "q": "Question (max 500 chars)",
                    "difficulty": "basic|normal|advanced",
                    "role": "student|educator|researcher"
                },
                "returns": {
                    "answer": "Grounded response from textbook",
                    "sources": "List of citations",
                    "confidence": "Confidence score 0.0-1.0"
                }
            },
            "GET /health": {
                "description": "Health check"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### 4.2 Content Ingestion Script

**File:** `backend/ingest.py`

```python
import os
import re
import psycopg2
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY')
)
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Chunk text into overlapping segments
def chunk_text(text: str, chunk_size: int = 512, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks (by tokens, approximate)"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.split()) > 50:  # Only include substantial chunks
            chunks.append(chunk)
    
    return chunks

# Parse chapter Markdown
def parse_chapter(file_path: str, chapter_num: int) -> list[dict]:
    """Parse chapter Markdown and extract sections"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove frontmatter and metadata
    content = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    
    # Split by sections (##)
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    
    chunks_data = []
    
    for section in sections[1:]:  # Skip first split (before first ##)
        lines = section.split('\n', 1)
        section_title = lines[0].strip()
        section_content = lines[1] if len(lines) > 1 else ""
        
        # Remove code blocks, links, and images
        section_content = re.sub(r'```[\s\S]*?```', '', section_content)
        section_content = re.sub(r'\[.*?\]\(.*?\)', '', section_content)
        section_content = re.sub(r'!\[.*?\]\(.*?\)', '', section_content)
        
        # Chunk the section
        text_chunks = chunk_text(section_content, chunk_size=512)
        
        for chunk_text_content in text_chunks:
            chunks_data.append({
                'chapter': chapter_num,
                'section': section_title,
                'content': chunk_text_content
            })
    
    return chunks_data

# Create Qdrant collection (if not exists)
def create_qdrant_collection():
    """Create vector collection in Qdrant"""
    try:
        qdrant_client.get_collection("textbook_chapters")
        logger.info("Collection 'textbook_chapters' already exists")
    except:
        logger.info("Creating collection 'textbook_chapters'...")
        qdrant_client.create_collection(
            collection_name="textbook_chapters",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        logger.info("Collection created successfully")

# Ingest chapters
def ingest_chapters():
    """Ingest all chapters into Qdrant and PostgreSQL"""
    
    create_qdrant_collection()
    
    docs_dir = Path('./docs/chapters')
    point_id = 1
    total_chunks = 0
    
    # Process each chapter file
    chapter_files = sorted(docs_dir.glob('ch*.md'))
    
    for chapter_file in chapter_files:
        # Extract chapter number from filename
        match = re.search(r'ch(\d+)', chapter_file.name)
        if not match:
            continue
        
        chapter_num = int(match.group(1))
        logger.info(f"Processing Chapter {chapter_num}: {chapter_file.name}")
        
        # Parse and chunk chapter
        chunks = parse_chapter(str(chapter_file), chapter_num)
        
        for chunk in chunks:
            # Generate embedding
            embedding = model.encode(chunk['content']).tolist()
            
            # Store in PostgreSQL
            cur.execute(
                "INSERT INTO chunks (chapter, section, content, embedding_id) VALUES (%s, %s, %s, %s)",
                (chunk['chapter'], chunk['section'], chunk['content'], str(point_id))
            )
            
            # Store in Qdrant
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    'chapter': chunk['chapter'],
                    'section': chunk['section'],
                    'content': chunk['content']
                }
            )
            qdrant_client.upsert(
                collection_name="textbook_chapters",
                points=[point]
            )
            
            point_id += 1
            total_chunks += 1
            
            if total_chunks % 100 == 0:
                logger.info(f"Ingested {total_chunks} chunks...")
    
    conn.commit()
    logger.info(f"Ingestion complete: {total_chunks} chunks stored")

if __name__ == '__main__':
    ingest_chapters()
```

---

### 4.3 FastAPI Requirements

**File:** `backend/requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
openai==1.3.0
qdrant-client==2.7.0
sentence-transformers==2.2.2
psycopg2-binary==2.9.9
slowapi==0.1.9
pytest==7.4.3
httpx==0.25.2
```

---

## V. Phase 3b: Frontend React Components

### 5.1 Chatbot Widget

**File:** `src/components/ChatbotWidget.tsx`

```typescript
import React, { useState, useEffect, useRef } from 'react';
import styles from './ChatbotWidget.module.css';
import CitationBlock from './CitationBlock';

interface Source {
  chapter: number;
  section: string;
  quote: string;
}

interface QueryResponse {
  answer: string;
  sources: Source[];
  confidence: number;
}

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [difficulty, setDifficulty] = useState('normal');
  const [role, setRole] = useState('student');
  const [error, setError] = useState<string | null>(null);
  const responseRef = useRef<HTMLDivElement>(null);

  // Auto-focus on widget open
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Auto-scroll to response
  useEffect(() => {
    if (responseRef.current) {
      responseRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [response]);

  // Detect selected text
  useEffect(() => {
    const handleTextSelect = () => {
      if (!isOpen) {
        const selectedText = window.getSelection()?.toString();
        if (selectedText && selectedText.length > 10) {
          setQuery(selectedText);
          setIsOpen(true);
        }
      }
    };

    document.addEventListener('mouseup', handleTextSelect);
    return () => document.removeEventListener('mouseup', handleTextSelect);
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          q: query,
          difficulty,
          role,
        }),
      });

      if (!res.ok) {
        throw new Error(`API error: ${res.statusText}`);
      }

      const data: QueryResponse = await res.json();
      setResponse(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to get response. Please try again.'
      );
      console.error('Query error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      {/* Floating Button */}
      <button
        className={styles.floatingButton}
        onClick={() => setIsOpen(!isOpen)}
        title="Ask AI Chatbot"
        aria-label="Toggle chatbot"
      >
        💬
      </button>

      {/* Chatbot Popup */}
      {isOpen && (
        <div className={styles.popup}>
          <div className={styles.header}>
            <h3>AI Chatbot</h3>
            <button
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
              aria-label="Close chatbot"
            >
              ✕
            </button>
          </div>

          {/* Settings */}
          <div className={styles.settings}>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              aria-label="Select difficulty level"
            >
              <option value="basic">🟢 Basic</option>
              <option value="normal">🟡 Normal</option>
              <option value="advanced">🔴 Advanced</option>
            </select>

            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              aria-label="Select your role"
            >
              <option value="student">👨‍🎓 Student</option>
              <option value="educator">👨‍🏫 Educator</option>
              <option value="researcher">🔬 Researcher</option>
            </select>
          </div>

          {/* Query Input */}
          <form onSubmit={handleSubmit} className={styles.inputForm}>
            <textarea
              ref={inputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question about the textbook..."
              className={styles.input}
              disabled={loading}
              rows={2}
            />
            <button
              type="submit"
              className={styles.submitButton}
              disabled={loading || !query.trim()}
            >
              {loading ? '⏳ Thinking...' : '🚀 Ask'}
            </button>
          </form>

          {/* Error Message */}
          {error && (
            <div className={styles.error}>
              <p>⚠️ {error}</p>
            </div>
          )}

          {/* Response */}
          {response && (
            <div ref={responseRef} className={styles.response}>
              <div className={styles.answer}>
                <strong>💡 Answer:</strong>
                <p>{response.answer}</p>
              </div>

              {/* Confidence Indicator */}
              <div className={styles.confidence}>
                Confidence: {(response.confidence * 100).toFixed(0)}%
              </div>

              {/* Citations */}
              {response.sources.length > 0 && (
                <div className={styles.sources}>
                  <strong>📚 Sources:</strong>
                  {response.sources.map((source, idx) => (
                    <CitationBlock
                      key={idx}
                      chapter={source.chapter}
                      section={source.section}
                      quote={source.quote}
                    />
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

---

### 5.2 Chatbot Styles

**File:** `src/components/ChatbotWidget.module.css`

```css
.container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.floatingButton {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-size: 28px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.floatingButton:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.floatingButton:active {
  transform: scale(0.95);
}

.popup {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 360px;
  max-height: 600px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 40px rgba(0, 0, 0, 0.16);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .popup {
    background: #1e1e1e;
    color: #e0e0e0;
  }
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h3 {
  margin: 0;
  font-size: 16px;
}

.closeButton {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
}

.settings {
  padding: 12px;
  display: flex;
  gap: 8px;
}

.settings select {
  flex: 1;
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 12px;
}

.inputForm {
  padding: 12px;
  border-bottom: 1px solid #eee;
  display: flex;
  gap: 8px;
}

@media (prefers-color-scheme: dark) {
  .inputForm {
    border-bottom-color: #333;
  }
}

.input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 13px;
  resize: none;
}

.submitButton {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.submitButton:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 12px;
  margin: 0;
  font-size: 13px;
}

@media (prefers-color-scheme: dark) {
  .error {
    background: #2c1414;
    color: #ff6f6f;
  }
}

.response {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
}

.answer {
  margin-bottom: 16px;
  line-height: 1.5;
}

.answer p {
  margin: 8px 0 0 0;
  font-size: 13px;
}

.confidence {
  font-size: 11px;
  color: #666;
  margin-bottom: 12px;
}

@media (prefers-color-scheme: dark) {
  .confidence {
    color: #999;
  }
}

.sources {
  margin-top: 12px;
}

.sources strong {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
}

@media (max-width: 480px) {
  .popup {
    width: calc(100vw - 40px);
    max-height: 400px;
  }

  .container {
    bottom: 10px;
    right: 10px;
  }
}
```

---

### 5.3 Citation Component

**File:** `src/components/CitationBlock.tsx`

```typescript
import React from 'react';
import styles from './CitationBlock.module.css';

interface CitationBlockProps {
  chapter: number;
  section: string;
  quote: string;
}

export default function CitationBlock({
  chapter,
  section,
  quote,
}: CitationBlockProps) {
  return (
    <div className={styles.citation}>
      <div className={styles.header}>
        <span className={styles.chapter}>📖 Ch. {chapter}</span>
        <span className={styles.section}>{section}</span>
      </div>
      <blockquote className={styles.quote}>{quote}...</blockquote>
    </div>
  );
}
```

---

### 5.4 Citation Styles

**File:** `src/components/CitationBlock.module.css`

```css
.citation {
  background: #f5f5f5;
  border-left: 4px solid #667eea;
  padding: 12px;
  margin: 8px 0;
  border-radius: 4px;
  font-size: 12px;
}

@media (prefers-color-scheme: dark) {
  .citation {
    background: #2a2a2a;
    border-left-color: #764ba2;
  }
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-weight: 600;
}

.chapter {
  color: #667eea;
  font-weight: 700;
}

@media (prefers-color-scheme: dark) {
  .chapter {
    color: #9bb1ff;
  }
}

.section {
  color: #666;
  font-weight: 500;
  font-size: 11px;
}

@media (prefers-color-scheme: dark) {
  .section {
    color: #999;
  }
}

.quote {
  margin: 8px 0 0 0;
  font-style: italic;
  color: #444;
  line-height: 1.4;
}

@media (prefers-color-scheme: dark) {
  .quote {
    color: #bbb;
  }
}
```

---

## VI. Phase 4–5: Testing & Deployment Code

### 6.1 Integration Tests

**File:** `backend/tests/test_integration.py`

```python
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

client = TestClient(app)

class TestRAGIntegration:
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "qdrant" in data
        assert "database" in data
    
    def test_query_returns_valid_response(self):
        """Test query endpoint returns proper structure"""
        response = client.post(
            "/api/query",
            json={"q": "What is Physical AI?"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "answer" in data
        assert "sources" in data
        assert "confidence" in data
        
        # Check answer is non-empty
        assert len(data["answer"]) > 0
        
        # Check confidence is between 0 and 1
        assert 0 <= data["confidence"] <= 1
    
    def test_query_with_parameters(self):
        """Test query with difficulty and role parameters"""
        response = client.post(
            "/api/query",
            json={
                "q": "Define humanoid robotics",
                "difficulty": "advanced",
                "role": "researcher"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
    
    def test_invalid_difficulty_param(self):
        """Test rejection of invalid difficulty parameter"""
        response = client.post(
            "/api/query",
            json={
                "q": "What is ROS 2?",
                "difficulty": "invalid"
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_empty_query(self):
        """Test handling of empty query"""
        response = client.post(
            "/api/query",
            json={"q": ""}
        )
        assert response.status_code == 422  # Validation error
    
    def test_query_latency(self):
        """Test that queries complete within 1 second"""
        import time
        start = time.time()
        
        response = client.post(
            "/api/query",
            json={"q": "What is a digital twin?"}
        )
        
        elapsed = time.time() - start
        assert elapsed < 1.0, f"Query took {elapsed:.2f}s (limit: 1.0s)"
        assert response.status_code == 200
    
    def test_response_includes_citations(self):
        """Test that response includes proper citations"""
        response = client.post(
            "/api/query",
            json={"q": "Explain ROS 2 topics"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Check sources structure
        assert len(data["sources"]) > 0
        for source in data["sources"]:
            assert "chapter" in source
            assert "section" in source
            assert "quote" in source
            assert isinstance(source["chapter"], int)
            assert isinstance(source["section"], str)
            assert isinstance(source["quote"], str)

@pytest.mark.parametrize("difficulty", ["basic", "normal", "advanced"])
def test_all_difficulty_levels(difficulty):
    """Test query endpoint with all difficulty levels"""
    response = client.post(
        "/api/query",
        json={
            "q": "What is Physical AI?",
            "difficulty": difficulty
        }
    )
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

### 6.2 Style Guide

**File:** `STYLE_GUIDE.md`

```markdown
# Textbook Style Guide

## Writing Standards

### Tone & Voice
- **Audience:** Beginners to intermediate learners
- **Tone:** Friendly, clear, and encouraging
- **Voice:** Second person ("you") when appropriate
- **Avoid:** Jargon without explanation, overly academic language

### Structure
- **Chapter Length:** 1,000–1,500 words
- **Sections:** 3–4 per chapter
- **Headings:** Use H2 for sections (##), H3 for subsections (###)
- **Paragraphs:** Keep to 3–4 sentences max

### Technical Accuracy
- All technical concepts must be accurate and verifiable
- Include citations to external resources when needed
- Code examples must be functional and tested
- Diagrams must accurately represent concepts

### Code Examples
- Keep code snippets ≤ 20 lines
- Use Python or pseudocode for clarity
- Include comments for clarity
- Always include docstrings

### Formatting
- **Bold:** Concepts being introduced for first time
- **Italics:** Emphasis or foreign terms
- **Code blocks:** Use triple backticks with language tag
- **Lists:** Use bullet points (unordered) or numbered (ordered)

## Accessibility
- All images must have descriptive alt text
- Use semantic HTML
- Ensure color contrast ratios ≥ 4.5:1
- Avoid walls of text; use lists and spacing

## Learning Outcomes
- Each chapter must list 3–5 learning outcomes
- Use action verbs (understand, implement, analyze, etc.)
- State outcomes at top of chapter

## Diagrams
- Include 2–4 diagrams per chapter
- Use SVG format when possible
- Ensure captions are descriptive
- Provide alt text for accessibility

## References
- Link to authoritative sources
- Include full citations (title, author, year, URL)
- Mark links as external where appropriate
```

---

## VII. Deployment Instructions

### 7.1 Quick Start Guide

```bash
# 1. Clone repository
git clone https://github.com/org/physical-ai-textbook.git
cd physical-ai-textbook

# 2. Install Node.js dependencies
npm install

# 3. Create .env.local from .env.example
cp .env.example .env.local
# Edit .env.local with your credentials

# 4. Install Python dependencies (for backend)
pip install -r backend/requirements.txt

# 5. Run ingestion (populate Qdrant)
python backend/ingest.py

# 6. Start Docusaurus locally
npm start

# 7. In another terminal, start FastAPI backend
cd backend
uvicorn app:app --reload

# 8. Visit http://localhost:3000
```

### 7.2 Production Deployment

```bash
# Build Docusaurus
npm run build

# GitHub Actions automatically deploys to GitHub Pages
# on push to main branch

# Backend deployment (Vercel)
vercel deploy --prod
```

---

## VIII. File Inventory & Checklist

**Generated Code Files:**

- [ ] `.github/workflows/deploy.yml` - CI/CD pipeline
- [ ] `.env.example` - Environment template
- [ ] `.gitignore` - Git ignore rules
- [ ] `docusaurus.config.ts` - Docusaurus config
- [ ] `sidebars.ts` - Navigation structure
- [ ] `package.json` - Node dependencies
- [ ] `tsconfig.json` - TypeScript config
- [ ] `docs/intro.md` - Textbook introduction
- [ ] `docs/chapters/TEMPLATE.md` - Chapter template
- [ ] `backend/app.py` - FastAPI main app
- [ ] `backend/ingest.py` - Ingestion script
- [ ] `backend/requirements.txt` - Python deps
- [ ] `backend/tests/test_integration.py` - Tests
- [ ] `src/components/ChatbotWidget.tsx` - Widget
- [ ] `src/components/ChatbotWidget.module.css` - Styles
- [ ] `src/components/CitationBlock.tsx` - Citations
- [ ] `src/components/CitationBlock.module.css` - Citation styles
- [ ] `STYLE_GUIDE.md` - Writing standards
- [ ] `ARCHITECTURE.md` - System architecture
- [ ] `README.md` - Project overview

---

## IX. Next Steps

1. **Create GitHub Repository** - Follow Task 1.1.1
2. **Copy Code Files** - Use generated files above
3. **Configure Secrets** - Add API keys to GitHub
4. **Run Ingestion** - Populate vector database
5. **Deploy** - Push to main branch for auto-deploy
6. **Begin Content** - Start writing chapters

---

**Implementation Status:** ✅ Ready for Deployment  
**Code Generation Date:** 2025-12-05  
**Total Generated Files:** 20+  
**Total Lines of Code:** ~3,500+

**Next Command:** Begin executing Phase 1 tasks from tasks.md

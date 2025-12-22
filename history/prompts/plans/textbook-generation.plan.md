# Implementation Plan: Textbook Generation

**Feature:** Physical AI & Humanoid Robotics — Essentials Textbook + RAG Chatbot  
**Project:** textbook-generation  
**Created:** 2025-12-05  
**Status:** Active Implementation Planning  
**Objective:** Full, step-by-step execution plan for building production-ready AI textbook with integrated RAG system

---

## I. Executive Summary

This plan outlines the complete implementation roadmap for delivering:
1. **Docusaurus-based static textbook** (6 chapters, ~9,000 words total)
2. **RAG chatbot backend** (FastAPI + Qdrant + PostgreSQL)
3. **Integrated UI** (Select-to-ask widget, citations, dark mode)
4. **GitHub Pages deployment** (automated via GitHub Actions)
5. **Free-tier infrastructure** (zero cost for hosting, minimal API costs)

**Total Timeline:** 8 weeks (Phase 1 MVP)  
**Team Size:** 1 full-stack engineer + 1 content writer + 1 technical reviewer (part-time)  
**Success Metric:** All 6 chapters published, RAG chatbot operational with 100% citation accuracy

---

## II. Phase 1: Foundation & Setup (Week 1)

### 2.1 Repository & Environment Setup

#### Task 1.1: Create GitHub Repository
**Objective:** Initialize project repository with proper structure and CI/CD pipeline

**Steps:**
1. Create GitHub repository: `physical-ai-textbook`
2. Configure repository settings:
   - Enable GitHub Pages (publish from `/build` or `/docs` folder)
   - Set main branch as default
   - Enable branch protection (require PR reviews)
   - Configure GitHub Actions permissions
3. Clone locally and initialize git submodules (if external code examples needed)
4. Create `.gitignore`:
   ```
   node_modules/
   .env.local
   .env.*.local
   dist/
   build/
   .docusaurus/
   *.log
   .DS_Store
   ```

**Acceptance Criteria:**
- [ ] Repository created and publicly accessible
- [ ] GitHub Pages enabled and configuration saved
- [ ] Branch protection rules enforced
- [ ] `.gitignore` prevents accidental commits of node_modules, env files

**Estimated Effort:** 30 minutes  
**Owner:** DevOps Engineer

---

#### Task 1.2: Initialize Docusaurus Project
**Objective:** Set up Docusaurus v3 with clean configuration, minimal dependencies

**Steps:**
1. Create Docusaurus project:
   ```bash
   npx create-docusaurus@latest physical-ai-textbook classic --typescript
   ```
2. Install additional dependencies:
   ```bash
   npm install docusaurus-plugin-search-local --save
   npm install @docusaurus/preset-classic --save
   ```
3. Configure `docusaurus.config.js`:
   - Set title: "Physical AI & Humanoid Robotics — Essentials"
   - Set URL: GitHub Pages URL (e.g., `https://org.github.io/physical-ai-textbook/`)
   - Enable dark mode toggle
   - Configure search plugin
   - Set up navbar links (Textbook, GitHub, Chat)
4. Configure `sidebars.js`:
   ```javascript
   module.exports = {
     docsSidebar: [
       { type: 'doc', id: 'intro', label: 'Introduction' },
       {
         type: 'category',
         label: 'Chapters',
         items: [
           'chapters/ch1-physical-ai',
           'chapters/ch2-humanoid-robotics',
           'chapters/ch3-ros2',
           'chapters/ch4-digital-twin',
           'chapters/ch5-vla',
           'chapters/ch6-capstone',
         ],
       },
     ],
   };
   ```
5. Test build:
   ```bash
   npm run build
   npm run start
   ```

**Acceptance Criteria:**
- [ ] Docusaurus build succeeds without errors
- [ ] Local server runs on localhost:3000 without crashes
- [ ] Sidebar navigation structure is correct
- [ ] Dark/light mode toggle functional
- [ ] Search plugin enabled

**Estimated Effort:** 1 hour  
**Owner:** Frontend Engineer

---

#### Task 1.3: Set Up GitHub Actions Workflow
**Objective:** Automate build and deployment pipeline

**Steps:**
1. Create `.github/workflows/deploy.yml`:
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
         - uses: actions/checkout@v3
         
         - name: Setup Node.js
           uses: actions/setup-node@v3
           with:
             node-version: '18'
             cache: 'npm'
         
         - name: Install dependencies
           run: npm ci
         
         - name: Build
           run: npm run build
         
         - name: Test build output
           run: test -d build && echo "Build successful"
         
         - name: Deploy to GitHub Pages
           if: github.ref == 'refs/heads/main'
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./build
             cname: textbook.physical-ai.org  # Optional custom domain
   ```
2. Test workflow by pushing dummy commit
3. Verify GitHub Actions logs for successful build and deployment

**Acceptance Criteria:**
- [ ] Workflow file properly formatted (no syntax errors)
- [ ] Workflow triggers on main branch push
- [ ] Build completes in < 30 seconds
- [ ] Deployment to GitHub Pages succeeds
- [ ] Public URL accessible after deploy

**Estimated Effort:** 1 hour  
**Owner:** DevOps Engineer

---

#### Task 1.4: Set Up Environment Variables & Secrets
**Objective:** Configure secrets for API keys, database credentials

**Steps:**
1. Create `.env.example` (no secrets):
   ```
   QDRANT_URL=https://your-qdrant-instance.com
   QDRANT_API_KEY=<placeholder>
   DATABASE_URL=postgresql://user:pass@neon-endpoint.com/db
   OPENAI_API_KEY=<placeholder>
   ```
2. Add GitHub Secrets:
   - Go to Settings → Secrets and variables → Actions
   - Add: `QDRANT_API_KEY`
   - Add: `DATABASE_URL`
   - Add: `OPENAI_API_KEY`
3. Update GitHub Actions workflow to use secrets:
   ```yaml
   - name: Deploy Backend
     env:
       QDRANT_API_KEY: ${{ secrets.QDRANT_API_KEY }}
       DATABASE_URL: ${{ secrets.DATABASE_URL }}
       OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
     run: npm run deploy:backend
   ```

**Acceptance Criteria:**
- [ ] `.env.example` documents all required variables
- [ ] Secrets added to GitHub (no accidental exposure in logs)
- [ ] GitHub Actions can access secrets during build

**Estimated Effort:** 30 minutes  
**Owner:** DevOps Engineer

---

### 2.2 Infrastructure Provisioning

#### Task 1.5: Set Up Qdrant Cloud Instance
**Objective:** Provision vector database for RAG embeddings

**Steps:**
1. Sign up for Qdrant Cloud (free tier): https://cloud.qdrant.io
2. Create cluster:
   - Name: `physical-ai-textbook-prod`
   - Tier: Free tier
   - Region: US-East (or closest to deployment)
3. Get cluster credentials:
   - Cluster URL (e.g., `https://xxx-qdrant.a.run.app`)
   - API Key (auto-generated)
4. Save credentials in GitHub Secrets
5. Test connection from local machine:
   ```python
   from qdrant_client import QdrantClient
   client = QdrantClient(url="<cluster-url>", api_key="<api-key>")
   print(client.get_collections())
   ```

**Acceptance Criteria:**
- [ ] Qdrant cluster created and accessible
- [ ] API credentials saved securely
- [ ] Connection test successful
- [ ] Free-tier limits documented (1GB storage, 10K requests/month)

**Estimated Effort:** 30 minutes  
**Owner:** DevOps Engineer

---

#### Task 1.6: Set Up Neon PostgreSQL Instance
**Objective:** Provision metadata database for RAG system

**Steps:**
1. Sign up for Neon PostgreSQL (free tier): https://neon.tech
2. Create project:
   - Name: `physical-ai-textbook`
   - Region: US-East
3. Create database:
   - Database name: `textbook_rag`
4. Get connection string (PostgreSQL URL)
5. Create initial schema:
   ```sql
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
   ```
6. Test connection:
   ```bash
   psql "<DATABASE_URL>"
   ```

**Acceptance Criteria:**
- [ ] PostgreSQL database created
- [ ] Connection string obtained and saved
- [ ] Schema tables created successfully
- [ ] Indexes created for performance

**Estimated Effort:** 45 minutes  
**Owner:** DevOps Engineer

---

#### Task 1.7: Provision FastAPI Backend Server
**Objective:** Set up backend for RAG processing

**Steps:**
1. Choose deployment platform (free tier):
   - **Option A:** Vercel (Node.js + Python support)
   - **Option B:** Railway (more free credits, simpler Python deployment)
   - **Option C:** Render (free tier with 15-min timeout limit)
2. Create FastAPI application skeleton:
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(title="Physical AI RAG Textbook")
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
       allow_headers=["*"],
   )
   
   @app.get("/health")
   def health():
       return {"status": "ok"}
   
   @app.post("/api/query")
   def query(q: str, difficulty: str = "normal"):
       # RAG logic here
       return {"answer": "...", "sources": [...]}
   ```
3. Deploy to chosen platform and get public URL
4. Test endpoint: `curl https://your-app.vercel.app/health`

**Acceptance Criteria:**
- [ ] FastAPI app deployed on free-tier server
- [ ] Health check endpoint responds with 200 OK
- [ ] CORS configured for Docusaurus domain
- [ ] Public URL accessible

**Estimated Effort:** 1 hour  
**Owner:** Backend Engineer

---

**Week 1 Deliverables:**
✅ GitHub repository with CI/CD pipeline configured  
✅ Docusaurus project initialized and building  
✅ Qdrant Cloud + Neon PostgreSQL provisioned  
✅ FastAPI backend server deployed  
✅ All infrastructure on free-tier services  

---

## III. Phase 2: Content Creation (Weeks 2–4)

### 3.1 Chapter Writing & Review Workflow

#### Task 2.1: Content Planning & Outline
**Objective:** Define detailed outline for all 6 chapters

**Steps:**
1. Create outline document (`CONTENT_OUTLINE.md`):
   ```markdown
   # Physical AI & Humanoid Robotics — Essentials
   
   ## Chapter 1: Introduction to Physical AI
   - Section 1.1: Definition and scope (300 words)
   - Section 1.2: Classical vs. Physical AI (300 words)
   - Section 1.3: Real-world examples (400 words)
   - Section 1.4: Why embodiment matters (300 words)
   [... and so on]
   ```
2. Assign 1,000–1,500 word target per chapter
3. Identify 2–4 diagrams needed per chapter
4. Draft code examples (≤ 20 lines each)
5. Get approval from technical reviewer

**Acceptance Criteria:**
- [ ] Outline covers all 6 chapters
- [ ] Word count target realistic and approved
- [ ] Diagram placeholders identified
- [ ] Code examples planned

**Estimated Effort:** 2 hours  
**Owner:** Content Lead + Technical Reviewer

---

#### Task 2.2: Write Chapter 1 — Introduction to Physical AI
**Objective:** Write and review first chapter

**Steps:**
1. Write draft in Markdown format (`docs/chapters/ch1-physical-ai.md`)
2. Include:
   - 4 sections (1,000–1,500 words total)
   - 2–4 diagrams (Mermaid or PNG)
   - Learning outcomes (3–5 bullet points)
   - 1 code example or conceptual diagram
3. Peer review checklist:
   - [ ] Word count within 1,000–1,500 range
   - [ ] All sections well-structured
   - [ ] Diagrams accurate and captioned
   - [ ] Technical accuracy verified
   - [ ] Accessibility (WCAG 2.1 AA)
   - [ ] No external knowledge required for understanding
4. Integrate into Docusaurus and build test

**Acceptance Criteria:**
- [ ] Chapter written and reviewed
- [ ] Docusaurus build succeeds with chapter included
- [ ] Chapter renders correctly on GitHub Pages test deployment
- [ ] All diagrams display properly

**Estimated Effort:** 6 hours (writing) + 2 hours (review)  
**Owner:** Content Writer + Technical Reviewer

---

#### Task 2.3–2.8: Write Chapters 2–6
**Objective:** Replicate Chapter 1 process for remaining 5 chapters

**Steps:**
- Repeat Task 2.2 for each chapter
- Maintain consistent style and formatting
- Build and test after each chapter

**Timeline:**
- Chapter 2 (Humanoid Robotics): Week 2
- Chapter 3 (ROS 2): Week 2–3
- Chapter 4 (Digital Twin): Week 3
- Chapter 5 (VLA): Week 3–4
- Chapter 6 (Capstone): Week 4

**Acceptance Criteria:**
- [ ] All 6 chapters written, reviewed, and integrated
- [ ] Docusaurus build succeeds with all chapters
- [ ] Full site accessible on test deployment
- [ ] Word count: ~9,000 total words (6 chapters × 1,500 words avg)

**Estimated Effort:** 30 hours writing + 10 hours review (shared among team)  
**Owner:** Content Writer + Technical Reviewer

---

### 3.2 Diagram Creation

#### Task 2.9: Create Diagrams for All Chapters
**Objective:** Develop visual aids for all 6 chapters

**Diagrams Needed:**

| Chapter | Diagram 1 | Diagram 2 | Diagram 3 | Diagram 4 |
|---------|-----------|-----------|-----------|-----------|
| Ch1 | Classical vs Physical AI | Real-world applications | — | — |
| Ch2 | Robot anatomy (joints, DOF) | Sensor/actuator placement | — | — |
| Ch3 | ROS 2 pub/sub architecture | Service/action call flow | — | — |
| Ch4 | Digital twin workflow | Gazebo plugin architecture | — | — |
| Ch5 | VLA perception-action loop | VLM inference pipeline | — | — |
| Ch6 | Full pipeline architecture | Hardware deployment workflow | — | — |

**Steps:**
1. Choose diagram tools:
   - **Mermaid (preferred):** Flowcharts, architecture diagrams (auto-rendered in Docusaurus)
   - **Lucidchart:** Complex diagrams (export as PNG/SVG)
   - **Excalidraw:** Hand-drawn style technical diagrams
2. Create all diagrams in vector format (SVG preferred, PNG acceptable)
3. Optimize images (< 200KB each)
4. Add alt text and captions to all diagrams
5. Store in `static/diagrams/` folder

**Acceptance Criteria:**
- [ ] All 12–16 diagrams created
- [ ] SVG or optimized PNG format
- [ ] Alt text on all diagrams
- [ ] Diagrams render correctly in Docusaurus

**Estimated Effort:** 4 hours  
**Owner:** Technical Illustrator / Content Writer

---

**Phase 2 Deliverables:**
✅ All 6 chapters written (~9,000 words)  
✅ All chapters peer-reviewed for accuracy  
✅ 12–16 diagrams created and integrated  
✅ Docusaurus site builds successfully with all content  

---

## IV. Phase 3: RAG Backend Implementation (Week 5–6)

### 4.1 Ingestion Pipeline

#### Task 3.1: Build Content Ingestion Script
**Objective:** Parse chapters and convert to searchable chunks

**Steps:**
1. Create `ingest.py` script:
   ```python
   import os
   import json
   from pathlib import Path
   from sentence_transformers import SentenceTransformer
   from qdrant_client import QdrantClient
   from qdrant_client.http.models import Distance, VectorParams, PointStruct
   import psycopg2
   
   def chunk_text(text: str, chunk_size: int = 512) -> list[str]:
       """Split text into overlapping chunks"""
       words = text.split()
       chunks = []
       for i in range(0, len(words), chunk_size):
           chunk = ' '.join(words[i:i+chunk_size])
           chunks.append(chunk)
       return chunks
   
   def ingest_chapters(docs_dir: str):
       # Initialize clients
       model = SentenceTransformer('all-MiniLM-L6-v2')
       qdrant = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
       conn = psycopg2.connect(os.getenv('DATABASE_URL'))
       cur = conn.cursor()
       
       # Iterate through chapters
       for chapter_file in Path(docs_dir).glob('chapters/*.md'):
           chapter_num = int(chapter_file.stem.split('-')[0])
           with open(chapter_file) as f:
               content = f.read()
           
           # Parse sections
           sections = content.split('##')
           for section in sections:
               chunks = chunk_text(section, chunk_size=512)
               for chunk in chunks:
                   # Generate embedding
                   embedding = model.encode(chunk)
                   
                   # Store in PostgreSQL
                   cur.execute(
                       "INSERT INTO chunks (chapter, section, content, embedding_id) VALUES (%s, %s, %s, %s)",
                       (chapter_num, section[:50], chunk, str(len(chunks)))
                   )
                   
                   # Store in Qdrant
                   # (implementation details...)
       
       conn.commit()
       conn.close()
       print(f"Ingested {len(chunks)} chunks successfully")
   
   if __name__ == '__main__':
       ingest_chapters('./docs')
   ```
2. Test ingestion locally:
   ```bash
   python ingest.py
   ```
3. Verify chunks in Qdrant and PostgreSQL

**Acceptance Criteria:**
- [ ] Script parses all 6 chapters
- [ ] Chunks created (target: ≤ 2,000 total)
- [ ] Embeddings generated using all-MiniLM-L6-v2
- [ ] Data stored in Qdrant + PostgreSQL
- [ ] Duplicate detection prevents re-ingestion

**Estimated Effort:** 4 hours  
**Owner:** Backend Engineer

---

#### Task 3.2: Integrate Ingestion into GitHub Actions
**Objective:** Automate ingestion on deployment

**Steps:**
1. Update `.github/workflows/deploy.yml`:
   ```yaml
   - name: Ingest chapters to RAG
     if: github.ref == 'refs/heads/main'
     run: |
       pip install -r backend/requirements.txt
       python backend/ingest.py
     env:
       QDRANT_URL: ${{ secrets.QDRANT_URL }}
       QDRANT_API_KEY: ${{ secrets.QDRANT_API_KEY }}
       DATABASE_URL: ${{ secrets.DATABASE_URL }}
   ```
2. Test workflow by pushing update to main branch

**Acceptance Criteria:**
- [ ] GitHub Actions workflow includes ingestion step
- [ ] Ingestion runs on main branch push
- [ ] Workflow logs show successful ingestion

**Estimated Effort:** 1 hour  
**Owner:** DevOps Engineer

---

### 4.2 RAG Query Endpoint

#### Task 3.3: Implement RAG Query Endpoint
**Objective:** Build FastAPI endpoint for Q&A

**Steps:**
1. Update `backend/app.py`:
   ```python
   from fastapi import FastAPI
   from sentence_transformers import SentenceTransformer
   from qdrant_client import QdrantClient
   import openai
   
   app = FastAPI()
   model = SentenceTransformer('all-MiniLM-L6-v2')
   qdrant = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
   
   @app.post("/api/query")
   async def query(q: str, difficulty: str = "normal", role: str = "student"):
       # 1. Embed query
       query_embedding = model.encode(q)
       
       # 2. Search Qdrant (top-3 chunks)
       search_results = qdrant.search(
           collection_name="textbook_chapters",
           query_vector=query_embedding,
           limit=3
       )
       
       # 3. Prepare context
       context = "\n".join([result.payload['content'] for result in search_results])
       
       # 4. Generate response via OpenAI
       system_prompt = f"You are a textbook assistant. Answer ONLY using the provided textbook excerpts. Role: {role}, Difficulty: {difficulty}"
       response = openai.ChatCompletion.create(
           model="gpt-4o-mini",
           messages=[
               {"role": "system", "content": system_prompt + f"\n\nTextbook Excerpts:\n{context}"},
               {"role": "user", "content": q}
           ],
           temperature=0.2  # Low temperature for deterministic responses
       )
       
       # 5. Format response with citations
       answer = response.choices[0].message['content']
       sources = [
           {
               "chapter": result.payload['chapter'],
               "section": result.payload['section'],
               "quote": result.payload['content'][:200]
           }
           for result in search_results
       ]
       
       return {
           "answer": answer,
           "sources": sources,
           "confidence": search_results[0].score if search_results else 0
       }
   
   @app.get("/health")
   def health():
       return {"status": "ok", "qdrant": "connected", "db": "connected"}
   ```
2. Test locally:
   ```bash
   curl -X POST http://localhost:8000/api/query?q="What is a digital twin?"
   ```

**Acceptance Criteria:**
- [ ] `/api/query` endpoint accepts POST requests
- [ ] Query embedded and Qdrant search succeeds
- [ ] LLM generates response from context
- [ ] Response includes citations (chapter, section, quote)
- [ ] Response latency < 1 second

**Estimated Effort:** 3 hours  
**Owner:** Backend Engineer

---

#### Task 3.4: Add RAG Validation & Constraints
**Objective:** Ensure chatbot only answers from textbook

**Steps:**
1. Implement response validation:
   ```python
   def validate_response(response: str, context: str) -> bool:
       """Check if response references only the provided context"""
       # Extract key terms from context
       context_terms = set(word.lower() for word in context.split())
       
       # Check if response uses context terms
       response_terms = set(word.lower() for word in response.split())
       overlap = len(response_terms & context_terms)
       
       # Simple heuristic: if < 30% overlap, likely hallucination
       return overlap / len(response_terms) > 0.3 if response_terms else False
   
   @app.post("/api/query")
   async def query(q: str, ...):
       # ... existing code ...
       
       is_valid = validate_response(answer, context)
       if not is_valid:
           answer = "This topic requires more context from the textbook. Please try a different question."
       
       return {...}
   ```
2. Test with known hallucination-prone queries
3. Monitor responses for quality

**Acceptance Criteria:**
- [ ] Validation logic prevents obvious hallucinations
- [ ] Out-of-scope queries return appropriate message
- [ ] Manual audit confirms 100% accuracy on sample queries

**Estimated Effort:** 2 hours  
**Owner:** Backend Engineer

---

### 4.3 Frontend Integration

#### Task 3.5: Create RAG Widget Component
**Objective:** Build "Select text → Ask AI" UI widget

**Steps:**
1. Create `src/components/ChatbotWidget.tsx`:
   ```typescript
   import React, { useState } from 'react';
   import styles from './ChatbotWidget.module.css';
   
   export default function ChatbotWidget() {
     const [isOpen, setIsOpen] = useState(false);
     const [query, setQuery] = useState('');
     const [response, setResponse] = useState(null);
     const [loading, setLoading] = useState(false);
   
     const handleTextSelect = () => {
       const selectedText = window.getSelection()?.toString();
       if (selectedText) {
         setQuery(selectedText);
         setIsOpen(true);
       }
     };
   
     const handleSubmit = async () => {
       setLoading(true);
       const res = await fetch('/api/query', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ q: query }),
       });
       const data = await res.json();
       setResponse(data);
       setLoading(false);
     };
   
     return (
       <div className={styles.widget}>
         <button onClick={() => setIsOpen(!isOpen)}>💬 Ask AI</button>
         {isOpen && (
           <div className={styles.popup}>
             <input
               value={query}
               onChange={(e) => setQuery(e.target.value)}
               placeholder="Ask a question..."
             />
             <button onClick={handleSubmit} disabled={loading}>
               {loading ? 'Thinking...' : 'Submit'}
             </button>
             {response && (
               <div className={styles.response}>
                 <p><strong>Answer:</strong> {response.answer}</p>
                 <p><strong>Sources:</strong></p>
                 {response.sources.map((src, i) => (
                   <div key={i} className={styles.citation}>
                     <p>Ch. {src.chapter}, {src.section}</p>
                     <p>"{src.quote}..."</p>
                   </div>
                 ))}
               </div>
             )}
           </div>
         )}
       </div>
     );
   }
   ```
2. Add to Docusaurus layout (all pages)
3. Style with CSS (`src/components/ChatbotWidget.module.css`)
4. Test widget functionality

**Acceptance Criteria:**
- [ ] Widget appears on all pages
- [ ] Text selection triggers widget
- [ ] Query submission works
- [ ] Response displays with citations
- [ ] Widget dismissible

**Estimated Effort:** 2 hours  
**Owner:** Frontend Engineer

---

#### Task 3.6: Add Citation Block Component
**Objective:** Display source references with formatting

**Steps:**
1. Create `src/components/CitationBlock.tsx`:
   ```typescript
   export default function CitationBlock({ chapter, section, quote }) {
     return (
       <div className={styles.citation}>
         <div className={styles.header}>
           <span className={styles.chapter}>Chapter {chapter}</span>
           <span className={styles.section}>{section}</span>
         </div>
         <blockquote>{quote}</blockquote>
       </div>
     );
   }
   ```
2. Style with professional citation formatting
3. Test rendering in response display

**Acceptance Criteria:**
- [ ] Citation block displays chapter and section
- [ ] Quote text properly formatted
- [ ] Styling matches textbook theme

**Estimated Effort:** 1 hour  
**Owner:** Frontend Engineer

---

**Phase 3 Deliverables:**
✅ RAG ingestion pipeline fully automated  
✅ Query endpoint returns grounded answers with citations  
✅ Chatbot widget integrated into Docusaurus  
✅ Citation display formatted and accessible  

---

## V. Phase 4: Integration & Testing (Week 7)

### 5.1 End-to-End Testing

#### Task 4.1: Integration Testing
**Objective:** Verify full pipeline works: textbook → ingestion → RAG → response

**Steps:**
1. Create test suite (`tests/test_integration.py`):
   ```python
   import pytest
   
   @pytest.fixture
   def client():
       from backend.app import app
       return app.test_client()
   
   def test_query_returns_valid_response(client):
       response = client.post('/api/query', json={'q': 'What is Physical AI?'})
       assert response.status_code == 200
       data = response.get_json()
       assert 'answer' in data
       assert 'sources' in data
       assert len(data['sources']) > 0
   
   def test_response_includes_citations(client):
       response = client.post('/api/query', json={'q': 'Define humanoid robotics'})
       data = response.get_json()
       for source in data['sources']:
           assert 'chapter' in source
           assert 'section' in source
           assert 'quote' in source
   
   def test_out_of_scope_query(client):
       response = client.post('/api/query', json={'q': 'What is quantum computing?'})
       data = response.get_json()
       assert 'not covered' in data['answer'].lower()
   
   def test_response_latency(client):
       import time
       start = time.time()
       client.post('/api/query', json={'q': 'ROS 2 topics'})
       elapsed = time.time() - start
       assert elapsed < 1.0  # < 1 second
   ```
2. Run tests:
   ```bash
   pytest tests/test_integration.py -v
   ```

**Acceptance Criteria:**
- [ ] All integration tests pass
- [ ] Query latency consistently < 1 second
- [ ] Responses always include citations
- [ ] Out-of-scope queries handled gracefully

**Estimated Effort:** 2 hours  
**Owner:** QA Engineer

---

#### Task 4.2: Accuracy Audit (Manual)
**Objective:** Manually verify 20 sample queries return correct answers

**Steps:**
1. Create test queries file (`tests/sample_queries.txt`):
   ```
   What is Physical AI?
   Define humanoid robotics
   What is ROS 2?
   Explain digital twins
   What are VLMs?
   What is the capstone project?
   [... 14 more queries ...]
   ```
2. Submit each query to chatbot
3. Verify response:
   - [ ] Answer is accurate and relevant
   - [ ] Citation includes correct chapter/section
   - [ ] Quote text matches source
   - [ ] No hallucinations detected
4. Document results in audit spreadsheet

**Acceptance Criteria:**
- [ ] 20/20 queries return accurate answers
- [ ] 20/20 citations verified correct
- [ ] 0/20 hallucinations detected
- [ ] Audit documented in `tests/AUDIT_REPORT.md`

**Estimated Effort:** 2 hours  
**Owner:** Technical Reviewer

---

### 5.2 Performance & Accessibility Testing

#### Task 4.3: Performance Audit
**Objective:** Verify all performance targets met

**Steps:**
1. Build site and run Lighthouse audit:
   ```bash
   npm run build
   npx lighthouse https://physical-ai-textbook.github.io --view
   ```
2. Check metrics:
   - [ ] Page load < 2 seconds
   - [ ] Lighthouse score ≥ 90
   - [ ] First Contentful Paint < 1.5s
   - [ ] Cumulative Layout Shift < 0.1
3. Test on slow 3G network (Chrome DevTools)
4. Measure RAG query latency (target: < 1 second)

**Acceptance Criteria:**
- [ ] Lighthouse score ≥ 90 on all pages
- [ ] Page load < 2 seconds (measured)
- [ ] RAG queries < 1 second (99th percentile)
- [ ] Mobile performance acceptable

**Estimated Effort:** 2 hours  
**Owner:** DevOps Engineer

---

#### Task 4.4: Accessibility Audit (WCAG 2.1 AA)
**Objective:** Verify compliance with accessibility standards

**Steps:**
1. Run automated accessibility scan:
   ```bash
   npx axe-core-automated-testing
   ```
2. Manual checks:
   - [ ] Keyboard navigation works (Tab, Enter, Escape)
   - [ ] Screen reader compatible (test with NVDA or JAWS)
   - [ ] Color contrast ratios ≥ 4.5:1 for text
   - [ ] All images have alt text
   - [ ] Heading hierarchy is semantic (H1 → H2 → H3)
   - [ ] Form inputs have labels
3. Test with multiple browsers (Chrome, Firefox, Safari, Edge)

**Acceptance Criteria:**
- [ ] Zero automated accessibility violations
- [ ] Keyboard navigation fully functional
- [ ] Screen reader compatible
- [ ] All color contrast ratios meet WCAG AA
- [ ] Mobile accessibility verified

**Estimated Effort:** 3 hours  
**Owner:** QA Engineer + Accessibility Specialist

---

### 5.3 Security & Infrastructure Testing

#### Task 4.5: Security Hardening
**Objective:** Implement security best practices

**Steps:**
1. Add rate limiting to API:
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   
   @app.post("/api/query")
   @limiter.limit("100/minute")
   async def query(...):
       ...
   ```
2. Input validation:
   ```python
   from pydantic import BaseModel
   
   class Query(BaseModel):
       q: str = Field(..., max_length=500)
       difficulty: str = Field("normal", regex="^(basic|normal|advanced)$")
   ```
3. Enable HTTPS only (GitHub Pages auto-enabled)
4. Add security headers:
   ```python
   @app.middleware("http")
   async def add_security_headers(request: Request, call_next):
       response = await call_next(request)
       response.headers["X-Content-Type-Options"] = "nosniff"
       response.headers["X-Frame-Options"] = "DENY"
       return response
   ```
5. Scan for dependencies vulnerabilities:
   ```bash
   npm audit
   pip install safety && safety check
   ```

**Acceptance Criteria:**
- [ ] Rate limiting prevents abuse
- [ ] Input validation rejects malformed queries
- [ ] Security headers present
- [ ] No high-severity vulnerabilities
- [ ] HTTPS enforced

**Estimated Effort:** 2 hours  
**Owner:** Backend Engineer + Security Lead

---

#### Task 4.6: Infrastructure Resilience Testing
**Objective:** Test failure scenarios and recovery

**Steps:**
1. Test Qdrant failover:
   - Simulate Qdrant outage
   - Verify graceful error message to user
   - Confirm fallback to keyword search works
2. Test database failover:
   - Simulate PostgreSQL connection loss
   - Verify connection pooling retry works
3. Test LLM API failover:
   - Simulate OpenAI API timeout
   - Verify fallback response generated
4. Load testing:
   ```bash
   pip install locust
   # Create locustfile.py with load scenarios
   locust -f locustfile.py
   ```

**Acceptance Criteria:**
- [ ] System gracefully handles service outages
- [ ] Fallback mechanisms trigger appropriately
- [ ] Error messages helpful to users
- [ ] Recovers automatically when services restore

**Estimated Effort:** 2 hours  
**Owner:** DevOps Engineer + Backend Engineer

---

**Phase 4 Deliverables:**
✅ Full end-to-end integration tested  
✅ RAG accuracy audited (100%)  
✅ Performance targets verified  
✅ Accessibility WCAG 2.1 AA compliant  
✅ Security hardened  

---

## VI. Phase 5: Launch & Monitoring (Week 8)

### 6.1 Pre-Launch Checklist

#### Task 5.1: Final Content Review
**Objective:** Last verification before public launch

**Checklist:**
- [ ] All 6 chapters accurate and reviewed
- [ ] All diagrams present and captioned
- [ ] All code examples tested
- [ ] No broken links (internal or external)
- [ ] Spelling/grammar checked
- [ ] Technical terms consistent across chapters
- [ ] References and citations complete

**Estimated Effort:** 2 hours  
**Owner:** Content Lead + Technical Reviewer

---

#### Task 5.2: Infrastructure Readiness Check
**Objective:** Verify all services operational

**Checklist:**
- [ ] GitHub Pages deployment successful
- [ ] Docusaurus build < 30 seconds
- [ ] RAG backend API responding
- [ ] Qdrant cluster healthy (≤ 2,000 chunks)
- [ ] PostgreSQL database accessible
- [ ] GitHub Actions workflow passing
- [ ] Monitoring/logging enabled
- [ ] Backup procedures documented

**Estimated Effort:** 1 hour  
**Owner:** DevOps Engineer

---

#### Task 5.3: Documentation Review
**Objective:** Verify user-facing and developer documentation

**Checklist:**
- [ ] README.md complete with setup instructions
- [ ] CONTRIBUTING.md guides contributors
- [ ] API documentation (OpenAPI schema)
- [ ] Architecture documentation (`ARCHITECTURE.md`)
- [ ] Deployment guide
- [ ] Troubleshooting guide

**Estimated Effort:** 1 hour  
**Owner:** Technical Writer

---

### 6.2 Launch & Announcement

#### Task 5.4: Public Launch
**Objective:** Make textbook publicly available

**Steps:**
1. Enable GitHub Pages (if not already enabled)
2. Test public URL: `https://org.github.io/physical-ai-textbook/`
3. Submit to:
   - Product Hunt
   - HackerNews
   - Reddit (r/robotics, r/AI)
   - LinkedIn
   - Twitter
4. Create launch announcement post highlighting:
   - Free, open-source textbook
   - RAG-powered chatbot
   - All 6 chapters available
   - GitHub repository link

**Acceptance Criteria:**
- [ ] Site publicly accessible
- [ ] All 6 chapters visible and searchable
- [ ] Chatbot functional for public users
- [ ] Announcement published on 3+ platforms

**Estimated Effort:** 2 hours  
**Owner:** Marketing / Community Lead

---

### 6.3 Monitoring & Operations

#### Task 5.5: Set Up Monitoring & Alerting
**Objective:** Track system health and performance

**Steps:**
1. GitHub Actions monitoring:
   - Enable notifications for failed builds
   - Review build logs weekly
2. RAG performance monitoring:
   ```python
   import logging
   from datetime import datetime
   
   logger = logging.getLogger("rag_monitoring")
   
   @app.post("/api/query")
   async def query(...):
       start = datetime.now()
       try:
           # Query logic
           elapsed = (datetime.now() - start).total_seconds()
           logger.info(f"Query completed in {elapsed:.2f}s")
       except Exception as e:
           logger.error(f"Query failed: {e}")
   ```
3. Set up centralized logging (e.g., free tier of Datadog or similar)
4. Configure email alerts for:
   - Build failures
   - API errors > threshold
   - Qdrant storage > 80% capacity

**Acceptance Criteria:**
- [ ] Logging implemented and centralized
- [ ] Alerts configured for critical issues
- [ ] Weekly monitoring report reviewed

**Estimated Effort:** 2 hours  
**Owner:** DevOps Engineer

---

#### Task 5.6: Community Feedback & Iteration
**Objective:** Gather initial feedback and plan improvements

**Steps:**
1. Monitor feedback channels:
   - GitHub Issues
   - Comments on launch posts
   - Email feedback
2. Create feedback spreadsheet:
   - Issue description
   - Category (bug/enhancement/documentation)
   - Priority (P0/P1/P2)
   - Assigned team member
3. Hold team sync (weekly for first month):
   - Review feedback
   - Prioritize fixes
   - Plan Phase 2 features
4. Document learnings in FEEDBACK.md

**Acceptance Criteria:**
- [ ] Feedback collection system in place
- [ ] Bugs triaged and assigned
- [ ] Enhancement backlog created
- [ ] First iteration planned

**Estimated Effort:** 2 hours/week (ongoing)  
**Owner:** Product Manager + Team

---

**Phase 5 Deliverables:**
✅ Textbook publicly launched  
✅ All systems operational and monitored  
✅ Community feedback collection active  
✅ Phase 2 roadmap planned

---

## VII. Phase 2 Future Features (Post-Launch)

### Optional Features (Not in MVP)

1. **Urdu Translation**
   - Pre-translate all chapters
   - RTL layout support
   - Searchable in Urdu

2. **Learner Personalization**
   - User profiles (difficulty, role)
   - Personalized responses
   - Reading history tracking

3. **Advanced RAG**
   - Hybrid semantic + keyword search
   - Response reranking
   - Conversation memory

4. **Community Features**
   - Discord integration
   - User-submitted questions archive
   - Contribution guidelines for translations

---

## VIII. Resource Allocation & Timeline

### Team Structure
- **Backend Engineer:** 1 FTE (infrastructure, RAG pipeline, API)
- **Frontend Engineer:** 0.5 FTE (Docusaurus, widget, UI)
- **Content Writer:** 0.5 FTE (chapter authoring)
- **Technical Reviewer:** 0.25 FTE (accuracy, QA)
- **DevOps Engineer:** 0.25 FTE (infrastructure, deployment)

### Timeline Summary

| Phase | Weeks | Key Deliverables |
|-------|-------|------------------|
| Phase 1: Foundation | Week 1 | GitHub repo, Docusaurus, Infrastructure provisioned |
| Phase 2: Content | Weeks 2–4 | All 6 chapters written + diagrams |
| Phase 3: RAG Backend | Weeks 5–6 | Ingestion pipeline, Query endpoint, Widget integration |
| Phase 4: Testing | Week 7 | Integration tests, Performance audit, Accessibility verified |
| Phase 5: Launch | Week 8 | Public launch, Monitoring enabled, Feedback collection |

**Total: 8 weeks (2 months) to MVP launch**

---

## IX. Success Criteria & Sign-Off

### MVP Success Criteria (Week 8)
- ✅ All 6 chapters published and accessible on GitHub Pages
- ✅ Docusaurus builds successfully (< 30 seconds)
- ✅ RAG chatbot responds to queries within 1 second
- ✅ 100% of manual audit queries return accurate, cited answers
- ✅ Zero hallucinations detected
- ✅ WCAG 2.1 AA accessibility compliance
- ✅ All services running on free-tier infrastructure
- ✅ GitHub Actions deployment automated
- ✅ Public GitHub repository with documentation
- ✅ Community feedback collection enabled

### Sign-Off Requirement
All success criteria must be met before marking MVP as complete.

**Sign-Off By:** Project Lead + Technical Reviewer

---

## X. Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Content delays | Medium | High | Hire additional writer; parallel chapter authoring |
| RAG hallucinations | Medium | High | Strict system prompts; validation layer; manual audits |
| Free-tier service limits exceeded | Low | High | Alternative providers identified; cost tracking enabled |
| Security vulnerabilities discovered | Low | Critical | Dependency scanning; security audit; quick patching |
| GitHub Pages deployment fails | Low | High | Test deployment weekly; rollback procedures documented |

---

**Document Status:** ✅ Production-Ready Implementation Plan  
**Last Updated:** 2025-12-05  
**Next Milestone:** Week 1 setup completion check-in (2025-12-12)

**Approved By:** [Project Lead Signature]  
**Reviewed By:** [Technical Lead Signature]

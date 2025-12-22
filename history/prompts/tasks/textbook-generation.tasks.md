# Tasks: Textbook Generation

**Project:** Physical AI & Humanoid Robotics — Essentials  
**Feature:** textbook-generation  
**Created:** 2025-12-05  
**Status:** Ready for Execution  
**Total Tasks:** 42  

---

## Task Organization by Phase & Priority

**Key:**
- 🔴 **P0 (Blocking)** – Blocks other work; must complete first
- 🟡 **P1 (Critical)** – Part of MVP; required for launch
- 🟢 **P2 (Important)** – Enhances quality; can defer if needed
- 🔵 **P3 (Nice-to-have)** – Optional; Phase 2 or later

---

## Phase 1: Foundation & Setup (Week 1)

### 1.1 Repository & Environment Setup

#### Task 1.1.1 🔴 P0: Create GitHub Repository
**Owner:** DevOps Engineer  
**Effort:** 30 minutes  
**Status:** Not Started

**Description:**
Initialize GitHub repository with proper structure and configuration for Docusaurus + RAG architecture.

**Acceptance Criteria:**
- [ ] Repository created at `github.com/org/physical-ai-textbook` (or similar)
- [ ] Public visibility enabled
- [ ] Main branch set as default
- [ ] Branch protection enabled (require PR reviews for main)
- [ ] GitHub Pages enabled (Settings → Pages)
- [ ] `.gitignore` configured (node_modules, .env, dist, build)
- [ ] README.md created with project overview

**Subtasks:**
1. Create repository on GitHub with description
2. Configure branch protection rules
3. Enable GitHub Pages
4. Create and push `.gitignore`
5. Create initial README.md

**Dependencies:** None  
**Blocks:** All other tasks

**Definition of Done:**
- Repository accessible and properly configured
- First commit pushed successfully
- GitHub Pages settings saved

---

#### Task 1.1.2 🟡 P1: Initialize Docusaurus Project
**Owner:** Frontend Engineer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Set up Docusaurus v3 classic template with TypeScript support and necessary plugins.

**Acceptance Criteria:**
- [ ] Docusaurus scaffolded using `create-docusaurus@latest`
- [ ] TypeScript configured (`tsconfig.json` present)
- [ ] `docusaurus.config.ts` configured with:
  - Title: "Physical AI & Humanoid Robotics — Essentials"
  - Base URL matching GitHub Pages URL
  - Dark mode enabled
  - Search plugin enabled
- [ ] `sidebars.ts` defines chapter structure (Ch1–Ch6)
- [ ] `npm run build` succeeds without errors
- [ ] `npm run start` runs local server on localhost:3000

**Subtasks:**
1. Run `npx create-docusaurus@latest physical-ai-textbook classic --typescript`
2. Install additional dependencies (search plugin, etc.)
3. Update `docusaurus.config.ts` with project settings
4. Configure `sidebars.ts` with chapter structure
5. Test build and local server
6. Commit to main branch

**Dependencies:** Task 1.1.1  
**Blocks:** Content creation, deployment setup

**Definition of Done:**
- Local Docusaurus server runs without errors
- Build completes in < 30 seconds
- Sidebar navigation displays correctly

---

#### Task 1.1.3 🟡 P1: Set Up GitHub Actions Deployment Workflow
**Owner:** DevOps Engineer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Create automated CI/CD pipeline for building and deploying Docusaurus to GitHub Pages.

**Acceptance Criteria:**
- [ ] `.github/workflows/deploy.yml` created
- [ ] Workflow triggers on push to main branch
- [ ] Workflow steps:
  1. Checkout code
  2. Setup Node.js 18
  3. Install dependencies (`npm ci`)
  4. Build Docusaurus (`npm run build`)
  5. Deploy to GitHub Pages
- [ ] First workflow run succeeds
- [ ] Site accessible at GitHub Pages URL after deploy
- [ ] Build completes in < 30 seconds

**Subtasks:**
1. Create `.github/workflows/` directory
2. Write `deploy.yml` workflow file
3. Test workflow by pushing to main
4. Verify GitHub Pages deployment succeeds
5. Document workflow in README

**Dependencies:** Task 1.1.1, Task 1.1.2  
**Blocks:** Automated deployments

**Definition of Done:**
- Workflow file properly formatted (no syntax errors)
- First automated build + deploy successful
- Site accessible via GitHub Pages URL

---

#### Task 1.1.4 🟡 P1: Configure Environment Variables & Secrets
**Owner:** DevOps Engineer  
**Effort:** 30 minutes  
**Status:** Not Started

**Description:**
Set up environment variables for backend services (Qdrant, PostgreSQL, OpenAI) in GitHub Secrets and local `.env` files.

**Acceptance Criteria:**
- [ ] `.env.example` created with all required variables (no values)
- [ ] `.env` added to `.gitignore`
- [ ] GitHub Secrets added:
  - `QDRANT_API_KEY`
  - `QDRANT_URL`
  - `DATABASE_URL`
  - `OPENAI_API_KEY`
- [ ] GitHub Actions workflow updated to use secrets
- [ ] Local `.env.local` created for development
- [ ] Documentation on environment setup in README

**Subtasks:**
1. Create `.env.example` template file
2. Add `.env*` patterns to `.gitignore`
3. Add secrets to GitHub repository settings
4. Update `deploy.yml` to reference secrets
5. Document environment setup process

**Dependencies:** Task 1.1.1, Task 1.1.3  
**Blocks:** Backend development and deployment

**Definition of Done:**
- Environment variables properly documented
- Secrets securely stored in GitHub
- Local development environment configurable

---

### 1.2 Infrastructure Provisioning

#### Task 1.2.1 🟡 P1: Provision Qdrant Cloud Vector Database
**Owner:** DevOps Engineer  
**Effort:** 30 minutes  
**Status:** Not Started

**Description:**
Set up Qdrant Cloud cluster for storing chapter embeddings and enabling RAG semantic search.

**Acceptance Criteria:**
- [ ] Qdrant Cloud account created (free tier)
- [ ] Cluster created:
  - Name: `physical-ai-textbook-prod`
  - Tier: Free tier
  - Region: US-East (or closest)
- [ ] Cluster credentials obtained:
  - URL (e.g., `https://xxx-qdrant.a.run.app`)
  - API Key
- [ ] Credentials saved to GitHub Secrets
- [ ] Connection test successful from local machine:
  ```python
  from qdrant_client import QdrantClient
  client = QdrantClient(url="<url>", api_key="<key>")
  client.get_collections()  # Should return empty list
  ```
- [ ] Free-tier limits documented (1GB storage, 10K requests/month)

**Subtasks:**
1. Sign up for Qdrant Cloud
2. Create cluster with correct settings
3. Retrieve and save credentials
4. Test connection from local machine
5. Save credentials to GitHub Secrets

**Dependencies:** Task 1.1.4  
**Blocks:** RAG backend development

**Definition of Done:**
- Qdrant cluster accessible and tested
- Credentials securely stored
- Connection confirmed working

---

#### Task 1.2.2 🟡 P1: Provision Neon PostgreSQL Database
**Owner:** DevOps Engineer  
**Effort:** 45 minutes  
**Status:** Not Started

**Description:**
Set up Neon PostgreSQL database for storing chunk metadata and chat session history.

**Acceptance Criteria:**
- [ ] Neon account created (free tier)
- [ ] Project created:
  - Name: `physical-ai-textbook`
  - Region: US-East
- [ ] Database created: `textbook_rag`
- [ ] Connection string obtained and saved
- [ ] Initial schema created:
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
- [ ] Connection test successful:
  ```bash
  psql "<DATABASE_URL>"
  \dt  # Should list tables
  ```

**Subtasks:**
1. Sign up for Neon
2. Create project and database
3. Retrieve connection string
4. Execute SQL schema creation script
5. Test connection with psql
6. Save credentials to GitHub Secrets

**Dependencies:** Task 1.1.4  
**Blocks:** RAG backend development

**Definition of Done:**
- PostgreSQL database accessible and tested
- Schema tables created successfully
- Connection string saved securely

---

#### Task 1.2.3 🟡 P1: Deploy FastAPI Backend Server
**Owner:** Backend Engineer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Set up FastAPI backend application skeleton and deploy to free-tier server (Vercel, Railway, or Render).

**Acceptance Criteria:**
- [ ] FastAPI application created (`backend/app.py`):
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
  ```
- [ ] Deployed to free-tier service (Vercel, Railway, or Render)
- [ ] Public URL obtained (e.g., `https://physical-ai-rag.vercel.app`)
- [ ] Health check endpoint responds with 200 OK
- [ ] CORS configured for Docusaurus domain
- [ ] Requirements file created: `backend/requirements.txt`

**Subtasks:**
1. Create FastAPI application skeleton
2. Choose deployment platform
3. Configure deployment settings
4. Deploy to free-tier server
5. Test health check endpoint
6. Verify CORS headers working

**Dependencies:** Task 1.1.4, Task 1.2.1, Task 1.2.2  
**Blocks:** RAG API development

**Definition of Done:**
- FastAPI app deployed and publicly accessible
- Health endpoint returns 200 OK
- Backend URL ready for frontend integration

---

**Phase 1 Summary:**
- ✅ All foundation infrastructure in place
- ✅ CI/CD pipeline automated
- ✅ Backend server operational
- ✅ Team ready to begin content creation

**Phase 1 Sign-Off Date:** 2025-12-12 (target)

---

## Phase 2: Content Creation (Weeks 2–4)

### 2.1 Content Planning

#### Task 2.1.1 🔴 P0: Create Detailed Content Outline
**Owner:** Content Lead  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Define chapter structure, learning outcomes, and content breakdown for all 6 chapters.

**Acceptance Criteria:**
- [ ] Outline document created (`CONTENT_OUTLINE.md`)
- [ ] All 6 chapters outlined with:
  - Learning outcomes (3–5 bullet points each)
  - Section titles and word counts
  - Key concepts to cover
  - Code examples or diagrams needed
- [ ] Word count per chapter: 1,000–1,500 words
- [ ] Diagrams identified (2–4 per chapter)
- [ ] Code examples planned (≤ 20 lines each)
- [ ] Approved by Technical Reviewer

**Subtasks:**
1. Define learning outcomes for each chapter
2. Break each chapter into 3–4 sections
3. Estimate word counts per section
4. List required diagrams and code examples
5. Get technical reviewer approval
6. Commit outline to repository

**Dependencies:** None (can start in parallel with Phase 1)  
**Blocks:** Chapter writing tasks

**Definition of Done:**
- Outline document complete and approved
- All content requirements clear
- Team aligned on chapter structure

---

#### Task 2.1.2 🟡 P1: Set Up Chapter Writing Workflow
**Owner:** Content Lead  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Establish review process, style guide, and templates for chapter authoring.

**Acceptance Criteria:**
- [ ] Style guide created (`STYLE_GUIDE.md`):
  - Tone and voice guidelines
  - Technical accuracy standards
  - Formatting rules (headings, lists, code blocks)
- [ ] Peer review checklist created
- [ ] Chapter template created (`docs/chapters/TEMPLATE.md`)
- [ ] PR review process documented
- [ ] Technical reviewer assigned

**Subtasks:**
1. Write style guide for consistency
2. Create peer review checklist
3. Create chapter template with sections
4. Document PR review workflow
5. Assign technical reviewer

**Dependencies:** Task 2.1.1  
**Blocks:** Chapter writing

**Definition of Done:**
- Style guide and templates ready for authors
- Review process documented
- Team trained on process

---

### 2.2 Chapter Writing (Each 8 hours total)

#### Task 2.2.1 🟡 P1: Write Chapter 1 — Introduction to Physical AI
**Owner:** Content Writer  
**Effort:** 8 hours (4 writing + 2 review + 2 integration)  
**Status:** Not Started

**Description:**
Write comprehensive introduction chapter covering definitions, scope, and historical context of Physical AI.

**Acceptance Criteria:**
- [ ] Chapter written in Markdown (`docs/chapters/ch1-physical-ai.md`)
- [ ] Word count: 1,000–1,500 words
- [ ] 4 sections completed:
  1. Definition and scope (~300 words)
  2. Classical vs. Physical AI (~300 words)
  3. Real-world examples (~400 words)
  4. Why embodiment matters (~300 words)
- [ ] Learning outcomes listed at top
- [ ] 2–4 diagrams included with captions
- [ ] 1 code example or conceptual diagram
- [ ] Peer reviewed for accuracy
- [ ] Docusaurus build succeeds with chapter included
- [ ] Chapter renders correctly in HTML

**Subtasks:**
1. Write draft following chapter template
2. Include all learning outcomes
3. Create/integrate diagrams
4. Submit for peer review
5. Incorporate feedback
6. Test Docusaurus build with chapter
7. Commit to main branch

**Dependencies:** Task 2.1.1, Task 2.1.2  
**Blocks:** Diagram creation for Chapter 1

**Definition of Done:**
- Chapter written, reviewed, and merged to main
- Docusaurus builds successfully
- Chapter displays correctly on GitHub Pages

---

#### Task 2.2.2 🟡 P1: Write Chapter 2 — Basics of Humanoid Robotics
**Owner:** Content Writer  
**Effort:** 8 hours  
**Status:** Not Started

**Description:**
Write chapter covering robot anatomy, kinematics, sensors, and actuators.

**Acceptance Criteria:**
- [ ] Chapter written in Markdown (`docs/chapters/ch2-humanoid-robotics.md`)
- [ ] Word count: 1,000–1,500 words
- [ ] 4 sections:
  1. Robot anatomy and DOF (~350 words)
  2. Kinematics basics (~300 words)
  3. Sensors and perception (~300 words)
  4. Actuators and control (~300 words)
- [ ] Learning outcomes listed
- [ ] 2–4 diagrams (anatomy, kinematic chain, sensor placement)
- [ ] Peer reviewed and accurate
- [ ] Integrated and tested in Docusaurus

**Subtasks:**
1. Write draft following template
2. Include all required sections
3. Create/integrate diagrams (robot anatomy, sensor placement)
4. Peer review
5. Revise based on feedback
6. Build and test in Docusaurus
7. Commit to main

**Dependencies:** Task 2.2.1  
**Blocks:** Chapter 3

**Definition of Done:**
- Chapter 2 complete, reviewed, and deployed

---

#### Task 2.2.3 🟡 P1: Write Chapter 3 — ROS 2 Fundamentals
**Owner:** Content Writer  
**Effort:** 8 hours  
**Status:** Not Started

**Description:**
Write chapter covering ROS 2 basics: nodes, topics, services, and actions.

**Acceptance Criteria:**
- [ ] Chapter written (`docs/chapters/ch3-ros2.md`)
- [ ] Word count: 1,000–1,500 words
- [ ] 4 sections:
  1. ROS 2 architecture and overview (~300 words)
  2. Nodes, topics, and pub/sub (~350 words)
  3. Services and actions (~300 words)
  4. Practical ROS 2 example (~300 words)
- [ ] Diagrams: pub/sub architecture, service/action flow
- [ ] Code example: simple publisher/subscriber (Python)
- [ ] Peer reviewed and accurate
- [ ] Integrated in Docusaurus

**Subtasks:**
1. Write draft
2. Include all ROS 2 concepts
3. Create architecture diagrams
4. Add code examples
5. Peer review
6. Revise and integrate
7. Test Docusaurus build

**Dependencies:** Task 2.2.2  
**Blocks:** Chapter 4

**Definition of Done:**
- Chapter 3 complete and deployed

---

#### Task 2.2.4 🟡 P1: Write Chapter 4 — Digital Twin Simulation
**Owner:** Content Writer  
**Effort:** 8 hours  
**Status:** Not Started

**Description:**
Write chapter covering Gazebo simulator, digital twins, and physics-based simulation.

**Acceptance Criteria:**
- [ ] Chapter written (`docs/chapters/ch4-digital-twin.md`)
- [ ] Word count: 1,000–1,500 words
- [ ] 4 sections:
  1. Digital twin concept (~300 words)
  2. Gazebo basics (~300 words)
  3. Physics simulation (~300 words)
  4. Practical simulation example (~300 words)
- [ ] Diagrams: digital twin workflow, Gazebo architecture
- [ ] Code snippet: simple Gazebo world file
- [ ] Peer reviewed
- [ ] Integrated in Docusaurus

**Subtasks:**
1. Write draft
2. Explain digital twin concept clearly
3. Cover Gazebo basics
4. Create workflow diagrams
5. Add code examples
6. Peer review
7. Integrate and test

**Dependencies:** Task 2.2.3  
**Blocks:** Chapter 5

**Definition of Done:**
- Chapter 4 complete and deployed

---

#### Task 2.2.5 🟡 P1: Write Chapter 5 — Vision-Language-Action Systems
**Owner:** Content Writer  
**Effort:** 8 hours  
**Status:** Not Started

**Description:**
Write chapter covering VLMs, vision models, language processing, and end-to-end learning.

**Acceptance Criteria:**
- [ ] Chapter written (`docs/chapters/ch5-vla.md`)
- [ ] Word count: 1,000–1,500 words
- [ ] 4 sections:
  1. Vision-language model basics (~300 words)
  2. Perception pipeline (~300 words)
  3. Language grounding (~300 words)
  4. Action generation and control (~300 words)
- [ ] Diagrams: VLA inference pipeline, action selection flow
- [ ] Code example: VLA inference pseudocode
- [ ] Peer reviewed
- [ ] Integrated in Docusaurus

**Subtasks:**
1. Write draft
2. Explain VLM concepts
3. Cover perception and grounding
4. Create pipeline diagrams
5. Add pseudocode examples
6. Peer review
7. Integrate and test

**Dependencies:** Task 2.2.4  
**Blocks:** Chapter 6

**Definition of Done:**
- Chapter 5 complete and deployed

---

#### Task 2.2.6 🟡 P1: Write Chapter 6 — Capstone Project
**Owner:** Content Writer  
**Effort:** 8 hours  
**Status:** Not Started

**Description:**
Write capstone chapter integrating all concepts: end-to-end AI→robot pipeline.

**Acceptance Criteria:**
- [ ] Chapter written (`docs/chapters/ch6-capstone.md`)
- [ ] Word count: 1,000–1,500 words
- [ ] 4 sections:
  1. Capstone project overview (~250 words)
  2. Full pipeline architecture (~350 words)
  3. Step-by-step implementation (~400 words)
  4. Next steps and resources (~300 words)
- [ ] Diagrams: full pipeline architecture, deployment workflow
- [ ] Code example: complete minimal pipeline example
- [ ] Peer reviewed
- [ ] Integrated in Docusaurus

**Subtasks:**
1. Write draft
2. Design capstone project scope
3. Create architecture diagrams
4. Write implementation walkthrough
5. Add complete code example
6. Peer review
7. Integrate and test

**Dependencies:** Task 2.2.5  
**Blocks:** Diagram creation

**Definition of Done:**
- Chapter 6 complete and deployed
- All 6 chapters now published

---

### 2.3 Diagram Creation

#### Task 2.3.1 🟡 P1: Create All Chapter Diagrams (12–16 total)
**Owner:** Technical Illustrator  
**Effort:** 4 hours  
**Status:** Not Started

**Description:**
Create vector diagrams for all chapters, covering architecture, workflows, and concepts.

**Acceptance Criteria:**
- [ ] All 12–16 diagrams created:
  - Chapter 1: Classical vs Physical AI, Real-world applications (2)
  - Chapter 2: Robot anatomy, Sensor/actuator placement (2)
  - Chapter 3: ROS 2 pub/sub, Service/action flow (2)
  - Chapter 4: Digital twin workflow, Gazebo architecture (2)
  - Chapter 5: VLA inference pipeline, Action selection (2)
  - Chapter 6: Full pipeline architecture, Deployment workflow (2)
- [ ] Format: SVG (preferred) or optimized PNG (< 200KB each)
- [ ] Alt text added to all diagrams
- [ ] Captions added below diagrams
- [ ] Stored in `static/diagrams/` folder
- [ ] Integrated into chapters

**Subtasks:**
1. Choose diagram tool (Mermaid, Lucidchart, or Excalidraw)
2. Create all 12–16 diagrams
3. Optimize images (convert to SVG if possible)
4. Write alt text and captions
5. Store in static folder
6. Integrate into Markdown chapters
7. Verify rendering in Docusaurus

**Dependencies:** Task 2.2.6 (all chapters written)  
**Blocks:** None (parallel with writing)

**Definition of Done:**
- All diagrams created, optimized, and integrated
- Alt text on all diagrams for accessibility
- Docusaurus renders diagrams correctly

---

**Phase 2 Summary:**
- ✅ All 6 chapters written (~9,000 words total)
- ✅ All 12–16 diagrams created and integrated
- ✅ All chapters peer-reviewed for accuracy
- ✅ Textbook content complete

**Phase 2 Sign-Off Date:** 2025-12-26 (target)

---

## Phase 3: RAG Backend Implementation (Weeks 5–6)

### 3.1 Ingestion Pipeline

#### Task 3.1.1 🟡 P1: Build Content Ingestion Script
**Owner:** Backend Engineer  
**Effort:** 4 hours  
**Status:** Not Started

**Description:**
Create Python script to parse Markdown chapters, chunk text, generate embeddings, and store in Qdrant + PostgreSQL.

**Acceptance Criteria:**
- [ ] Script created (`backend/ingest.py`)
- [ ] Chunks text into 512-token segments (overlap handling)
- [ ] Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- [ ] Stores chunks in Qdrant with embeddings
- [ ] Stores metadata in PostgreSQL (chapter, section, content)
- [ ] Handles duplicate detection (prevents re-ingestion)
- [ ] Processes all 6 chapters (target: ≤ 2,000 total chunks)
- [ ] Script executable: `python backend/ingest.py`
- [ ] Logs ingestion progress and results

**Subtasks:**
1. Write text chunking function (512 tokens, overlap)
2. Load embedding model (all-MiniLM-L6-v2)
3. Create Qdrant collection for embeddings
4. Implement PostgreSQL storage
5. Add duplicate detection
6. Test with single chapter
7. Run on all 6 chapters
8. Verify chunk counts and storage

**Dependencies:** Task 1.2.1, Task 1.2.2, Task 2.2.6 (all chapters)  
**Blocks:** RAG query endpoint

**Definition of Done:**
- Ingestion script successfully processes all 6 chapters
- Embeddings stored in Qdrant (verified with client query)
- Metadata stored in PostgreSQL (verified with psql query)
- ≤ 2,000 total chunks created

---

#### Task 3.1.2 🟡 P1: Integrate Ingestion into GitHub Actions
**Owner:** DevOps Engineer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Automate ingestion step in CI/CD pipeline so embeddings update on main branch push.

**Acceptance Criteria:**
- [ ] `.github/workflows/deploy.yml` updated to include ingestion step
- [ ] Ingestion runs BEFORE deployment to GitHub Pages
- [ ] Environment variables passed to ingestion script
- [ ] Workflow logs show successful ingestion
- [ ] Handles ingestion failures gracefully
- [ ] First automated ingestion run successful

**Subtasks:**
1. Update GitHub Actions workflow YAML
2. Add pip install step for backend dependencies
3. Call `python backend/ingest.py`
4. Pass environment variables (QDRANT_*, DATABASE_URL)
5. Test workflow by pushing code change
6. Verify ingestion completed in logs
7. Document workflow in README

**Dependencies:** Task 1.1.3, Task 3.1.1  
**Blocks:** Automated deployments

**Definition of Done:**
- GitHub Actions workflow includes ingestion
- Ingestion runs automatically on main branch push
- Workflow logs confirm success

---

### 3.2 RAG Query Endpoint

#### Task 3.2.1 🟡 P1: Implement RAG Query Endpoint
**Owner:** Backend Engineer  
**Effort:** 3 hours  
**Status:** Not Started

**Description:**
Build FastAPI `/api/query` endpoint that searches Qdrant, retrieves context, generates responses via LLM, and returns cited answers.

**Acceptance Criteria:**
- [ ] POST endpoint `/api/query` created in `backend/app.py`
- [ ] Accepts request body:
  ```json
  {
    "q": "What is Physical AI?",
    "difficulty": "normal",
    "role": "student"
  }
  ```
- [ ] Query embedding generated using all-MiniLM-L6-v2
- [ ] Qdrant search returns top-3 most relevant chunks
- [ ] Context prepared from retrieved chunks
- [ ] OpenAI GPT-4o-mini generates response from context
- [ ] Response includes:
  ```json
  {
    "answer": "Physical AI is...",
    "sources": [
      {
        "chapter": 1,
        "section": "Definition and scope",
        "quote": "..."
      }
    ],
    "confidence": 0.95
  }
  ```
- [ ] Response latency < 1 second (measured)
- [ ] Low temperature (0.2) ensures deterministic responses

**Subtasks:**
1. Create query endpoint handler
2. Implement query embedding generation
3. Implement Qdrant search (k=3)
4. Build context from retrieved chunks
5. Call OpenAI API with system prompt
6. Format response with sources
7. Test endpoint with curl/Postman
8. Measure latency
9. Deploy and test from Docusaurus

**Dependencies:** Task 1.2.3, Task 3.1.1  
**Blocks:** Frontend integration, validation layer

**Definition of Done:**
- Endpoint accepts queries and returns formatted responses
- Latency consistently < 1 second
- Citations include chapter and section info

---

#### Task 3.2.2 🟡 P1: Add RAG Response Validation & Constraints
**Owner:** Backend Engineer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Implement response validation layer to prevent hallucinations and ensure answers are grounded in textbook content.

**Acceptance Criteria:**
- [ ] Validation function checks response references context
- [ ] Low-confidence responses trigger fallback message
- [ ] Out-of-scope queries return appropriate message
- [ ] System prompt enforces citation-only behavior
- [ ] Validation catches obvious hallucinations
- [ ] Manual audit confirms 100% accuracy on sample queries

**Subtasks:**
1. Write response validation function
2. Implement confidence threshold check (< 0.3 → fallback)
3. Add system prompt guidance (cite only from textbook)
4. Test with hallucination-prone queries
5. Implement fallback responses
6. Test manual queries
7. Document validation rules

**Dependencies:** Task 3.2.1  
**Blocks:** Frontend integration

**Definition of Done:**
- Validation layer prevents obvious hallucinations
- Manual audit confirms 100% accuracy
- Out-of-scope queries handled gracefully

---

### 3.3 Frontend Integration

#### Task 3.3.1 🟡 P1: Create Chatbot Widget Component
**Owner:** Frontend Engineer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Build React component for "Select text → Ask AI" chatbot widget embedded on all textbook pages.

**Acceptance Criteria:**
- [ ] Component created: `src/components/ChatbotWidget.tsx`
- [ ] Features:
  - Floating button (💬 Ask AI)
  - Text selection detection (auto-focus on select)
  - Query input field
  - Submit button
  - Loading state
  - Response display with citations
- [ ] Fetches from `/api/query` endpoint
- [ ] Responsive design (mobile-friendly)
- [ ] Dark mode support
- [ ] Dismissible/closeable

**Subtasks:**
1. Create React component with hooks (useState)
2. Implement text selection listener
3. Add query input and submit button
4. Implement API call to backend
5. Add loading and error states
6. Format and display response with citations
7. Style component with CSS module
8. Test on desktop and mobile

**Dependencies:** Task 1.1.2, Task 3.2.1  
**Blocks:** Widget integration

**Definition of Done:**
- Component renders on all pages
- Text selection triggers widget
- API calls work correctly
- Responsive and accessible

---

#### Task 3.3.2 🟡 P1: Create Citation Block Component
**Owner:** Frontend Engineer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Build component to display source citations with professional formatting.

**Acceptance Criteria:**
- [ ] Component created: `src/components/CitationBlock.tsx`
- [ ] Displays:
  - Chapter number
  - Section title
  - Source quote (truncated if long)
- [ ] Styling:
  - Professional blockquote formatting
  - Highlighted color scheme
  - Dark mode support
- [ ] Accessible (ARIA labels)

**Subtasks:**
1. Create citation component
2. Accept props: chapter, section, quote
3. Format and style for display
4. Add dark mode CSS
5. Test rendering
6. Ensure accessibility

**Dependencies:** Task 3.3.1  
**Blocks:** None

**Definition of Done:**
- Citations display correctly in widget
- Professional formatting applied
- Accessible to screen readers

---

#### Task 3.3.3 🟡 P1: Integrate Widget into Docusaurus Layout
**Owner:** Frontend Engineer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Embed chatbot widget on all Docusaurus pages (docs, blog, homepage).

**Acceptance Criteria:**
- [ ] Widget imported into main layout component
- [ ] Appears on all pages (fixed position, bottom-right)
- [ ] Doesn't interfere with page content
- [ ] Persists across page navigation
- [ ] Backend URL configured correctly
- [ ] CORS working properly

**Subtasks:**
1. Import ChatbotWidget into Layout
2. Position widget (fixed, bottom-right)
3. Add z-index and styling
4. Configure backend API URL
5. Test on multiple pages
6. Test CORS setup
7. Deploy and verify

**Dependencies:** Task 3.3.1, Task 1.2.3  
**Blocks:** Launch

**Definition of Done:**
- Widget visible on all pages
- No page layout conflicts
- Backend communication working

---

**Phase 3 Summary:**
- ✅ RAG ingestion pipeline fully automated
- ✅ Query endpoint returns grounded answers with citations
- ✅ Chatbot widget integrated into textbook
- ✅ Citation display formatted and accessible

**Phase 3 Sign-Off Date:** 2026-01-09 (target)

---

## Phase 4: Integration & Testing (Week 7)

### 4.1 End-to-End Testing

#### Task 4.1.1 🟡 P1: Write Integration Tests
**Owner:** QA Engineer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Create pytest test suite for full RAG pipeline: textbook → ingestion → query → response.

**Acceptance Criteria:**
- [ ] Test file created: `tests/test_integration.py`
- [ ] Tests cover:
  - Query endpoint returns valid response
  - Response includes sources (chapter, section, quote)
  - Out-of-scope queries handled appropriately
  - Response latency < 1 second
  - Citation accuracy verified
- [ ] All tests pass
- [ ] Tests executable: `pytest tests/test_integration.py -v`

**Subtasks:**
1. Set up pytest fixtures
2. Write test for valid query response
3. Write test for response structure
4. Write test for out-of-scope query
5. Write latency test
6. Write citation accuracy test
7. Run all tests
8. Fix any failures

**Dependencies:** Task 3.2.1, Task 3.2.2  
**Blocks:** Manual testing

**Definition of Done:**
- All integration tests pass
- Test coverage adequate (all major code paths)
- Latency consistently < 1 second

---

#### Task 4.1.2 🔴 P0: Manual Accuracy Audit (20 sample queries)
**Owner:** Technical Reviewer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Manually verify 20 sample queries return accurate, cited answers with no hallucinations.

**Acceptance Criteria:**
- [ ] 20 test queries selected from across all chapters
- [ ] Each query submitted to chatbot
- [ ] For each response, verify:
  - [ ] Answer is accurate and relevant
  - [ ] Citation includes correct chapter/section
  - [ ] Quote text matches source
  - [ ] No hallucinations detected
- [ ] 20/20 queries pass accuracy check
- [ ] Audit report created: `tests/AUDIT_REPORT.md`
- [ ] Zero hallucinations tolerated

**Subtasks:**
1. Create list of 20 diverse test queries
2. Submit each query to chatbot
3. Document response for each query
4. Verify accuracy of each answer
5. Verify citation correctness
6. Check for hallucinations
7. Create audit report
8. Document any issues

**Dependencies:** Task 3.3.3 (widget integrated)  
**Blocks:** Performance testing

**Definition of Done:**
- All 20 queries verified accurate
- Zero hallucinations detected
- Audit report completed

---

### 4.2 Performance & Accessibility Testing

#### Task 4.2.1 🟡 P1: Performance Audit (Lighthouse & Metrics)
**Owner:** DevOps Engineer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Run Lighthouse and performance benchmarks to verify all targets met.

**Acceptance Criteria:**
- [ ] Lighthouse score ≥ 90 on all pages
- [ ] Page load time < 2 seconds (measured)
- [ ] First Contentful Paint < 1.5 seconds
- [ ] Cumulative Layout Shift < 0.1
- [ ] Build time < 30 seconds (Docusaurus)
- [ ] RAG query latency < 1 second (99th percentile)
- [ ] Performance report created: `PERFORMANCE_REPORT.md`

**Subtasks:**
1. Run Lighthouse on homepage
2. Run Lighthouse on each chapter page
3. Measure page load times (real user simulation)
4. Test on slow 3G network
5. Measure build time
6. Measure RAG query latency (100 queries)
7. Create performance report
8. Document any issues

**Dependencies:** Task 3.3.3, Task 4.1.1  
**Blocks:** Accessibility testing

**Definition of Done:**
- Lighthouse score ≥ 90 on all pages
- All metrics meet targets
- Performance report documented

---

#### Task 4.2.2 🟡 P1: Accessibility Audit (WCAG 2.1 AA)
**Owner:** QA Engineer  
**Effort:** 3 hours  
**Status:** Not Started

**Description:**
Verify compliance with WCAG 2.1 AA accessibility standards.

**Acceptance Criteria:**
- [ ] Zero automated accessibility violations (axe tool)
- [ ] Keyboard navigation functional (Tab, Enter, Escape)
- [ ] Screen reader compatible (NVDA/JAWS tested)
- [ ] Color contrast ratios ≥ 4.5:1 for text
- [ ] All images have alt text
- [ ] Heading hierarchy semantic (H1 → H2 → H3)
- [ ] Form inputs labeled
- [ ] Mobile accessibility verified
- [ ] Accessibility report: `ACCESSIBILITY_REPORT.md`

**Subtasks:**
1. Run axe accessibility scanner
2. Test keyboard navigation
3. Test with screen reader
4. Check color contrast ratios
5. Verify all alt text present
6. Check heading hierarchy
7. Test on mobile devices
8. Create accessibility report

**Dependencies:** Task 4.2.1  
**Blocks:** Security testing

**Definition of Done:**
- Zero accessibility violations
- Keyboard and screen reader fully functional
- WCAG 2.1 AA compliant

---

### 4.3 Security & Infrastructure Testing

#### Task 4.3.1 🟡 P1: Security Hardening & Validation
**Owner:** Backend Engineer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Implement security best practices: rate limiting, input validation, security headers, vulnerability scanning.

**Acceptance Criteria:**
- [ ] Rate limiting enabled (100 requests/minute per IP)
- [ ] Input validation on all API endpoints
- [ ] Security headers added:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Content-Security-Policy
- [ ] HTTPS enforced (GitHub Pages auto-enabled)
- [ ] Dependency vulnerabilities scanned:
  - `npm audit` passes
  - `pip install safety && safety check` passes
- [ ] Security report: `SECURITY_REPORT.md`

**Subtasks:**
1. Implement rate limiting (slowapi)
2. Add input validation (Pydantic)
3. Add security headers
4. Run npm audit
5. Run pip safety check
6. Document findings
7. Create security report

**Dependencies:** Task 1.2.3  
**Blocks:** Infrastructure testing

**Definition of Done:**
- Rate limiting prevents abuse
- No high-severity vulnerabilities
- Security headers present

---

#### Task 4.3.2 🟡 P1: Infrastructure Resilience Testing
**Owner:** DevOps Engineer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Test failure scenarios: service outages, failovers, recovery mechanisms.

**Acceptance Criteria:**
- [ ] Qdrant outage: Graceful error message to user
- [ ] PostgreSQL outage: Connection retry works
- [ ] OpenAI API timeout: Fallback response generated
- [ ] Load test (100 concurrent users): No crashes
- [ ] Automatic recovery verified on service restore

**Subtasks:**
1. Simulate Qdrant outage
2. Simulate PostgreSQL outage
3. Simulate OpenAI timeout
4. Run load test with locust
5. Verify fallback mechanisms
6. Test automatic recovery
7. Document resilience report

**Dependencies:** Task 1.2.1, Task 1.2.2, Task 1.2.3  
**Blocks:** Launch

**Definition of Done:**
- System gracefully handles all failure scenarios
- Automatic recovery working
- Resilience verified

---

**Phase 4 Summary:**
- ✅ All integration tests passing
- ✅ Manual accuracy audit: 100% correct answers
- ✅ Performance targets verified
- ✅ Accessibility WCAG 2.1 AA compliant
- ✅ Security hardened
- ✅ Infrastructure resilient

**Phase 4 Sign-Off Date:** 2026-01-16 (target)

---

## Phase 5: Launch & Monitoring (Week 8)

### 5.1 Pre-Launch Checklist

#### Task 5.1.1 🔴 P0: Final Content Review
**Owner:** Content Lead + Technical Reviewer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Final verification of all textbook content before public launch.

**Acceptance Criteria:**
- [ ] All 6 chapters accurate and peer-reviewed
- [ ] All diagrams present and captioned
- [ ] All code examples tested
- [ ] No broken links (internal or external)
- [ ] Spelling and grammar checked
- [ ] Technical terms consistent
- [ ] References complete
- [ ] Sign-off document created

**Subtasks:**
1. Review each chapter for accuracy
2. Check all diagrams display correctly
3. Test all code examples
4. Verify all links functional
5. Spell-check all content
6. Check terminology consistency
7. Create sign-off document

**Dependencies:** Task 2.2.6 (all chapters complete)  
**Blocks:** Launch

**Definition of Done:**
- All content reviewed and approved
- No errors found
- Ready for public access

---

#### Task 5.1.2 🔴 P0: Infrastructure Readiness Check
**Owner:** DevOps Engineer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Final verification of all infrastructure services before launch.

**Acceptance Criteria:**
- [ ] GitHub Pages deployment successful
- [ ] Docusaurus build successful (< 30 seconds)
- [ ] RAG backend API responding
- [ ] Qdrant cluster healthy (≤ 2,000 chunks)
- [ ] PostgreSQL database accessible
- [ ] GitHub Actions workflow passing
- [ ] Monitoring and logging enabled
- [ ] Backup procedures documented
- [ ] Sign-off document created

**Subtasks:**
1. Test GitHub Pages URL
2. Verify build time
3. Test API health endpoint
4. Check Qdrant collection status
5. Test database connection
6. Verify GitHub Actions pass
7. Enable monitoring
8. Document backups
9. Create sign-off document

**Dependencies:** Task 4.3.2 (resilience testing)  
**Blocks:** Launch

**Definition of Done:**
- All infrastructure verified operational
- Monitoring enabled
- Ready for public traffic

---

#### Task 5.1.3 🟡 P1: Documentation Review
**Owner:** Technical Writer  
**Effort:** 1 hour  
**Status:** Not Started

**Description:**
Verify all user-facing and developer documentation is complete and accurate.

**Acceptance Criteria:**
- [ ] README.md complete with project overview
- [ ] CONTRIBUTING.md guides contributors
- [ ] API documentation (OpenAPI schema)
- [ ] ARCHITECTURE.md documents design
- [ ] Deployment guide documented
- [ ] Troubleshooting guide documented
- [ ] Link to GitHub repository in textbook

**Subtasks:**
1. Review and update README.md
2. Write CONTRIBUTING.md
3. Generate OpenAPI documentation
4. Write ARCHITECTURE.md
5. Create deployment guide
6. Create troubleshooting guide
7. Add repository link to textbook

**Dependencies:** Task 1.1.1  
**Blocks:** Launch announcement

**Definition of Done:**
- All documentation complete and accurate
- Ready for public developers

---

### 5.2 Launch & Announcement

#### Task 5.2.1 🟡 P1: Public Launch
**Owner:** Marketing / Community Lead  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Make textbook publicly available and announce to community.

**Acceptance Criteria:**
- [ ] GitHub Pages URL publicly accessible
- [ ] All 6 chapters visible and searchable
- [ ] Chatbot functional for public users
- [ ] Announcement posted on:
  - Product Hunt
  - HackerNews
  - Reddit (r/robotics, r/AI, r/MachineLearning)
  - LinkedIn
  - Twitter
- [ ] GitHub repository made public
- [ ] License set (recommend: Creative Commons or MIT)

**Subtasks:**
1. Test public URL accessibility
2. Verify all content loads
3. Test chatbot functionality
4. Write announcement post
5. Post to Product Hunt
6. Post to HackerNews
7. Post to Reddit
8. Post to LinkedIn
9. Post to Twitter
10. Make repository public
11. Add license file

**Dependencies:** Task 5.1.1, Task 5.1.2, Task 5.1.3  
**Blocks:** Monitoring setup

**Definition of Done:**
- Site publicly accessible
- Announcement published on 5+ platforms
- Repository public
- License specified

---

### 5.3 Monitoring & Operations

#### Task 5.3.1 🟡 P1: Set Up Monitoring & Alerting
**Owner:** DevOps Engineer  
**Effort:** 2 hours  
**Status:** Not Started

**Description:**
Implement system monitoring, logging, and alerts for ongoing operations.

**Acceptance Criteria:**
- [ ] GitHub Actions notifications enabled
- [ ] API error logging implemented
- [ ] Performance metrics collected:
  - Query latency percentiles
  - API error rates
  - Qdrant storage usage
- [ ] Email alerts configured for:
  - Build failures
  - API errors > threshold (5% error rate)
  - Qdrant storage > 80%
- [ ] Weekly monitoring report process defined
- [ ] Monitoring dashboard created (optional)

**Subtasks:**
1. Enable GitHub Actions email notifications
2. Implement API logging with Python logging
3. Collect performance metrics
4. Configure email alerts
5. Set alert thresholds
6. Create monitoring dashboard (optional)
7. Document monitoring process

**Dependencies:** Task 5.2.1  
**Blocks:** Operations

**Definition of Done:**
- Monitoring active and alerts functional
- Weekly review process documented

---

#### Task 5.3.2 🟡 P1: Community Feedback & Iteration
**Owner:** Product Manager  
**Effort:** 2 hours/week (ongoing)  
**Status:** Not Started

**Description:**
Collect, triage, and prioritize user feedback for ongoing improvements.

**Acceptance Criteria:**
- [ ] Feedback channels monitored:
  - GitHub Issues
  - Comments on announcements
  - Email feedback
- [ ] Feedback spreadsheet created (issue, category, priority)
- [ ] Bugs triaged and assigned
- [ ] Enhancement backlog created
- [ ] Team sync scheduled (weekly for first month)
- [ ] Phase 2 features documented

**Subtasks:**
1. Set up GitHub Issues template
2. Monitor feedback sources
3. Create feedback spreadsheet
4. Triage bugs (P0/P1/P2)
5. Prioritize enhancements
6. Schedule weekly team sync
7. Document learnings

**Dependencies:** Task 5.2.1  
**Blocks:** Phase 2 planning

**Definition of Done:**
- Feedback collection system active
- Bugs triaged
- Enhancement backlog created

---

**Phase 5 Summary:**
- ✅ Textbook publicly launched
- ✅ All systems operational and monitored
- ✅ Community feedback collection active
- ✅ Phase 2 roadmap planned

**Phase 5 Sign-Off Date:** 2026-01-23 (target)

---

## Future Phase 2 Features (Post-Launch)

### 6.1 Optional Enhancement Features

#### Task 6.1.1 🔵 P3: Urdu Translation
**Owner:** Translator + Content Writer  
**Effort:** TBD  
**Status:** Blocked (Phase 2)

**Description:**
Translate all chapters to Urdu with RTL layout support and searchable Urdu index.

**Acceptance Criteria:**
- [ ] All chapters professionally translated to Urdu
- [ ] RTL layout implemented in Docusaurus
- [ ] Qdrant index updated with Urdu embeddings
- [ ] Search functional in both English and Urdu

**Dependencies:** Phase 1 MVP complete  
**Blocks:** None

---

#### Task 6.1.2 🔵 P3: Learner Personalization
**Owner:** Backend Engineer  
**Effort:** TBD  
**Status:** Blocked (Phase 2)

**Description:**
Add user profiles, personalized responses, and reading history.

**Acceptance Criteria:**
- [ ] User profile system (difficulty level, role)
- [ ] Personalized RAG responses based on profile
- [ ] Reading history tracking
- [ ] Optional: User authentication

**Dependencies:** Phase 1 MVP complete  
**Blocks:** None

---

#### Task 6.1.3 🔵 P3: Advanced RAG Features
**Owner:** Backend Engineer  
**Effort:** TBD  
**Status:** Blocked (Phase 2)

**Description:**
Enhance RAG with hybrid search, reranking, and conversation memory.

**Acceptance Criteria:**
- [ ] Hybrid semantic + keyword search
- [ ] Response reranking
- [ ] Conversation memory (multi-turn)
- [ ] Improved answer quality

**Dependencies:** Phase 1 MVP complete  
**Blocks:** None

---

#### Task 6.1.4 🔵 P3: Community Features
**Owner:** Community Lead  
**Effort:** TBD  
**Status:** Blocked (Phase 2)

**Description:**
Add Discord integration, community Q&A archive, and contribution guidelines.

**Acceptance Criteria:**
- [ ] Discord bot for Q&A
- [ ] Community Q&A archive
- [ ] Translation contribution guidelines
- [ ] Community feedback loop

**Dependencies:** Phase 1 MVP complete + community size > 100  
**Blocks:** None

---

---

## Task Summary & Metrics

### By Priority Level

| Priority | Count | Est. Hours | Phase |
|----------|-------|-----------|-------|
| 🔴 P0 (Blocking) | 4 | 8 | 1, 4, 5 |
| 🟡 P1 (Critical/MVP) | 38 | 92 | 1–5 |
| 🟢 P2 (Important) | — | — | — |
| 🔵 P3 (Nice-to-have) | 4 | TBD | 6 (Phase 2) |
| **TOTAL** | **46** | **~100 hours** | **8 weeks** |

### By Role

| Role | Tasks | Est. Hours |
|------|-------|-----------|
| Backend Engineer | 10 | 20 |
| Frontend Engineer | 5 | 8 |
| Content Writer | 7 | 40 |
| DevOps Engineer | 7 | 8 |
| QA Engineer | 5 | 10 |
| Technical Reviewer | 3 | 6 |
| Technical Illustrator | 1 | 4 |
| Marketing Lead | 1 | 2 |
| **TOTAL** | **42** | **~100 hours** |

### By Phase Completion

| Phase | Weeks | Tasks | Status |
|-------|-------|-------|--------|
| Phase 1: Foundation | Week 1 | 7 | Not Started |
| Phase 2: Content | Weeks 2–4 | 9 | Not Started |
| Phase 3: RAG Backend | Weeks 5–6 | 9 | Not Started |
| Phase 4: Testing | Week 7 | 8 | Not Started |
| Phase 5: Launch | Week 8 | 6 | Not Started |
| **Phase 2 (Future)** | **TBD** | **4** | **Blocked** |

---

## Dependencies & Critical Path

```
Week 1:
├─ 1.1.1 (Create GitHub Repo) 🔴 P0
│  └─ 1.1.2 (Init Docusaurus) 🟡 P1
│     └─ 1.1.3 (GitHub Actions) 🟡 P1
│        └─ 1.1.4 (Secrets) 🟡 P1
│           ├─ 1.2.1 (Qdrant) 🟡 P1
│           ├─ 1.2.2 (PostgreSQL) 🟡 P1
│           └─ 1.2.3 (FastAPI) 🟡 P1

Weeks 2–4 (Parallel):
├─ 2.1.1 (Content Outline) 🔴 P0
│  └─ 2.1.2 (Writing Workflow) 🟡 P1
│     └─ 2.2.1–2.2.6 (Write Chapters) 🟡 P1
│        └─ 2.3.1 (Create Diagrams) 🟡 P1

Weeks 5–6:
├─ 3.1.1 (Ingestion Script) 🟡 P1
│  └─ 3.1.2 (GitHub Actions Ingest) 🟡 P1
│     └─ 3.2.1 (Query Endpoint) 🟡 P1
│        └─ 3.2.2 (Validation) 🟡 P1
│           └─ 3.3.1–3.3.3 (Widget) 🟡 P1

Week 7:
├─ 4.1.1 (Integration Tests) 🟡 P1
├─ 4.1.2 (Accuracy Audit) 🔴 P0
├─ 4.2.1–4.2.2 (Perf & Access) 🟡 P1
└─ 4.3.1–4.3.2 (Security & Resilience) 🟡 P1

Week 8:
├─ 5.1.1 (Content Review) 🔴 P0
├─ 5.1.2 (Infrastructure Check) 🔴 P0
├─ 5.1.3 (Docs Review) 🟡 P1
├─ 5.2.1 (Public Launch) 🟡 P1
└─ 5.3.1–5.3.2 (Monitoring & Feedback) 🟡 P1
```

**Critical Path (Blocking Items):**
1. GitHub repository creation (Task 1.1.1)
2. Content outline (Task 2.1.1)
3. All chapters written (Task 2.2.6)
4. Accuracy audit (Task 4.1.2)
5. Content review (Task 5.1.1)
6. Infrastructure check (Task 5.1.2)
7. Public launch (Task 5.2.1)

---

## Document Status & Sign-Off

**Document Status:** ✅ Production-Ready Task List  
**Created:** 2025-12-05  
**Last Updated:** 2025-12-05  

**Task List Prepared By:** Project Manager  
**Reviewed By:** Technical Lead  
**Approved By:** [Project Lead Signature]

---

## How to Use This Document

1. **Weekly Planning:** Review tasks in current phase at start of week
2. **Task Assignment:** Assign tasks to team members by role
3. **Progress Tracking:** Update task status (Not Started → In Progress → Completed)
4. **Blocking Issues:** Flag P0 tasks if blocked; escalate immediately
5. **Sign-Off:** Collect sign-off from task owner when complete
6. **Phase Transitions:** Complete all phase tasks before moving to next phase

**Next Action:** Begin Phase 1 tasks (Week 1 starting 2025-12-05)

# Feature Specification: AI-Native Textbook with RAG Chatbot

**Project Name:** Physical AI & Humanoid Robotics — Essentials  
**Format:** Docusaurus v3 + FastAPI + Qdrant RAG  
**Target Audience:** Beginners to intermediate learners  
**Primary Language:** English (with optional Urdu translation)  
**Infrastructure:** 100% Free-tier services  
**Created:** 2025-12-05  
**Status:** Production-Ready Specification

---

## User Scenarios & Testing *(Mandatory)*

### User Story 1: Learner Reads Textbook Chapter (Priority: P1)

**User Journey:**
A beginner learns about Physical AI and humanoid robotics by reading well-structured chapters. They navigate the textbook using a clean sidebar, find specific content via search, and read minimalist, diagram-rich explanations. All chapters load fast even on low-bandwidth connections.

**Why This Priority:** Core feature; textbook readability is foundational to entire project success.

**Independent Test:** 
Fully testable by deploying Docusaurus on GitHub Pages, opening a chapter, verifying readable content, and confirming sidebar navigation works. Delivers immediate learning value without RAG dependency.

**Acceptance Scenarios:**

1. **Given** user opens Chapter 1 textbook, **When** page loads, **Then** content displays within 2 seconds and sidebar navigation is visible
2. **Given** user clicks Chapter 2 in sidebar, **When** navigation occurs, **Then** user is directed to Chapter 2 without page reload failure
3. **Given** user opens dark mode toggle, **When** toggled on, **Then** page renders in dark theme with readable contrast (WCAG 2.1 AA)
4. **Given** user searches for "ROS nodes" via search box, **When** query submitted, **Then** search returns results linking to Chapter 3 Section 2
5. **Given** user views on mobile device, **When** page loads, **Then** layout is responsive and readable at 320px width

---

### User Story 2: Learner Uses RAG Chatbot to Ask Questions (Priority: P1)

**User Journey:**
A learner selects text from Chapter 4 about Gazebo, clicks "Ask AI", and the chatbot answers specifically from that chapter with exact citations. The response is fast, accurate, and includes source chapter/section reference.

**Why This Priority:** RAG chatbot is key differentiator; deterministic, grounded answers are core promise.

**Independent Test:**
Testable with pre-populated Qdrant index and FastAPI backend running. Submit sample questions, verify responses cite exact text from book, and confirm no external knowledge is used. Works independently of full Docusaurus build.

**Acceptance Scenarios:**

1. **Given** user selects text "digital twins enable safe exploration", **When** "Ask AI" button clicked, **Then** chatbot responds with explanation grounded in Chapter 4
2. **Given** user asks question not covered in textbook (e.g., "quantum computing"), **When** chatbot processes query, **Then** response explicitly states: "This topic is not covered in the textbook"
3. **Given** chatbot generates response, **When** response displays, **Then** citation includes "Chapter [#], Section [Title]" and exact quote from source text
4. **Given** user submits question, **When** RAG processes query, **Then** response returns within 1 second
5. **Given** user asks follow-up question, **When** chatbot responds, **Then** context from previous question is NOT carried over (deterministic per-query, no memory)

---

### User Story 3: Developer Deploys Textbook on GitHub Pages (Priority: P1)

**User Journey:**
A developer clones the repository, runs build commands, and the textbook deploys automatically to GitHub Pages via GitHub Actions. Build succeeds without errors, pages render cleanly, and deployment requires zero manual steps.

**Why This Priority:** Deployment automation is non-negotiable; enables contributor participation and CI/CD reliability.

**Independent Test:**
Testable by cloning repo, running `npm run build`, verifying output folder, and simulating GitHub Actions workflow. Works without RAG backend present.

**Acceptance Scenarios:**

1. **Given** developer runs `npm run build`, **When** command executes, **Then** build completes without errors in < 30 seconds
2. **Given** build succeeds, **When** `build/` folder generated, **Then** folder contains valid HTML, CSS, JS for all 6 chapters
3. **Given** GitHub Actions workflow triggered on main branch push, **When** workflow runs, **Then** deployment to GitHub Pages succeeds and pages become publicly accessible
4. **Given** contributor modifies chapter markdown, **When** PR is merged to main, **Then** GitHub Actions automatically rebuilds and redeploys without manual intervention
5. **Given** build process encounters error (e.g., broken link), **When** build fails, **Then** error message clearly identifies issue location (file + line number)

---

### User Story 4: RAG Backend Ingests Textbook Content (Priority: P1)

**User Journey:**
During deployment, a Python script automatically extracts all 6 chapters from markdown, chunks text into 512-1024 token chunks, generates embeddings using a lightweight model, and stores chunks + embeddings in Qdrant and PostgreSQL. Process is fully automated and requires zero manual content management.

**Why This Priority:** Automated ingestion enables scalable maintenance and chapter updates without manual re-indexing.

**Independent Test:**
Testable by providing sample chapter markdown, running ingestion script, querying Qdrant for retrieved chunks, and verifying PostgreSQL metadata. Works independently of Docusaurus build.

**Acceptance Scenarios:**

1. **Given** ingestion script runs on 6 chapters, **When** processing completes, **Then** Qdrant contains ≤ 2,000 total chunks across all chapters
2. **Given** a chunk "Gazebo uses URDF files for robot description", **When** embedded and stored, **Then** chunk is retrievable by semantic query "robot file format"
3. **Given** ingestion process executes, **When** completed, **Then** PostgreSQL metadata table contains chapter/section references for all chunks
4. **Given** chapter markdown is updated (e.g., typo fix), **When** ingestion reruns, **Then** previous version is replaced without duplication
5. **Given** ingestion completes, **When** queried for embeddings, **Then** all embeddings generated using consistent lightweight model (e.g., all-MiniLM-L6-v2)

---

### User Story 5: Optional — Learner Toggles Urdu Translation (Priority: P2)

**User Journey:**
An Urdu-speaking learner clicks "Urdu/English" toggle button in navbar. Chapter content automatically translates to Urdu while RTL layout is applied. Sidebar, search, and chatbot also respond in Urdu. User can toggle back to English without loss of reading position.

**Why This Priority:** Inclusive accessibility; high cultural impact but non-blocking for MVP.

**Independent Test:**
Testable with translation layer pre-built, toggling UI button, and verifying content rendering in both languages. Works with mockup translated content.

**Acceptance Scenarios:**

1. **Given** user clicks "Urdu" button in navbar, **When** toggle activates, **Then** all chapter content displays in Urdu with RTL layout applied
2. **Given** user in Urdu mode searches for term, **When** search executes, **Then** results display in Urdu with Urdu-language chapter titles
3. **Given** user in Urdu mode selects text and clicks "Ask AI", **When** chatbot processes, **Then** response is generated in Urdu from English retrieval
4. **Given** user switches back to English, **When** toggle clicks English, **Then** layout reverts to LTR and content is in English
5. **Given** user is on Section 3 of Chapter 2 in Urdu, **When** switches to English, **Then** user remains on same chapter/section (scroll position preserved as much as possible)

---

### User Story 6: Optional — Learner Personalizes Learning Difficulty (Priority: P2)

**User Journey:**
A learner creates optional profile, selects reading difficulty level (Basic/Normal/Advanced), and role (Developer/Student/Robotics Enthusiast). Textbook displays personalized summaries, and RAG chatbot tailors explanations to learner's level. Preference is persisted across sessions.

**Why This Priority:** Enhances engagement but optional; MVP can omit initially.

**Independent Test:**
Testable with mock profile data in PostgreSQL, toggling difficulty levels in UI, and verifying different response content is returned by RAG. Works without authentication system.

**Acceptance Scenarios:**

1. **Given** learner selects "Basic" difficulty, **When** Chapter 1 renders, **Then** explanations use simpler language and skip advanced math/equations
2. **Given** learner profile is "Developer" role, **When** RAG chatbot responds about ROS 2, **Then** response emphasizes code examples over theory
3. **Given** learner saves profile, **When** returning to site on same browser, **Then** previous difficulty and role preferences are remembered
4. **Given** learner selects "Advanced" difficulty, **When** requesting explanation, **Then** response includes formal terminology, equations, and references to research papers
5. **Given** learner switches from "Advanced" to "Basic", **When** requesting same query, **Then** response is regenerated at lower difficulty level

---

## Requirements *(Mandatory)*

### Functional Requirements — Textbook (Docusaurus Frontend)

- **FR-001:** Textbook MUST contain exactly 6 chapters: Ch1 (Physical AI), Ch2 (Humanoid Robotics), Ch3 (ROS 2), Ch4 (Digital Twin), Ch5 (VLA), Ch6 (Capstone)
- **FR-002:** Each chapter MUST be 1,000–1,500 words, organized into 3–5 sections, with 2–4 diagrams
- **FR-003:** Sidebar navigation MUST auto-generate from `/docs` folder structure with chapter hierarchy
- **FR-004:** Dark/light mode toggle MUST be functional and persist user preference in localStorage
- **FR-005:** Search functionality MUST be full-text across all chapter content using Docusaurus search-local plugin
- **FR-006:** All diagrams MUST be SVG or optimized PNG (< 200KB each) with alt text and captions
- **FR-007:** Page load time MUST be < 2 seconds (measured on GitHub Pages from US-East)
- **FR-008:** Responsive design MUST support 320px (mobile) to 1920px (desktop) screen widths
- **FR-009:** Syntax highlighting MUST be enabled for code blocks using Prism.js
- **FR-010:** Accessibility MUST meet WCAG 2.1 AA standard (contrast ratios, heading hierarchy, alt text)
- **FR-011:** Build process MUST complete in < 30 seconds using `npm run build` command
- **FR-012:** GitHub Pages deployment MUST occur automatically via GitHub Actions on main branch push
- **FR-013:** All links (internal + external) MUST be valid and functional

### Functional Requirements — RAG Chatbot Backend

- **FR-014:** RAG chatbot MUST accept user queries via FastAPI `/query` endpoint (POST)
- **FR-015:** Query embedding MUST be generated using lightweight model (all-MiniLM-L6-v2 or equivalent, CPU-only)
- **FR-016:** Qdrant search MUST retrieve top-3 semantically relevant chunks from textbook
- **FR-017:** LLM response generation MUST use only retrieved chunks; NO external knowledge, NO web search
- **FR-018:** Chatbot response MUST include verbatim citation: chapter number, section title, and exact text quote
- **FR-019:** If query is out-of-scope, response MUST explicitly state: "This topic is not covered in the textbook"
- **FR-020:** Query response time MUST be < 1 second (embedding + retrieval + generation)
- **FR-021:** RAG system MUST NOT have GPU dependency; all compute must run on CPU
- **FR-022:** Qdrant storage MUST remain within free-tier limits (≤ 2,000 chunks, ≤ 1GB storage)
- **FR-023:** PostgreSQL metadata table MUST store chunk_id, chapter, section, embedding_id, created_at
- **FR-024:** Chatbot MUST accept optional system prompt constraint: "Answer ONLY from retrieved book chunks"
- **FR-025:** RAG ingestion pipeline MUST run automatically on deployment, updating Qdrant + PostgreSQL

### Functional Requirements — Frontend Integration

- **FR-026:** Docusaurus page MUST include floating "Select text → Ask AI" widget
- **FR-027:** Widget MUST capture selected text and submit to FastAPI backend
- **FR-028:** Chatbot response MUST display in-page dialog with citation block visible
- **FR-029:** Each conversation turn MUST be independent (no memory across queries)
- **FR-030:** Widget MUST be dismissible and remain hidden after dismissal (localStorage preference)

### Functional Requirements — Deployment & Infrastructure

- **FR-031:** All services MUST be free-tier only: Qdrant Cloud (free), Neon PostgreSQL (free), GitHub Pages (free)
- **FR-032:** FastAPI backend MUST be deployable on Vercel free tier OR alternative free hosting (Railway, Render)
- **FR-033:** GitHub Actions workflow MUST automate: build → test → deploy to GitHub Pages
- **FR-034:** Repository MUST include `README.md` with deployment instructions and architecture diagram
- **FR-035:** Environment variables MUST be stored securely (GitHub Secrets for API keys, Qdrant endpoint)
- **FR-036:** Build MUST reject PRs with broken links, missing alt text, or accessibility violations

### Functional Requirements — Optional Features (Urdu Translation)

- **FR-037:** Navbar MUST include "English / Urdu" toggle button
- **FR-038:** Translation layer MUST translate chapter content on-the-fly using free API (e.g., Google Translate API)
- **FR-039:** RTL layout MUST be applied when Urdu mode active (sidebar, text direction, margins)
- **FR-040:** Search queries in Urdu MUST be translated to English before Qdrant retrieval, then results translated back
- **FR-041:** User language preference MUST persist in localStorage

### Functional Requirements — Optional Features (Personalization)

- **FR-042:** Optional user profile MUST allow selection of reading difficulty (Basic/Normal/Advanced)
- **FR-043:** Profile MUST store role selection (Developer/Student/Robotics Enthusiast)
- **FR-044:** RAG chatbot MUST accept optional `difficulty` and `role` parameters in query
- **FR-045:** Response content MUST be tailored to learner profile (simpler language for Basic, code-heavy for Developer)
- **FR-046:** Profile preference MUST persist in Neon PostgreSQL (optional login) or localStorage (anonymous)

---

## Content Structure *(Mandatory)*

### Chapter 1: Introduction to Physical AI
**Word Count:** 1,000–1,500 | **Sections:** 3–5 | **Diagrams:** 2–4

- **Section 1:** Definition and scope of Physical AI
- **Section 2:** Differentiation from classical AI and symbolic systems
- **Section 3:** Real-world examples (warehouse robots, humanoid robots, embodied agents)
- **Section 4:** Why physical embodiment matters for learning
- **Diagram 1:** Classical AI vs. Physical AI comparison
- **Diagram 2:** Real-world robot applications (warehouse, humanoid, manipulator)

### Chapter 2: Basics of Humanoid Robotics
**Word Count:** 1,000–1,500 | **Sections:** 3–5 | **Diagrams:** 2–4

- **Section 1:** Robot morphology and degrees of freedom
- **Section 2:** Kinematics and dynamics fundamentals (non-mathematical overview)
- **Section 3:** Sensors (vision, proprioception, force/torque) and actuators (motors, servos)
- **Section 4:** Control loops and feedback mechanisms
- **Section 5:** Balance and locomotion basics
- **Diagram 1:** Humanoid robot anatomy (joints, DOF labels)
- **Diagram 2:** Sensor and actuator placement on robot body

### Chapter 3: ROS 2 Fundamentals
**Word Count:** 1,000–1,500 | **Sections:** 3–5 | **Diagrams:** 2–4

- **Section 1:** ROS 2 architecture (nodes, topics, services, actions)
- **Section 2:** QoS profiles and DDS layer basics
- **Section 3:** Executors and async execution model
- **Section 4:** Python rclpy basics with minimal working example
- **Section 5:** Best practices for lightweight ROS 2 deployments
- **Code Example 1:** Simple ROS 2 subscriber node (≤ 20 lines)
- **Diagram 1:** ROS 2 pub/sub architecture
- **Diagram 2:** Service and action call flow

### Chapter 4: Digital Twin Simulation
**Word Count:** 1,000–1,500 | **Sections:** 3–5 | **Diagrams:** 2–4

- **Section 1:** Digital twin concept and benefits for robotics
- **Section 2:** Gazebo basics (URDF, SDF, physics plugins)
- **Section 3:** Isaac Sim basics (USD format, articulation models)
- **Section 4:** Lightweight workflows for free-tier users
- **Section 5:** Simulation-to-reality considerations
- **Code Example 1:** Minimal Gazebo launch file
- **Diagram 1:** Digital twin workflow (CAD → Sim → Hardware)
- **Diagram 2:** Gazebo plugin architecture

### Chapter 5: Vision-Language-Action (VLA) Systems
**Word Count:** 1,000–1,500 | **Sections:** 3–5 | **Diagrams:** 2–4

- **Section 1:** Vision-language models (VLM) for robot perception
- **Section 2:** Action policies and decision-making
- **Section 3:** VLA control loops and task grounding
- **Section 4:** Latency, safety, and grounding considerations
- **Section 5:** Free-tier VLM options (open-source, quantized models)
- **Diagram 1:** VLA perception-action loop
- **Diagram 2:** VLM inference pipeline with grounding annotations

### Chapter 6: Capstone — Minimal AI→Robot Pipeline
**Word Count:** 1,000–1,500 | **Sections:** 3–5 | **Diagrams:** 2–4

- **Section 1:** End-to-end system architecture
- **Section 2:** VLM prompt engineering for robotics tasks
- **Section 3:** ROS 2 policy execution (mapping VLM output to actions)
- **Section 4:** Digital twin validation before hardware deployment
- **Section 5:** Free-tier constraints and best practices
- **Code Example 1:** Simple VLM → ROS 2 action pipeline (≤ 30 lines total)
- **Diagram 1:** Full pipeline: VLM → decision → ROS 2 action
- **Diagram 2:** Hardware deployment workflow (sim → real)

---

## Technical Specifications

### Docusaurus Configuration

**Directory Structure:**
```
physical-ai-textbook/
├── docs/
│   ├── intro.md
│   ├── chapter-1/
│   │   ├── _category_.json
│   │   ├── section-1.md
│   │   ├── section-2.md
│   │   └── ...
│   ├── chapter-2/ ... chapter-6/
│   └── resources/
│       ├── glossary.md
│       └── references.md
├── src/
│   ├── components/
│   │   ├── ChatbotWidget.tsx
│   │   └── CitationBlock.tsx
│   ├── css/custom.css
│   └── pages/
├── static/
│   ├── diagrams/
│   └── code-examples/
├── docusaurus.config.js
├── sidebars.js
├── package.json
└── .github/workflows/deploy.yml
```

**Build Command:** `npm run build`  
**Output:** Static HTML in `/build` folder  
**Deployment Target:** GitHub Pages  
**Build Time Requirement:** < 30 seconds  
**Page Load Time Requirement:** < 2 seconds

### RAG Backend Configuration

**API Endpoint:** `/api/query` (POST)  
**Request Payload:**
```json
{
  "query": "What is a digital twin?",
  "difficulty": "normal",
  "role": "student",
  "language": "english"
}
```

**Response Payload:**
```json
{
  "answer": "A digital twin is a virtual replica...",
  "sources": [
    {
      "chapter": 4,
      "section": "Digital Twin Concept",
      "quote": "A digital twin is a virtual replica..."
    }
  ],
  "confidence": 0.95,
  "retrieval_time_ms": 850
}
```

**Dependencies (Free-Tier):**
- FastAPI
- Qdrant Python client
- psycopg2 (PostgreSQL)
- sentence-transformers (all-MiniLM-L6-v2)
- openai (or similar LLM API with free tier)

---

## Edge Cases

- **What happens when user queries topic not in textbook?** System returns: "This topic is not covered in the textbook. Please refer to [related chapter]."
- **What happens if Qdrant is temporarily down?** Backend returns 503 Service Unavailable; frontend displays: "Chat service temporarily unavailable. Try again shortly."
- **What happens if embedding generation fails?** Fallback to keyword-based search on PostgreSQL metadata
- **What happens if user selects text from code block?** Widget still appears and processes selected code as query text
- **What happens if RAG returns multiple contradictory answers from different chapters?** System returns highest-confidence match with caveat: "Multiple interpretations exist in the textbook. See sources for alternatives."

---

## Success Criteria ✅

- ✅ All 6 chapters written, reviewed, and published on GitHub Pages
- ✅ Docusaurus build completes without errors in < 30 seconds
- ✅ Textbook loads in < 2 seconds on GitHub Pages (measured from US-East)
- ✅ RAG chatbot returns grounded answers with 100% citation accuracy
- ✅ Zero hallucinations; all responses verifiable from book text
- ✅ Query response time < 1 second consistently
- ✅ GitHub Actions deployment workflow fully automated
- ✅ Zero paid services used; 100% free-tier infrastructure
- ✅ Accessibility audit passes WCAG 2.1 AA
- ✅ Mobile responsiveness verified on iOS Safari + Android Chrome
- ✅ RAG ingestion pipeline runs automatically on deployment

---

**Version:** 1.0 | **Created:** 2025-12-05 | **Status:** Production-Ready

---

# Clarification Document: Physical AI & Humanoid Robotics — Essentials

**Project:** Physical AI & Humanoid Robotics — Essentials Textbook + RAG Chatbot  
**Date Created:** 2025-12-05  
**Status:** Active Clarification Phase  
**Purpose:** Resolve ambiguities, document assumptions, and capture key decisions

---

## I. Clarification of Unclear Points

### 1. RAG Chatbot LLM Provider — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "LLM (small hosted model, e.g., OpenAI / Claude free-tier) generates answer"

**Clarification:**
- **Selected Option:** Use OpenAI GPT-4o-mini free tier (currently $0.15 per 1M input tokens, sufficient for MVP)
- **Fallback Option 1:** Claude 3.5 Haiku (low-cost alternative if OpenAI unavailable)
- **Fallback Option 2:** Open-source local LLM (Mistral 7B quantized, runs on CPU, no API cost)
- **Rationale:** OpenAI has best free-tier accessibility; Claude is premium but affordable; local option ensures full free-tier compliance
- **Decision Required:** Confirm LLM provider preference before implementation starts
- **Cost Estimate:** ~$5-15/month for typical textbook usage (manageable even if not free)

**Remaining Question:** Should we prioritize **full free-tier compliance** (local LLM only) or **ease of deployment** (OpenAI API)?

---

### 2. Embedding Model Selection — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "Embeddings minimized (≤ 2K total chunks recommended)" but embedding model not specified

**Clarification:**
- **Selected Option:** sentence-transformers/all-MiniLM-L6-v2 (384-dim embeddings, ~22MB model)
- **Rationale:** 
  - Runs on CPU (no GPU needed)
  - Fast inference (< 100ms per chunk)
  - 384-dim embeddings fit comfortably in Qdrant free tier
  - Production-proven for semantic search
- **Chunk Size:** 512 tokens per chunk (optimal for retrieval, ~2,000 total across 6 chapters)
- **Storage Estimate:** ~1.5GB in Qdrant (well under free-tier 1GB limit with optimizations)
- **Decision:** Confirmed — no changes needed

---

### 3. RAG Response Generation Constraints — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "Answer ONLY from retrieved chunks" — How strictly enforced?

**Clarification:**
- **Constraint Level 1 (Hard Constraint):** LLM MUST only reference retrieved chunks; system prompt explicitly forbids external knowledge
- **Constraint Level 2 (Validation):** Post-generation validation checks if response references only source chunks
- **Constraint Level 3 (Safety):** If LLM hallucinates, fallback to "This topic requires more context. See: [Chapter X, Section Y]"
- **Implementation:** System prompt + retrieval context will be formatted as:

```
You are a textbook assistant. Answer ONLY using the provided textbook excerpts.
If the question cannot be answered from these excerpts, respond: "This topic is not covered in the textbook."

Textbook Excerpts:
---
[Top-3 retrieved chunks with chapter/section labels]
---

User Question: [question]
```

- **Decision:** Implement all three constraint levels; prioritize hard constraint

---

### 4. Docusaurus Deployment Target — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "GitHub Pages deployment" but exact workflow unclear

**Clarification:**
- **Primary Target:** GitHub Pages (free, reliable, static-friendly)
- **Build Output:** `/build` folder (HTML only, no Node.js server)
- **GitHub Actions Trigger:** Auto-deploy on main branch push
- **URL Format:** `https://[org-name].github.io/physical-ai-textbook/`
- **Build Cache:** Enabled to speed up repeat builds (< 30s target)
- **Domain:** Custom domain optional (e.g., `textbook.physical-ai.org`)
- **SSL/TLS:** GitHub Pages provides free SSL certificate
- **Workflow File:** `.github/workflows/deploy.yml` (auto-build on push)
- **Decision:** Confirmed — standard GitHub Pages deployment

---

### 5. Free-Tier Infrastructure Stack — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "100% free-tier services" but which services exactly?

**Clarification:**

| Service | Component | Free Tier Details | Cost/Month |
|---------|-----------|-------------------|-----------|
| **GitHub Pages** | Textbook hosting | Unlimited static sites | $0 |
| **GitHub Actions** | CI/CD pipeline | 2,000 free minutes/month | $0 |
| **Qdrant Cloud** | Vector database | 1GB storage, 10K requests/month | $0 |
| **Neon PostgreSQL** | Metadata storage | 3GB storage, 5M compute units/month | $0 |
| **Vercel/Railway** | FastAPI backend | Free tier with deployment limits | $0 |
| **OpenAI API** | LLM responses | Pay-per-token ($0.15/1M tokens) | $5-15* |

*Note: OpenAI API cost may exceed free tier; fallback to local LLM if needed*

- **Decision:** All services confirmed free; OpenAI cost is acceptable MVP trade-off

---

### 6. Chapter Content Completeness — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "Each chapter 1,000–1,500 words" but what if topics require more depth?

**Clarification:**
- **Core Content:** 1,000–1,500 words per chapter (mandatory)
- **Extended Content:** Optional "Deep Dive" subsections (not counted in word limit, marked as optional)
- **Code Examples:** ≤ 20 lines (inline); full code examples linked to GitHub repository
- **Rationale:** Minimize page bloat for RAG retrieval efficiency; enable full-depth exploration via external links
- **Decision:** Confirmed — maintain strict chapter word limits; provide extension links

---

### 7. Urdu Translation Implementation — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "Toggle button: Urdu/English" but real-time translation overhead unclear

**Clarification:**

**Option A: Static Pre-Translated Content (Recommended)**
- Chapters manually translated by native Urdu speaker
- Both English + Urdu versions stored in Docusaurus
- Sidebar toggle loads full Urdu chapter
- No runtime cost; fast loading
- Trade-off: Requires upfront translation effort

**Option B: Runtime Translation (API-based)**
- English chapters served; translation happens on button click
- Uses Google Translate API free tier
- Slower (2-3 second translation delay)
- Cheaper upfront (no manual translation needed)
- Trade-off: Quality depends on API; adds latency

**Decision:** Recommend **Option A** (pre-translated) for Phase 2; defer to Phase 1 MVP

---

### 8. RAG Chunk Retrieval Strategy — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "Top-k book chunks" but what is optimal k value?

**Clarification:**
- **k (Number of Chunks to Retrieve):** 3 chunks per query
- **Rationale:** 
  - 1-2 chunks: Often insufficient context
  - 3 chunks: Sweet spot (300-3,000 tokens context)
  - 4+ chunks: Increases latency, diminishing returns
- **Reranking:** Optional post-retrieval reranking to prioritize most relevant chunk
- **Fallback:** If < 3 semantically relevant chunks found, return fewer (don't pad with low-quality results)
- **Decision:** k=3 confirmed; reranking optional for Phase 2

---

### 9. Learner Personalization Storage — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "Personalized learning profile" but how to handle anonymous users?

**Clarification:**
- **Authenticated Users:** Profile stored in Neon PostgreSQL (requires optional login)
- **Anonymous Users:** Profile stored in browser localStorage (no login required)
- **Cross-Device Sync:** Not supported in MVP (localStorage is per-device)
- **Privacy:** Profiles do NOT store user identity; only preferences (difficulty, role)
- **Data Retention:** localStorage cleared on browser cache clear; DB profiles deletable on request
- **Decision:** Implement both paths; default to anonymous (localStorage) for ease of use

---

### 10. Success Criteria Metrics — NEEDS CLARIFICATION RESOLVED ✅

**Original Ambiguity:** "Success criteria" listed but measurement methods unclear

**Clarification:**

| Criterion | Measurement Method | Target | Frequency |
|-----------|-------------------|--------|-----------|
| Textbook builds without errors | `npm run build` exit code | 0 (success) | Every push |
| Build time < 30s | GitHub Actions logs | < 30 seconds | Every push |
| Page load < 2s | Lighthouse, PageSpeed Insights | < 2 seconds | Weekly |
| RAG response < 1s | API response time logging | < 1 second avg | Real-time |
| RAG accuracy | Manual audit of 20 queries | 100% citations correct | Monthly |
| Accessibility passes WCAG 2.1 AA | axe-core automated scan | 0 errors | Every push |
| Mobile responsiveness | BrowserStack testing | Works on iOS 12+, Android 8+ | Monthly |
| All 6 chapters published | Manual checklist | 6/6 chapters live | Final milestone |
| Zero hallucinations | Human review of chatbot responses | 0 hallucinations in 100 queries | Monthly audit |
| Free-tier only services | Cost tracking | $0 (or minimal < $20/month) | Monthly |

- **Decision:** Implement automated monitoring for build + performance; monthly manual audits for RAG quality

---

## II. Assumed Design Decisions

### Assumption 1: Chapter Length Trade-off
**Assumption:** 1,000–1,500 words per chapter is sufficient for textbook learning
**Rationale:** Minimizes RAG chunk explosion; forces clarity and conciseness; full courses provide external links
**Risk:** May oversimplify complex topics (e.g., ROS 2 lifecycle)
**Mitigation:** "Deep Dive" optional sections address advanced learners

### Assumption 2: Semantic Search Sufficiency
**Assumption:** Semantic search (embeddings) is sufficient for Q&A retrieval
**Rationale:** all-MiniLM-L6-v2 proven on academic/technical text
**Risk:** May miss specific queries requiring keyword matching
**Mitigation:** Implement fallback hybrid search (semantic + keyword) in Phase 2

### Assumption 3: Single-Turn QA Model
**Assumption:** Each query is independent; no conversation memory
**Rationale:** Simplifies backend; deterministic responses; no cost for context storage
**Risk:** Users may want follow-up questions on same topic
**Mitigation:** Suggestion: "See also: [related chapter]" links in response

### Assumption 4: Free-Tier LLM Cost Acceptable
**Assumption:** OpenAI API cost (< $20/month for MVP) acceptable despite "free-tier" goal
**Rationale:** Local LLM alternative available but more complex; OpenAI prioritizes UX
**Risk:** If budget unavailable, project must switch to local LLM
**Mitigation:** Document fallback to Mistral 7B quantized model

### Assumption 5: Docusaurus Static Generation Only
**Assumption:** Textbook is fully static HTML (no server-side rendering)
**Rationale:** GitHub Pages only supports static sites; faster build; simpler deployment
**Risk:** Dynamic features (e.g., user accounts, real-time tracking) not supported
**Mitigation:** Personalization can use localStorage (client-side) or external backend for advanced features

---

## III. Key Decisions Documented

### Decision 1: Minimize Dependencies Strategy
**Context:** "≤ 50 dependencies across entire project" — why so strict?

**Decision Made:** Reduce dependency surface for:
- **Security:** Fewer packages = fewer vulnerability vectors
- **Build Speed:** Faster npm install + build
- **Maintenance:** Easier to keep dependencies updated
- **Free-tier Compatibility:** Some services limit package count

**Implementation:**
- Docusaurus (main package) brings ~100 deps, but this is acceptable (framework baseline)
- RAG backend (FastAPI + dependencies): ~20-30 deps
- Total: ~150 deps (relaxed from ≤50 to ≤150 for realistic MVP)
- Action: Audit dependencies quarterly; remove unused packages

---

### Decision 2: No GPU Anywhere Rationale
**Context:** "Zero GPU dependency; all compute must run on CPU" — strict requirement

**Decision Made:** 
- **Embeddings:** all-MiniLM-L6-v2 runs on CPU (~100ms inference)
- **LLM:** Use API-based LLM (OpenAI, Claude) OR quantized local model (Mistral 7B)
- **Qdrant Search:** CPU-efficient vector search algorithm
- **Rationale:** Democratizes access (anyone can run/host) + free-tier services (no GPU access)

---

### Decision 3: Citation-First RAG Design
**Context:** "Chatbot answers ONLY from book's text" — how enforce?

**Decision Made:**
- **System Prompt Constraint:** Explicit instruction to cite sources
- **Post-Generation Validation:** Check if response references only retrieved chunks
- **User Display:** Always show source chapter + section + exact quote
- **Transparency:** If LLM hallucinates, system detects and flags as unverified
- **Rationale:** Builds trust; enables verification; differentiates from general search engines

---

### Decision 4: Staged Feature Release Strategy
**Context:** Optional features (Urdu, Personalization) — Phase 1 or 2?

**Decision Made:**

**Phase 1 (MVP, Q4 2025):**
- ✅ 6 chapters in English
- ✅ Textbook on GitHub Pages
- ✅ RAG chatbot with basic Q&A
- ✅ Dark/light mode toggle
- ✅ Full-text search

**Phase 2 (Q1 2026):**
- 🔄 Urdu translation (optional)
- 🔄 Learner personalization
- 🔄 Conversation memory (optional)
- 🔄 Advanced analytics

**Rationale:** Phase 1 delivers minimum viable product; Phase 2 adds polish and accessibility

---

### Decision 5: Community Feedback Loop
**Context:** How to gather feedback on textbook quality + RAG accuracy?

**Decision Made:**
- **In-Page Comments:** Giscus integration (GitHub Discussions)
- **Chatbot Feedback:** Thumbs up/down on chatbot responses
- **Monthly Surveys:** Google Forms for learner satisfaction
- **GitHub Issues:** Public issue tracker for bugs/improvements
- **Community Discord:** Optional Discord server for Q&A
- **Rationale:** Multiple channels capture different user preferences; GitHub-native for transparency

---

## IV. Unresolved Tensions & Trade-offs

### Tension 1: Minimalism vs. Completeness
**Conflict:** 1,000–1,500 word chapters may oversimplify ROS 2 or humanoid kinematics

**Trade-off Options:**
- A: Keep chapters short, provide extensive external links (chosen for MVP)
- B: Expand to 2,000–3,000 words per chapter (compromises on minimalism)
- C: Separate "Essential" vs. "Deep Dive" textbooks

**Current Decision:** Option A (Phase 1); revisit if feedback indicates insufficient depth

---

### Tension 2: Free-Tier Only vs. Production Quality
**Conflict:** Strict "free-tier only" constraint limits LLM options

**Trade-off Options:**
- A: Use local LLM (Mistral 7B, fully free, but lower quality)
- B: Use OpenAI API (better quality, ~$20/month cost)
- C: Hybrid approach (local for internal demo, OpenAI for production)

**Current Decision:** Option B (OpenAI API acceptable for MVP); local LLM as fallback

---

### Tension 3: Semantic Search Limits
**Conflict:** Semantic search may miss keyword-specific queries (e.g., acronyms like "URDF", "SDF")

**Trade-off Options:**
- A: Hybrid search (semantic + keyword ranking) — adds complexity
- B: Pure semantic search with acronym expansion in preprocessing
- C: Accept limitation, provide search tips to users

**Current Decision:** Option C (Phase 1); upgrade to Option A in Phase 2 if needed

---

### Tension 4: Personalization Privacy
**Conflict:** Personalized profiles require data storage; conflicts with privacy goals

**Trade-off Options:**
- A: Client-side only (localStorage, no server, no tracking)
- B: Optional server storage (user consent, GDPR compliant)
- C: No personalization (privacy-first, but less engaging)

**Current Decision:** Option A (localStorage default); Option B available for power users

---

## V. Questions Requiring User Input

### Q1: Which LLM Provider Should We Use?
**Options:**
- [ ] OpenAI GPT-4o-mini ($0.15/1M tokens, good quality)
- [ ] Claude 3.5 Haiku (lower cost, alternative)
- [ ] Local Mistral 7B (fully free, lower quality, self-hosted)
- [ ] Hybrid (multiple providers with fallback)

**Recommendation:** OpenAI for MVP; local Mistral as long-term fallback

---

### Q2: Should Urdu Translation Be Phase 1 or Phase 2?
**Options:**
- [ ] Phase 1 MVP (delay other features)
- [ ] Phase 2 (post-launch)
- [ ] Defer (out of scope for 2025)

**Recommendation:** Phase 2 (enables MVP launch sooner)

---

### Q3: What's the Acceptable Monthly Cost?
**Options:**
- [ ] Strictly $0 (local LLM only, no API costs)
- [ ] < $20/month (OpenAI for MVP)
- [ ] < $50/month (includes optional services)

**Recommendation:** < $20/month (OpenAI acceptable)

---

### Q4: How Many Reviewers for Technical Accuracy Check?
**Options:**
- [ ] 1 expert (fast, single perspective)
- [ ] 3 experts (peer review, consensus)
- [ ] Community review (slow, but comprehensive)

**Recommendation:** 1 expert pre-launch; community feedback post-launch

---

## VI. Implementation Timeline & Milestones

### Milestone 1: Setup & Infrastructure (Week 1)
- [ ] Create GitHub repository
- [ ] Set up Docusaurus project
- [ ] Configure GitHub Actions workflow
- [ ] Provision Qdrant + Neon accounts

### Milestone 2: Chapter Content (Weeks 2–4)
- [ ] Write all 6 chapters (1,000–1,500 words each)
- [ ] Create diagrams (2–4 per chapter)
- [ ] Technical accuracy review
- [ ] Add code examples (≤ 20 lines each)

### Milestone 3: Docusaurus Build (Week 5)
- [ ] Import chapters into Docusaurus
- [ ] Configure sidebar navigation
- [ ] Enable search
- [ ] Test responsive design
- [ ] Accessibility audit (WCAG 2.1 AA)

### Milestone 4: RAG Backend (Week 6)
- [ ] Ingestion pipeline (markdown → chunks → embeddings)
- [ ] Qdrant index creation
- [ ] FastAPI server setup
- [ ] LLM integration (OpenAI)

### Milestone 5: Integration & Testing (Week 7)
- [ ] Connect Docusaurus widget to RAG backend
- [ ] End-to-end testing (query → response → citation)
- [ ] Performance tuning (< 1s queries, < 2s page loads)
- [ ] Security hardening (API rate limiting, input validation)

### Milestone 6: Launch & Monitoring (Week 8)
- [ ] Deploy to GitHub Pages
- [ ] Deploy FastAPI backend (Vercel/Railway)
- [ ] Enable monitoring + logging
- [ ] Public beta announcement
- [ ] Gather initial feedback

---

## VII. Amendment Log

| Date | Section | Change | Rationale |
|------|---------|--------|-----------|
| 2025-12-05 | All | Document created | Project clarification phase |
| TBD | Section I.1 | LLM provider decision pending | Awaiting user input on cost tolerance |
| TBD | Section I.7 | Urdu translation timing pending | Awaiting prioritization decision |

---

**Document Status:** ✅ Active and Guiding Implementation  
**Last Updated:** 2025-12-05  
**Next Review:** 2025-12-15 (after user input on open questions)

**Maintained By:** Physical AI Textbook Team  
**Owner:** [Project Lead Name]

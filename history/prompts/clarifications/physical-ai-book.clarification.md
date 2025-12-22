# Physical AI Book - Clarification Document

**Project:** Physical AI - Learn by Building  
**Date Created:** December 5, 2025  
**Status:** Active Clarification Phase  

---

## I. Key Questions & Answers

### 1. Target Hardware Platform
**Question:** Which hardware platforms should be prioritized for the first release?

**Current Assumption:**
- **Primary:** Raspberry Pi 4/5 (most accessible for beginners)
- **Secondary:** Arduino (microcontroller alternative)
- **Tertiary:** Simulation environments (PyBullet, Gazebo) as equal-priority alternatives

**Decision Needed:** Should we support specific sensor kits (e.g., official Raspberry Pi kits) or remain agnostic?

---

### 2. Python Version & Dependencies
**Question:** What is the minimum/maximum Python version range?

**Current Assumption:**
- **Minimum:** Python 3.9
- **Maximum:** Python 3.12+
- **Lock Strategy:** Pin all dependencies to specific versions in requirements.txt

**Decision Needed:** Do we support Python 3.8 for older devices? Should we provide Docker containers for consistent environments?

---

### 3. Course Pacing & Duration
**Question:** What is the target completion time for learners?

**Current Assumption:**
- **Beginner Path:** 8-10 weeks (20-30 hours total)
- **Intermediate Path:** 12-14 weeks (40-50 hours total)
- **Per Lesson:** 20-60 minutes (hands-on + reading)

**Decision Needed:** Should lessons be self-paced or synchronized? Do we provide weekly release schedules?

---

### 4. Assessment & Gamification
**Question:** Should the course include quizzes, badges, or progress tracking?

**Current Assumption:**
- **Phase 1:** No formal assessments (project-based learning only)
- **Phase 2:** Optional self-checks and quizzes (not graded)
- **Phase 3:** Community project showcase and peer review

**Decision Needed:** Do we want learner accounts? Analytics/dashboards? Progress syncing across devices?

---

### 5. Community & Support Model
**Question:** What support channels should be available?

**Current Assumption:**
- **Primary:** GitHub Discussions (asynchronous)
- **Secondary:** Discord community server (real-time chat)
- **Tertiary:** Monthly office hours (live Q&A, asynchronous video archive)
- **Support Level:** Best-effort community moderation; no SLA

**Decision Needed:** Should we hire dedicated moderators? Provide commercial support tier? Bot for FAQs?

---

### 6. Hardware Accessibility & Alternatives
**Question:** How do we handle learners without hardware access?

**Current Assumption:**
- **Mandatory Alternatives:** PyBullet, Gazebo simulations for every hardware exercise
- **Cost Awareness:** Sensor kits < $50 USD for full chapter
- **Documentation:** Clear setup guides with photos and video walkthroughs

**Decision Needed:** Should we provide simulator pre-built binaries? Cloud-based simulation access?

---

### 7. Multilingual Support
**Question:** Should documentation support languages other than English?

**Current Assumption:**
- **Phase 1:** English only
- **Phase 2:** Community translation contributions (volunteer-based)
- **Phase 3:** Official translations (priority: Spanish, Mandarin, Hindi)

**Decision Needed:** What translation management tool? Which languages first?

---

### 8. Future Chapter Roadmap
**Question:** What comes after Chapter 1: Foundations?

**Current Assumption:**
- **Chapter 2:** Hello Physical AI (20-30 hours) - First full system build
- **Chapter 3:** Computer Vision (20-30 hours) - Image processing & object detection
- **Chapter 4:** Motion & Control (20-30 hours) - Motors, servos, movement planning
- **Chapter 5:** Sensor Fusion (20-30 hours) - Multi-sensor integration
- **Capstone:** Autonomous system project (40-50 hours)

**Decision Needed:** Should chapters be released sequentially or in parallel? Beta release strategy?

---

### 9. Code Repository Management
**Question:** How should code examples be organized externally?

**Current Assumption:**
- **Main Repo:** `physical-ai/book` (documentation, configs)
- **Code Repo:** `physical-ai/course-examples` (runnable code, organized by chapter/lesson)
- **Hardware Files:** Fritzing, CAD models, datasheets in `physical-ai/hardware`
- **Community Projects:** Separate `physical-ai/community-showcase` repo with contributions

**Decision Needed:** Monorepo vs. distributed repos? How to version code alongside docs?

---

### 10. License & Attribution
**Question:** What license should the project use?

**Current Assumption:**
- **Documentation:** CC-BY-4.0 (Creative Commons Attribution)
- **Code:** MIT License
- **Hardware Files:** CC-BY-SA-4.0 (ShareAlike for derivative designs)
- **Attribution:** Mandatory credits for contributors and third-party resources

**Decision Needed:** Should commercial use be permitted? Trademark guidelines for "Physical AI"?

---

## II. Assumptions Documentation

### Technical Assumptions
1. Learners have Python 3.9+ installed or access to cloud IDE (Replit, Colab)
2. Learners can install pip packages or use virtual environments
3. Hardware learners have internet for downloading models/libraries (~500MB per chapter)
4. Simulation learners have graphics-capable devices (GPU recommended but not required)

### Pedagogical Assumptions
1. Learners retain better through hands-on practice than reading
2. Beginner learners need motivating examples early (within Lesson 1.3)
3. Error messages should be explicitly taught (debugging is a skill)
4. Community projects are valuable for retention and portfolio building

### Organizational Assumptions
1. Maintainers are volunteers with 10-20 hours/week capacity
2. Community contributors will provide translations and improvements
3. Project will sustain without commercial funding (open-source model)
4. GitHub and Discord scale appropriately for community needs

### Hardware Assumptions
1. Raspberry Pi 4 is affordable enough for target audience (~$75)
2. USB connectivity and standard GPIO is sufficient for introductory projects
3. No bleeding-edge hardware required; 2-3 year old components acceptable
4. Simulation environments are viable alternatives for 80%+ of exercises

---

## III. Key Decisions Made

### Decision 1: Docusaurus Over Alternatives
**Context:** Why Docusaurus instead of Jupyter Book, Sphinx, or custom build?

**Rationale:**
- Strong markdown + MDX support for interactive components
- Built-in versioning for course evolution
- Fast builds and good performance (Lighthouse scores 90+)
- Familiar to developers (lowers contributor barrier)
- Easy theming and customization
- Strong plugin ecosystem

**Trade-off:** Limited interactive notebook execution (can embed or link to Colab)

---

### Decision 2: Three Lessons Per Chapter Initially
**Context:** Why not more comprehensive first chapter?

**Rationale:**
- Manageable scope for maintenance (10 weeks vs. 20 weeks)
- Quick to publish, gather community feedback
- Allows for iterative improvement based on real learner data
- Proof-of-concept for chapter structure and pedagogy

**Implication:** Chapters 2+ will follow similar 3-lesson structure for consistency

---

### Decision 3: Hardware + Simulation Parity
**Context:** Why make simulations first-class, not fallback?

**Rationale:**
- Removes cost barrier for entry (critical for developing regions)
- Enables learning anywhere (no hardware setup constraints)
- Safer for exploring dangerous operations (e.g., high-speed motors)
- Simulation debugging is faster iteration
- Hardware learners benefit from simulation validation

**Trade-off:** Requires maintaining two parallel exercise implementations

---

### Decision 4: Community-Driven Evolution (No Paywall)
**Context:** Why open-source instead of commercial?

**Rationale:**
- Aligns with democratization mission
- Maximizes contributor participation
- Sustainability through community engagement, not sales
- Easier adoption by institutions and bootcamps
- Avoids vendor lock-in (learners own their data)

**Sustainability Plan:**
- Donations/sponsorships for infrastructure
- Consulting services for enterprises
- Professional services (workshops, training)

---

### Decision 5: Beginner-to-Intermediate Scope
**Context:** Why not include advanced AI topics (RL, transformers)?

**Rationale:**
- Mental model must be built sequentially (foundational concepts first)
- Beginner frustration leads to churn if topic jumps from supervised → advanced RL
- Can iterate on foundations with real learner feedback before advanced topics
- Capstone projects bridge to self-directed learning

**Expansion Plan:** Chapter 6+ (post-launch) will cover advanced topics

---

## IV. Unresolved Tensions

### Tension 1: Breadth vs. Depth
**Conflict:** Should each lesson cover many sensors/actuators (breadth) or master few deeply (depth)?

**Current Position:** Lean depth for Chapter 1 (master temperature sensing → classification)

**Trade-off:** Breadth (many hardware examples) vs. Depth (understand one system fully)

**Recommendation:** Gather learner feedback to determine preference

---

### Tension 2: Theory vs. Hands-On
**Conflict:** How much math/theory before first hands-on exercise?

**Current Position:** Lesson 1.2 (fundamentals) before Lesson 1.3 (hardware), minimal math

**Trade-off:** Some learners want theory foundations; others want to "just build"

**Recommendation:** Provide optional deep-dive chapters; maintain main path as practical

---

### Tension 3: Professional vs. Beginner Code
**Conflict:** Should code examples be production-quality or pedagogically simple?

**Current Position:** Pedagogically clear; comments over clever code

**Trade-off:** May not reflect real-world practices learners encounter later

**Recommendation:** Include professional refactoring examples in stretch goals

---

### Tension 4: Simulation Fidelity
**Conflict:** Should simulations be highly realistic or simplified for learning?

**Current Position:** Start simple (PyBullet for motion); evolve to realistic (Gazebo, ROS)

**Trade-off:** Simple simulations may not prepare learners for real hardware failures

**Recommendation:** Explicitly document simulation limitations; transition to real hardware early

---

## V. Future Decision Points

### Q3 2025: Chapter 2 Planning
- [ ] Decide on capstone project scope (3-week project? full chapter?)
- [ ] Gather community input on desired topics (RL vs. optimization vs. real-time?)
- [ ] Plan hardware upgrades (add motor controller? multi-sensor system?)

### Q4 2025: Community Infrastructure
- [ ] Evaluate Discord usage and support load
- [ ] Determine if paid moderators needed
- [ ] Plan security and code-of-conduct enforcement

### Q1 2026: Commercialization Exploration
- [ ] Survey interest in professional services (training, consulting)
- [ ] Evaluate grant funding opportunities (education, AI democratization)
- [ ] Plan sustainability model for maintainer compensation

### Q2 2026: Multilingual Support
- [ ] Identify translation priority languages
- [ ] Set up translation management system (Crowdin? Transifex?)
- [ ] Recruit volunteer translators

---

## VI. Communication & Feedback Channels

### How to Contribute Clarifications
1. **GitHub Issues:** Project-level questions and clarifications
2. **Discord:** Real-time discussions and community input
3. **Quarterly Reviews:** Structured community surveys
4. **Community Council:** Monthly meeting with active contributors

### How to Track Changes
- All decisions documented in this file (updated monthly)
- Amendment history at bottom (see Section VII)
- GitHub Projects board for active decision items

---

## VII. Amendment History

| Date | Section | Change | Rationale |
|------|---------|--------|-----------|
| 2025-12-05 | Initial | Document created | Project launch |
| TBD | TBD | TBD | TBD |

---

**Document Status:** ✅ Active and Evolving  
**Last Updated:** December 5, 2025  
**Next Review:** January 15, 2026

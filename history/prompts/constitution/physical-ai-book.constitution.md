# Physical AI & Humanoid Robotics Essentials — Constitution

## Project Goal

Develop a short, modern, AI-native textbook titled "Physical AI & Humanoid Robotics — Essentials", designed for fast learning and optimized for free-tier hosting. The textbook must integrate seamlessly with a lightweight RAG chatbot that answers strictly from the book's content.

---

## 🎯 Purpose

Create a simple, accurate, minimalist, and professional learning resource that introduces students to the foundations of Physical AI and humanoid robotics, supported by a Docusaurus-based UI and a free-tier-friendly RAG system.

---

## Core Principles

### I. Simplicity (NON-NEGOTIABLE)
All content must be minimal, distraction-free, and essential. No unnecessary complexity, jargon, or tangential topics. Every sentence serves a clear pedagogical purpose.

**Requirements:**
- Each chapter ≤ 1,500 words
- Maximum 3 key concepts per section
- Plain language; minimize acronyms (explain on first use)
- No fluff, examples, or "nice-to-know" content
- Code snippets ≤ 20 lines per example

### II. Accuracy First
Content must be technically verified and deterministic. No approximations, no ambiguous statements, no AI hallucinations. Every concept must be grounded in established knowledge or cited sources.

**Requirements:**
- All claims must be verifiable or cited
- Technical accuracy reviewed by domain expert pre-publication
- No speculative or theoretical-only content
- Clear distinction between core concepts vs. advanced topics
- Testable code examples (reproducible on free-tier environments)

### III. Minimalism in Architecture
System architecture must be lightweight, deterministic, and free-tier friendly. No GPU inference, no large embedding models, no expensive infrastructure. Build fast, deploy fast, query fast.

**Requirements:**
- Docusaurus static build < 30 seconds
- GitHub Pages as primary hosting (zero cost)
- RAG: Qdrant free tier + Neon PostgreSQL free tier
- Embeddings: Lightweight sentence-level vectors only
- API response time < 1 second (RAG queries)
- Total dependencies < 50 (both book + chatbot combined)

### IV. Deterministic RAG (NON-NEGOTIABLE)
Chatbot must answer ONLY from the book's text. No external knowledge, no web searches, no LLM hallucinations. Every response includes citation with chapter/section reference.

**Requirements:**
- Chatbot constrained to book-only retrieval
- All responses include exact text citation and source reference
- "Out of scope" responses explicitly state: "This topic is not covered in the textbook"
- Retrieval augmented generation must be deterministic (no stochastic sampling beyond embeddings)
- Test suite: 100% response accuracy on book content queries

### V. Docusaurus-First UI
Textbook hosted on Docusaurus with clean, minimal theme optimized for readability. No custom builds, no heavy JavaScript. Static generation for fast GitHub Pages deployment.

**Requirements:**
- Single-column layout (mobile-first responsive)
- Sidebar navigation matching chapter structure
- Full-text search enabled
- Dark/light mode support
- Accessibility: WCAG 2.1 AA minimum
- All diagrams accessible (alt text, SVG preferred)

### VI. Content Structure Alignment
Book structure strictly follows 6 chapters, each self-contained. No interdependencies except linear progression. Each chapter must work standalone for RAG retrieval.

**Requirements:**
- Chapter 1: Introduction to Physical AI
- Chapter 2: Basics of Humanoid Robotics
- Chapter 3: ROS 2 Fundamentals
- Chapter 4: Digital Twin Simulation (Gazebo + Isaac)
- Chapter 5: Vision-Language-Action Systems
- Chapter 6: Capstone - Simple AI-Robot Pipeline
- Each chapter: 1,000-1,500 words, 3-5 sections, 2-4 diagrams

### 3.3 Audience Accessibility Considerations
- **Language:** Clear, plain English with technical terms defined at first use
- **Pace:** Assume ~2-3 hours per module for beginners
- **Tools:** Provide both hardware and simulation-based learning paths
- **Support:** Curated Q&A section and troubleshooting for each major topic

---

## 4. Content Organization & Structure

### 4.1 Top-Level Modules (Docusaurus Docs Sidebar)

```
docs/
├── 00-getting-started/
│   ├── what-is-physical-ai.md
│   ├── learning-path-beginner.md
│   ├── learning-path-intermediate.md
│   └── environment-setup.md
├── 01-foundations/
│   ├── ai-fundamentals.md
│   ├── neural-networks-basics.md
│   ├── sensors-and-actuators.md
│   └── embedded-systems-intro.md
├── 02-setup-and-tools/
│   ├── python-setup.md
│   ├── hardware-requirements.md
│   ├── simulation-environments.md
│   └── development-workflow.md
├── 03-hello-physical-ai/
│   ├── first-sensor-reading.md
│   ├── first-neural-network.md
│   ├── integrating-sensor-to-model.md
│   └── project-simple-classifier.md
├── 04-computer-vision/
│   ├── image-basics.md
│   ├── opencv-essentials.md
│   ├── object-detection.md
│   └── project-object-tracker.md
├── 05-motion-and-control/
│   ├── motor-basics.md
│   ├── servo-control.md
│   ├── movement-planning.md
│   └── project-mobile-robot.md
├── 06-sensor-fusion/
│   ├── multi-sensor-integration.md
│   ├── data-synchronization.md
│   ├── filtering-techniques.md
│   └── project-autonomous-navigation.md
├── 07-advanced-topics/
│   ├── reinforcement-learning-intro.md
│   ├── real-time-inference.md
│   ├── energy-optimization.md
│   └── project-adaptive-system.md
├── 08-troubleshooting/
│   ├── hardware-issues.md
│   ├── model-performance.md
│   ├── integration-problems.md
│   └── faq.md
└── 09-resources/
    ├── hardware-guide.md
    ├── library-references.md
    ├── community-projects.md
    └── further-learning.md
```

### 4.2 Blog Section (Project Showcases & Case Studies)
- Real-world physical AI implementations
- Community project spotlights
- Monthly learner showcases
- Industry interviews with practitioners

### 4.3 Interactive Examples & Experiments
Each major concept includes:
- **Runnable Code Blocks:** Copy-paste friendly, tested snippets
- **Virtual Labs:** Browser-based simulators (when hardware unavailable)
- **Hardware Guides:** Step-by-step assembly instructions with photos
- **Expected Output:** Screenshots/videos showing correct behavior

---

## 5. Technical Architecture

### 5.1 Docusaurus Configuration

#### Site Metadata
```
title: Physical AI - Learn by Building
tagline: Master AI through hands-on robotics and embedded projects
url: https://physical-ai-book.example.com
baseUrl: /
```

#### Key Plugins & Features to Enable
- **Search:** Full-text search across all modules
- **Versioning:** Support multiple course versions (v1.0, v2.0, etc.)
- **Comments:** Giscus or Utterances for learner feedback on each page
- **Analytics:** Track learner progress through modules
- **Dark Mode:** Support for accessibility

#### Sidebar Structure
```typescript
// sidebars.ts organization
sidebars = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/what-is-physical-ai',
        'getting-started/learning-path-beginner',
        // ...
      ]
    },
    // ... additional categories
  ]
}
```

### 5.2 Content Rendering Standards

#### Markdown Enhancements
- **Code Blocks:** Language-specific syntax highlighting (python, cpp, javascript)
- **Callout Boxes:** Info, Warning, Tip, Danger using admonitions
- **Diagrams:** Mermaid diagrams for architecture, workflows, decision trees
- **Tabs:** Hardware vs. Simulation alternatives shown in tabs
- **Math:** KaTeX for mathematical equations and formulas

#### Component Usage
- **Interactive Code Playgrounds:** Embed CodePen/JSFiddle for web-based simulations
- **Video Embeds:** YouTube videos for visual walkthroughs
- **Image Galleries:** Before/after, step-by-step photo sequences
- **Collapsible Sections:** Expand advanced topics or optional deep-dives

### 5.3 Code Repository Integration

#### External Code Hosting
- **GitHub Repository:** `physical-ai/course-examples`
- **Notebook Repository:** Jupyter notebooks for complex projects
- **Hardware Configs:** Fritzing files, CAD models, sensor datasheets

#### In-Document Code Linking
```markdown
<!-- Link to specific function in external repo -->
<!-- Link to file with line ranges: lines 10-50 -->
<!-- Import code snippets directly into docs -->
```

---

## 6. Content Standards & Quality Assurance

### 6.1 Writing Style Guide

#### Tone & Voice
- **Conversational yet professional:** "Let's build a robot" not "One must construct a robotic apparatus"
- **Encouraging:** Acknowledge challenges; celebrate milestones
- **Precise:** Avoid ambiguous language; define specialized terms
- **Practical:** Lead with "why" before "how" for motivation

#### Structure Per Module
1. **Learning Objectives:** What you'll accomplish (3-5 bullet points)
2. **Prerequisites:** Required knowledge/skills
3. **Introduction:** Relatable problem/motivation
4. **Core Content:** Explanations + diagrams
5. **Code Example:** Runnable, annotated code snippet
6. **Hands-On Exercise:** Guided practical activity
7. **Common Mistakes:** Pitfalls and solutions
8. **Summary:** Key takeaways
9. **Next Steps:** What to learn next

### 6.2 Code Quality Standards

#### Every Code Example Must
- ✅ Be tested and verified to run
- ✅ Include inline comments explaining logic
- ✅ Have clear variable/function names
- ✅ Specify Python version, library versions
- ✅ Include expected output or error messages
- ✅ Link to full example in GitHub repository

#### Python Code Standards
```python
# Example structure
"""
Module docstring explaining purpose.

Required Libraries: numpy==1.23.0, opencv-python==4.6.0
Python Version: 3.9+
"""

import numpy as np
from typing import Tuple

def classify_sensor_data(data: np.ndarray) -> str:
    """
    Classify sensor readings into categories.
    
    Args:
        data: 1D array of sensor values
        
    Returns:
        Classification label: 'hot', 'warm', 'cold'
    """
    # Implementation with comments
    pass
```

### 6.3 Hands-On Exercise Standards

#### Every Module Must Include
- **Duration:** Estimated time to complete (e.g., 20-30 minutes)
- **Difficulty:** Beginner / Intermediate
- **Requirements:** Hardware, software, files needed
- **Step-by-Step Guide:** Numbered, screenshot-rich instructions
- **Verification Checklist:** How to confirm success
- **Troubleshooting:** Common issues and fixes
- **Stretch Goal:** Optional extension for faster learners

#### Exercise Format Example
```markdown
## Exercise: Reading Temperature Sensors

**Duration:** 15 minutes | **Difficulty:** Beginner

### Requirements
- [ ] Raspberry Pi 4 or simulation environment
- [ ] DS18B20 temperature sensor (or simulated)
- [ ] Python 3.9+

### Steps
1. Wire the sensor to GPIO pin 4
   - [See diagram: temperature-sensor-wiring.png]
2. Install the library: `pip install w1thermsensor`
3. Run the example script: `python read_temp.py`

### Verification
- [ ] Script runs without errors
- [ ] Temperature readings display every 2 seconds
- [ ] Values match room temperature (±2°C)

### Troubleshooting
**Problem:** "Module not found" error
**Solution:** Run `pip install w1thermsensor --upgrade`
```

## Content Organization & Standards

### Module Structure (Required Template)
```
# [Chapter Title]

**Chapter [#]**: [Subtitle]  
**Word Count:** [1,000-1,500]  
**Sections:** [3-5]  
**Diagrams:** [2-4]  

## Overview
[1-2 sentence purpose and learning outcome]

## Section 1: [Core Concept]
[300-400 words]
- Definition
- Key components
- Relevance to Physical AI

## Section 2: [Building Block]
[300-400 words]
- Foundational knowledge
- Practical implications
- Example application

## Code Example (Optional)
[≤ 20 lines, runnable on free-tier]

## Key Takeaways
- Bullet point 1
- Bullet point 2
- Bullet point 3

## Next Steps
[Link to next chapter or related topic]

## References & Citations
[Sources for all claims]
```

### Code Example Standards

**All code must:**
- Run on Python 3.10+ (no GPU required)
- Be ≤ 20 lines (preferably ≤ 15)
- Include type hints (Python 3.10+ style)
- Have docstring explaining purpose
- Show expected output inline
- Link to full code on GitHub if extended
- Use only free-tier compatible libraries (no CUDA, no heavy models)

**Example Template:**
```python
"""
Simple ROS 2 node example.

Dependencies: rclpy (free tier)
"""

import rclpy
from std_msgs.msg import String

class MinimalSubscriber:
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node('minimal_listener')
        self.subscription = self.node.create_subscription(
            String, 'topic', self.listener_callback, 10)
    
    def listener_callback(self, msg):
        print(f'Received: {msg.data}')

# Output: "Received: [message content]"
```

### Diagram Requirements

**All diagrams must:**
- Be SVG or high-quality PNG (< 200KB)
- Include descriptive captions
- Have alt text (accessibility)
- Illustrate 1 concept per diagram
- Use consistent color palette (colorblind-friendly)
- Include labels and legends

**Diagram Types:**
- **Architecture Diagrams:** System components and data flow (Mermaid)
- **Flowcharts:** Process steps and decision trees (Mermaid)
- **Structural Diagrams:** Physical layouts, robot anatomy (SVG/PNG)
- **Data Flow:** Sensor → Processing → Action pipelines (Mermaid)

---

## Docusaurus Configuration

### File Structure
```
physical-ai-textbook/
├── docusaurus.config.ts
├── sidebars.ts
├── package.json
├── docs/
│   ├── intro.md
│   ├── ch1-physical-ai/
│   │   ├── overview.md
│   │   └── _category_.json
│   ├── ch2-humanoid-robotics/
│   ├── ch3-ros2/
│   ├── ch4-digital-twin/
│   ├── ch5-vision-language-action/
│   ├── ch6-capstone/
│   └── resources/
│       ├── glossary.md
│       └── references.md
├── src/
│   ├── components/
│   │   ├── CitationBlock.tsx
│   │   └── CodeBlock.tsx
│   ├── css/custom.css
│   └── pages/
├── static/
│   ├── diagrams/
│   └── code-examples/
└── .github/workflows/deploy.yml
```

### Build Configuration (docusaurus.config.ts)
```typescript
const config: Config = {
  title: 'Physical AI & Humanoid Robotics — Essentials',
  tagline: 'Short, accurate, AI-native textbook for fast learning',
  favicon: 'img/favicon.ico',
  url: 'https://physical-ai-textbook.github.io',
  baseUrl: '/book/',
  
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/[org]/book/tree/main',
        },
        theme: { customCss: './src/css/custom.css' },
      },
    ],
  ],
  
  plugins: ['docusaurus-plugin-search-local'],
  
  themeConfig: {
    colorMode: { defaultMode: 'light', respectPrefersColorScheme: true },
    navbar: {
      title: 'Physical AI Essentials',
      items: [
        { to: '/docs/intro', label: 'Textbook' },
        { href: 'https://github.com/[org]/book', label: 'GitHub' },
      ],
    },
  },
};
```

---

## RAG Chatbot Specifications

### Tech Stack
- **Embeddings:** Sentence-Transformers (free tier, no GPU)
- **Vector DB:** Qdrant (free tier, local or cloud)
- **SQL DB:** Neon PostgreSQL (free tier, 3GB storage)
- **Backend:** FastAPI (lightweight Python framework)
- **Frontend:** Docusaurus built-in chat widget

### Retrieval Pipeline
1. **Ingestion:** Parse chapters into sentence-level chunks (50-100 tokens each)
2. **Embedding:** Generate embeddings using sentence-transformers/all-MiniLM-L6-v2
3. **Storage:** Store embeddings + raw text in Qdrant + PostgreSQL
4. **Query:** User question → embedding → semantic search → retrieve top-3 passages
5. **Response:** LLM generates answer from retrieved passages with citations

### Constraints
- Maximum 3 passages per response
- All responses must cite chapter and section
- If no relevant passage found: "This topic is not covered in the textbook"
- Response time target: < 1 second
- No external knowledge retrieval; deterministic only

### Citation Format
```
**Answer:** [Generated response]

**Source:** Chapter [#], Section "[Section Name]"
**Text:** "[Exact quote from textbook]"
```

---

## Quality Assurance

### Pre-Publication Checklist
- [ ] All claims technically accurate
- [ ] Code examples tested on free-tier setup
- [ ] Word count per chapter: 1,000-1,500
- [ ] Sections: 3-5 per chapter
- [ ] Diagrams: 2-4 per chapter with captions + alt text
- [ ] Accessibility: WCAG 2.1 AA compliance
- [ ] Docusaurus build: < 30 seconds
- [ ] All links valid (internal + external)
- [ ] RAG test suite: 100% accuracy on sample queries

### Testing Requirements
- **Build Test:** `npm run build` succeeds without warnings
- **Accessibility Test:** axe-core automated scan passes
- **RAG Test:** 20 representative queries return correct citations
- **Performance Test:** GitHub Pages loads < 2 seconds
- **Mobile Test:** Responsive design on 320px+ width

---

## Success Criteria

✅ **Textbook Completion**
- All 6 chapters published and accessible
- Clean, minimal Docusaurus UI
- Zero broken links, diagrams, code examples

✅ **RAG Chatbot Deployment**
- Deterministic retrieval from book content
- Citation-based responses (100% accuracy)
- Query latency < 1 second
- Running on free-tier infrastructure

✅ **Infrastructure**
- GitHub Pages deployment automated via GitHub Actions
- Build time < 30 seconds
- No external GPU/heavy compute dependencies
- Total monthly cost: $0 (free tier only)

✅ **Content Quality**
- All code examples tested and runnable
- All diagrams accessible (alt text, SVG)
- Reading difficulty: University beginner level
- Zero hallucinations, all claims verified

---

## Non-Negotiable Constraints

1. **Free Tier Only:** Zero paid services; all infrastructure must be free tier
2. **No GPU:** Zero GPU inference required anywhere in system
3. **Deterministic:** Chatbot answers ONLY from textbook; no external web search
4. **Static Build:** Textbook is fully static HTML (GitHub Pages compatible)
5. **Speed:** Build time < 30s, page load < 2s, query response < 1s
6. **Accuracy:** No hallucinations; all responses cited
7. **Minimalism:** ≤ 50 dependencies across entire project

---

## Versioning & Maintenance

**Format:** MAJOR.MINOR.PATCH

- **MAJOR:** Breaking changes (chapter structure reorganization)
- **MINOR:** New content, updated chapters, accuracy fixes
- **PATCH:** Typo corrections, diagram updates, link fixes

**Release Cadence:**
- v1.0: Initial 6-chapter release
- v1.x: Content refinement based on community feedback
- v2.0: Proposed after 6+ months community usage

---

## Governance

### Constitution Authority
This constitution supersedes all development decisions. All deviations require explicit amendment with documented rationale.

### Amendment Process
1. **Proposal:** Document rationale and impact
2. **Review:** Core team discussion (GitHub issue)
3. **Approval:** Unanimous agreement required
4. **Documentation:** Amendment recorded in this file
5. **Communication:** Notify all stakeholders

### Compliance Enforcement
- All PRs must comply with these principles
- Build pipeline rejects violations automatically
- Weekly audit of textbook content quality

---

**Version:** 1.0 | **Ratified:** 2025-12-05 | **Last Amended:** 2025-12-05

**Status:** ✅ Active and Guiding Development  
**Maintained By:** Physical AI Textbook Core Team

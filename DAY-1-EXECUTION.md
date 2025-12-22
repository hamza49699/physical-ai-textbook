# 🚀 DAY 1 EXECUTION GUIDE - December 5, 2025

**Your GitHub Username:** `hamza699`  
**Repository URL:** https://github.com/hamza699/physical-ai-textbook  
**Time Estimate:** 3 hours  
**Status:** READY TO BEGIN  

---

## ✅ Task 1.1.1: Create GitHub Repository (30 min)

### Step 1: Create Repo on GitHub

1. Open https://github.com/new
2. Fill in:
   - **Repository name:** `physical-ai-textbook`
   - **Description:** `AI-native textbook with RAG chatbot for Physical AI and Humanoid Robotics`
   - **Visibility:** Public ✓
   - **Add a README file:** ✓ Check
   - **Add .gitignore:** Python
   - **Choose a license:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

3. Click **Create repository**

**Result:** Repository created at https://github.com/hamza699/physical-ai-textbook

---

### Step 2: Configure Repository Settings

1. Go to **Settings** → **General**
2. Set default branch to `main`

3. Go to **Settings** → **Branch protection rules** → **Add rule**
   - Branch name pattern: `main`
   - ✓ Require pull request reviews before merging: 1
   - ✓ Require status checks to pass
   - ✓ Do not allow bypassing

4. Go to **Settings** → **Pages**
   - Source: Deploy from a branch
   - Branch: `gh-pages` / `root`
   - ✓ Enforce HTTPS

---

### Step 3: Clone Locally and Set Up Structure

Run these commands in your terminal:

```bash
cd c:\Users\digital\claude_first
git clone https://github.com/hamza699/physical-ai-textbook.git
cd physical-ai-textbook

# Create folder structure
mkdir .github\workflows backend\tests docs\chapters src\components static\diagrams
```

---

### Step 4: Add .gitignore

Create `.gitignore` file with this content:

```
# Dependencies
node_modules/
.pnp
.pnp.js
package-lock.json
yarn.lock

# Production
build/
dist/
.next/
out/

# Backend
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
.venv

# Environment variables
.env
.env.local
.env.*.local
.env.production.local

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
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

Then commit:

```bash
git add .gitignore
git commit -m "chore: add gitignore"
git push origin main
```

---

### ✅ Task 1.1.1 Verification Checklist

- [ ] Repository visible at https://github.com/hamza699/physical-ai-textbook
- [ ] Repository is Public
- [ ] README.md exists
- [ ] CC-BY-4.0 license added
- [ ] Branch protection rules configured
- [ ] GitHub Pages enabled with HTTPS
- [ ] Local clone created at `c:\Users\digital\claude_first\physical-ai-textbook`
- [ ] `.gitignore` committed
- [ ] Default branch is `main`

**⏱️ Time: 30 minutes**  
**✅ Status: Ready for next task**

---

## ✅ Task 1.1.2: Initialize Docusaurus (1 hour)

### Step 1: Copy Existing my-website Folder

You already have Docusaurus set up in `my-website`. Now copy it to the repo:

```bash
# Copy entire my-website to physical-ai-textbook
cd c:\Users\digital\claude_first
xcopy my-website\* physical-ai-textbook /E /I /Y

cd physical-ai-textbook
```

---

### Step 2: Update docusaurus.config.ts

Replace the content of `docusaurus.config.ts` with:

```typescript
import {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Essential Guide to Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://hamza699.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/physical-ai-textbook/',

  // GitHub pages deployment config.
  organizationName: 'hamza699',
  projectName: 'physical-ai-textbook',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

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
          editUrl:
            'https://github.com/hamza699/physical-ai-textbook/tree/main',
        },
        blog: {
          showReadingTime: true,
          editUrl:
            'https://github.com/hamza699/physical-ai-textbook/tree/main',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/hamza699/physical-ai-textbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Discussions',
              href: 'https://github.com/hamza699/physical-ai-textbook/discussions',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/hamza699/physical-ai-textbook',
            },
          ],
        },
      ],
      copyright: `Copyright © 2025 Physical AI Textbook. Licensed under CC-BY-4.0.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
```

---

### Step 3: Update sidebars.ts

Replace the content of `sidebars.ts` with:

```typescript
import type {SidebarsConfig} from '@docusaurus/types';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'intro',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 1: Introduction to Physical AI',
      items: [
        'chapters/chapter-1-intro',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: Humanoid Robotics Basics',
      items: [
        'chapters/chapter-2-humanoid',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: ROS 2 Fundamentals',
      items: [
        'chapters/chapter-3-ros2',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4: Digital Twin Simulation',
      items: [
        'chapters/chapter-4-digital-twin',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5: Vision-Language-Action Systems',
      items: [
        'chapters/chapter-5-vla',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 6: Capstone Project',
      items: [
        'chapters/chapter-6-capstone',
      ],
    },
  ],
};

export default sidebars;
```

---

### Step 4: Test Build

```bash
cd c:\Users\digital\claude_first\physical-ai-textbook

npm run build
```

**Expected output:**
```
✓ Build success
Build time: XX seconds (should be < 30 seconds)
Output: ./build/
```

---

### Step 5: Test Local Server

```bash
npm start
```

**Expected output:**
```
[INFO] Docusaurus server started on http://localhost:3000
```

**Verify in browser:**
- [ ] Homepage loads at http://localhost:3000
- [ ] Sidebar shows all 6 chapters
- [ ] Dark/light mode toggle works
- [ ] Navigation works
- [ ] No console errors

Press `Ctrl+C` to stop the server.

---

### Step 6: Commit to Git

```bash
git add .
git commit -m "feat: initialize Docusaurus v3 project with chapter structure"
git push origin main
```

---

### ✅ Task 1.1.2 Verification Checklist

- [ ] `npm run build` completes in < 30 seconds
- [ ] `npm start` runs without errors
- [ ] Homepage loads on http://localhost:3000
- [ ] All 6 chapters visible in sidebar
- [ ] Dark mode toggle functional
- [ ] No console errors or warnings
- [ ] Changes committed to git

**⏱️ Time: 1 hour**  
**✅ Status: Ready for next task**

---

## ✅ Task 1.1.3: Set Up GitHub Actions (1 hour)

### Step 1: Create Workflow File

Create `.github/workflows/deploy.yml` with this content:

```yaml
name: Deploy to GitHub Pages (Production)

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: pages
  cancel-in-progress: true

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build-frontend:
    runs-on: ubuntu-latest
    outputs:
      cache-key: ${{ steps.build.outputs.cache-key }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build Docusaurus
        id: build
        run: |
          npm run build
          echo "cache-key=$(date +%s)" >> $GITHUB_OUTPUT

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./build

  deploy-frontend:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build-frontend
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  test-backend:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt

      - name: Run tests
        run: |
          python -m pytest backend/tests/ -v
```

---

### Step 2: Commit Workflow

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: add GitHub Actions deployment workflow"
git push origin main
```

---

### Step 3: Monitor Workflow

1. Go to https://github.com/hamza699/physical-ai-textbook/actions
2. Watch the workflow run
3. Should see:
   - ✅ build-frontend: PASSED
   - ✅ deploy-frontend: DEPLOYED

**Wait 2-3 minutes for deployment to complete.**

---

### Step 4: Verify GitHub Pages Deployment

1. Open https://hamza699.github.io/physical-ai-textbook/
2. You should see the Docusaurus homepage
3. Check browser console (F12) for any errors
4. Navigate through chapters

---

### ✅ Task 1.1.3 Verification Checklist

- [ ] `.github/workflows/deploy.yml` created and committed
- [ ] Workflow appears in Actions tab
- [ ] build-frontend job passes
- [ ] deploy-frontend job succeeds
- [ ] GitHub Pages URL accessible
- [ ] Site displays correctly
- [ ] No console errors

**⏱️ Time: 1 hour**  
**✅ Status: COMPLETE**

---

## 🎉 DAY 1 SUMMARY

| Task | Time | Status |
|------|------|--------|
| 1.1.1 Create GitHub Repo | 30 min | ⏳ Ready |
| 1.1.2 Initialize Docusaurus | 1 hour | ⏳ Ready |
| 1.1.3 Set up GitHub Actions | 1 hour | ⏳ Ready |
| **TOTAL** | **~3 hours** | **✅ Ready** |

---

## 📋 Quick Commands Reference

```bash
# Clone repo
cd c:\Users\digital\claude_first
git clone https://github.com/hamza699/physical-ai-textbook.git
cd physical-ai-textbook

# Copy Docusaurus files
xcopy ..\my-website\* . /E /I /Y

# Test build
npm run build

# Start dev server
npm start

# Commit and push
git add .
git commit -m "your message"
git push origin main

# View actions
# https://github.com/hamza699/physical-ai-textbook/actions

# View live site
# https://hamza699.github.io/physical-ai-textbook/
```

---

## 🚀 START NOW!

Ready to begin? Start with **Task 1.1.1** above! ✅

**Next milestone:** By end of Day 1, your site should be live at https://hamza699.github.io/physical-ai-textbook/

Good luck! 🚀

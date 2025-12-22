# 🚀 QUICK REFERENCE - Infrastructure Setup Card

**Print this or keep it handy during execution!**

---

## 📌 PHASE 1: GitHub Secrets (15 min)

**Go to:** https://github.com/hamza49699/physical-ai-textbook/settings/secrets/actions

**Create 4 Secrets:**
```
1. QDRANT_URL = https://placeholder-qdrant.qdrant.io
2. QDRANT_API_KEY = placeholder-key-xxx
3. DATABASE_URL = postgresql://user:pass@neon.tech/textbook_rag
4. OPENAI_API_KEY = sk-placeholder-key-xxx
```

**Verify:** All 4 appear in the list ✅

---

## 📌 PHASE 2A: Qdrant Cloud (20 min)

**Signup:** https://cloud.qdrant.io/

**Create Cluster:**
- Name: `physical-ai-textbook-prod`
- Region: `us-east-1`
- Storage: `100MB` (free)

**Get Credentials:**
- Cluster URL: `https://[xxx]-qdrant.a.run.app`
- API Key: From Settings → API Keys

**Test Connection:**
```bash
curl -X GET "https://[url]/health" -H "api-key: [key]"
# Expected: {"status":"ok"}
```

**Update GitHub Secret:**
- `QDRANT_URL` = Real cluster URL
- `QDRANT_API_KEY` = Real API key

---

## 📌 PHASE 2B: PostgreSQL / Neon (20 min)

**Signup:** https://neon.tech/

**Create Project:**
- Name: `physical-ai-textbook`
- Database: `textbook_rag`
- Region: `us-east-1`
- Version: `15.x` or latest

**Get Connection String:**
- Format: `postgresql://[user]:[pass]@[host].neon.tech/textbook_rag?sslmode=require`
- Copy from "Connection strings" tab

**Initialize Database:**
```python
import psycopg2
conn = psycopg2.connect('[connection-string]')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        content TEXT,
        embedding VECTOR(1536),
        created_at TIMESTAMP DEFAULT NOW()
    );
''')
conn.commit()
cursor.close()
conn.close()
print('✅ Schema created')
```

**Update GitHub Secret:**
- `DATABASE_URL` = Real connection string

---

## 📌 PHASE 3: Railway Backend (15 min)

**Go to:** https://railway.app/

**Create Project:**
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Authorize & Select: `hamza49699/physical-ai-textbook`
4. Railway auto-builds (3-5 min)

**Add Environment Variables:**
- `QDRANT_URL` = From GitHub Secrets
- `QDRANT_API_KEY` = From GitHub Secrets
- `DATABASE_URL` = From GitHub Secrets
- `OPENAI_API_KEY` = From GitHub Secrets
- `PORT` = 8000
- `ENVIRONMENT` = production

**Get Domain URL:**
- Format: `https://physical-ai-backend-xxx.railway.app`

**Test Health Endpoint:**
```bash
curl https://[domain].railway.app/health
# Expected: {"status":"healthy","service":"Physical AI Textbook API","version":"1.0.0"}
```

---

## 📌 PHASE 4: Verification (10 min)

**Test All Endpoints:**

| Endpoint | Command | Expected |
|----------|---------|----------|
| Basic Health | `curl https://[domain]/health` | 200 OK |
| Database | `curl https://[domain]/health/db` | 200 OK, connected |
| Qdrant | `curl https://[domain]/health/qdrant` | 200 OK, connected |
| Root | `curl https://[domain]/` | 200 OK + docs link |
| API Docs | `curl https://[domain]/docs` | 200 OK, Swagger UI |

**Latency Test:**
```bash
time curl https://[domain]/health
# Target: < 1000ms (1 second)
```

**View Logs:**
```bash
# Railway CLI (if installed)
railway logs --follow
```

---

## 📞 Troubleshooting Quick Tips

| Problem | Solution |
|---------|----------|
| Qdrant health fails | Check API key format, cluster status |
| PostgreSQL connection fails | Verify SSL flag (?sslmode=require) in connection string |
| Railway build fails | Check requirements.txt syntax, Python 3.9+ needed |
| Health endpoints 500 | Check all 4 environment variables are set |
| Slow latency | Wait for cold start, check Railway tier |
| API docs broken | Verify /docs endpoint is working |

---

## 🔐 Security Reminders

✅ **DO:**
- Use GitHub Secrets for all sensitive data
- Rotate API keys every 3 months
- Use HTTPS everywhere
- Log deployment events

❌ **DON'T:**
- Hardcode secrets in code
- Share API keys in Slack/Email
- Commit .env files
- Use same password twice

---

## 📊 Service URLs (Save These!)

After Phase 3 completion:

```
Frontend: https://hamza699.github.io/physical-ai-textbook/
Backend: https://[your-domain].railway.app
Qdrant Dashboard: https://cloud.qdrant.io/
Neon Dashboard: https://console.neon.tech/
Railway Dashboard: https://railway.app/
GitHub Repo: https://github.com/hamza49699/physical-ai-textbook
```

---

## ⏱️ Time Budget

```
Phase 1: GitHub Secrets       15 min  ████░░░░░░
Phase 2a: Qdrant Cloud        20 min  █████░░░░░░
Phase 2b: PostgreSQL          20 min  █████░░░░░░
Phase 3: Railway Deploy       15 min  ████░░░░░░
Phase 4: Verification         10 min  ███░░░░░░░
                    ─────────────────
TOTAL:                         80 min  ██████████
```

---

## ✅ Final Checklist

- [ ] Phase 1 complete (4 secrets created)
- [ ] Phase 2a complete (Qdrant cluster live)
- [ ] Phase 2b complete (PostgreSQL ready)
- [ ] Phase 3 complete (Backend deployed)
- [ ] All 5 endpoints return 200 OK
- [ ] Latency < 1 second verified
- [ ] API docs accessible
- [ ] No errors in logs
- [ ] Team notified

**Status when complete:** ✅ INFRASTRUCTURE READY FOR DAY 2

---

## 📚 Full Guides Location

```
c:\Users\digital\claude_first\EXECUTION-PLAN-SPEC.md
c:\Users\digital\claude_first\TASK-1.1.4-ENV-SETUP.md
c:\Users\digital\claude_first\TASK-1.2.1-2.2-PROVISION.md
c:\Users\digital\claude_first\INFRASTRUCTURE-CHECKLIST.md
c:\Users\digital\claude_first\EXECUTION-SUMMARY.md (Overview)
```

---

## 🎯 You're Ready!

**Next Action:** Open `EXECUTION-PLAN-SPEC.md` and start Phase 1 ✨

Good luck! Questions? Check the troubleshooting sections! 🚀


## Project: Tradify — Trading Analytics Platform

**One-liner:** Upload trade history & portfolio → AI-powered analysis: mistakes, hidden risk, agentic investigation of flagged trades.

---

### CORE SYSTEM (yeh banega, bas yeh banega)

**Flow 1 — Upload & Parse**

User CSV/broker export upload karta hai (Zerodha/Groww format) → validate → parse → Trade/Holding records banते hain → async processing (Celery) → status track.

*Approve karne layak decision:* kaunse 2 broker formats support karne hain (2 se zyada nahi).

**Flow 2 — Portfolio Analytics (pure DRF, no AI)**

Holdings se: sector concentration (hidden linkage included), diversification score, P&L summary, win rate, overtrading days, SL-discipline stats. Sab computed, rule-based, fast APIs.

*Decision:* kaunse 5-6 metrics — maine upar likh diye, in se shuru.

**Flow 3 — Risk Engine (rule-based, no AI)**

Har parsed trade pe rules chalte hain: position size > X% of capital, no stop-loss, revenge trade (loss ke Y min andar re-entry), overtrading (din me > N trades). Flag hota hai → DB me `RiskFlag` record.

*Decision:* 4 rules se start, configurable thresholds.

**Flow 4 — Agentic Investigation (yeh RAG/agentic core hai)**

`RiskFlag` bana → agent trigger → agent retrieve karta hai: us din/time ki news (ingested + embedded), user ke past similar flagged trades, pattern history → multi-step reasoning → investigation report ("yeh trade kyun problematic tha, pehle bhi 3 baar same pattern") → save + API se dikhao.

Yehi interview ka 20-minute piece hai.

**Flow 5 — Ask-your-portfolio (RAG Q&A)**

"Mera banking exposure kitna hai?" "Is month sabse badi galti?" → agent decide karta hai: DB query chahiye, vector search chahiye, ya dono → answer with data citations.

**Flow 6 — Auth & Multi-user**

JWT, apna data apna, permissions, throttling. AI se likhwa, tu review kar.

**Deploy:** EC2 + RDS + pgvector, monolith with modular apps (`accounts`, `trades`, `portfolio`, `risk`, `agent`).

---

### FUTURE SCOPE (README me likhega, banayega NAHI — new job ke baad)

1. Tax module (regime comparison, 80C room, LTCG/STCG summary)
2. Live broker connect (Kite API)
3. Dividend/upcoming opportunities
4. Tax harvesting suggestions
5. Long-term stock discovery
6. MCP server layer
7. Microservices split

---

**Order of build:** Flow 6 → 1 → 2 → 3 → 4 → 5. (Auth pehle kyunki sab uspe depend karta hai; AI flows last kyunki data pehle chahiye.)

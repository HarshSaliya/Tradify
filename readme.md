
# Tradify

## Overview

Paper trading platform with a RAG pipeline for stock analytics, built as a DRF depth + RAG integration resume project.

## Goal

Not a Groww clone — MVP scope only. Built to demonstrate:

- Django REST Framework depth (models, serializers, views, auth, permissions, service layer)
- RAG integration (plain RAG, with an optional agentic layer)
- Production practices (env config, logging, tests, deployment)

UI is Django templates, built with AI assistance — UI polish is not the learning focus of this project.

## Timeline

3 months, starting **27 Jul 2026**. Built part-time as a side project.

## Tech stack

- **Backend:** Django + Django REST Framework
- **DB:** SQLite locally → PostgreSQL (RDS) for deployment
- **Vector store:** Qdrant
- **Embeddings:** BAAI embeddings (existing pipeline)
- **Auth:** Session Auth (recommended fit — UI is Django templates, DRF browsable API works fine with it) or JWT (`djangorestframework-simplejwt`) if a future mobile client angle is wanted. **Status: not finalized yet — decide before Week 1 models.**
- **Deployment:** EC2 + RDS + Gunicorn + Nginx (+ S3 only if needed)

## Scope — explicitly out

Charts, real-time price feed, price alerts, full broker features.

## Models

| Model           | Fields                                                                | Notes                                                                                                                                                                                        |
| --------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Trade`       | user, stock_symbol, trade_type (buy/sell), quantity, price, timestamp | Immutable ledger — source of truth / audit trail                                                                                                                                            |
| `Holding`     | user, stock_symbol, quantity, avg_buy_price                           | Materialized/derived table, kept in sync via a service function (not signals) — updated inside a DB transaction with`select_for_update()` to prevent race conditions on concurrent trades |
| `Profile`     | user (OneToOne), virtual_balance                                      |                                                                                                                                                                                              |
| `Watchlist`   | user, stock_symbol, added_at                                          |                                                                                                                                                                                              |
| `TradingCall` | user, stock_symbol, query_text, rag_response, call_type, created_at   | RAG output log — the resume/interview highlight table                                                                                                                                       |

**Design decisions locked:**

- `Holding` is kept as a materialized table rather than derived on-the-fly from `Trade` — better read performance (single indexed lookup vs. aggregating trade history) and a stronger interview talking point (`atomic()`, row locking).
- Trade execution goes through a `services.py` (`execute_trade()`) rather than fat models/views.
- Cost basis method: **weighted-average** (not FIFO/LIFO) — simpler for MVP scope.
- `TradingCall.call_type` and `Trade.trade_type` share a consistent naming convention but stay separate enums (`TradingCall` needs a third `hold` option that `Trade` never will).
- Sell validation (can't sell more than you hold) is enforced via serializer `validate()`.

## RAG plan

**Phase 1 — Plain RAG (build first, get fully working):**
Stock query → embed → Qdrant retrieve top-k news chunks → LLM reasons over context → buy/hold/sell + reasoning → saved to `TradingCall`. One endpoint, one fixed flow, no tool-calling.

**Phase 2 — Agentic RAG (layer on top, optional/time-permitting):**
Give the LLM 2–3 tools and let it decide what to retrieve:

- `search_news(symbol, query)` — existing Qdrant retrieval
- `get_user_holding(symbol)` — checks user's own position before answering
- optionally `get_recent_trades(symbol)`

Build the tool-calling loop directly against the raw LLM API (not LangChain/LlamaIndex agents) — more explainable in an interview.

**News source:** NewsAPI / MoneyControl / ET RSS → clean text → BAAI embeddings → Qdrant.

## Roadmap

**Month 1 — DRF core (no RAG, no UI)**

- Week 1: Project setup, `.env` config, custom User/Profile model, auth decision, git repo + README skeleton
- Week 2: `Trade`, `Holding` models + `execute_trade()` service (with `select_for_update`), serializers with `validate()`
- Week 3: `Watchlist` CRUD, `IsOwner` custom permission, DRF views/viewsets
- Week 4: APITestCase tests, logging setup, custom DRF exception handler

**Month 2 — RAG + basic UI**

- Week 5: News ingestion pipeline (scheduled script, not a DRF view)
- Week 6: `TradingCall` model + plain RAG endpoint
- Week 7: Django templates UI — login, portfolio, trade form, watchlist, ask-for-a-call form
- Week 8: Agentic layer (only if Weeks 5–7 finished on time)

**Month 3 — Production hardening + deploy**

- Week 9: Logging (request/error logs), error handling audit, input validation edge cases
- Week 10: Test coverage push, full README with API docs
- Week 11: Deployment — EC2, RDS (Postgres) migration, env vars, Gunicorn + Nginx
- Week 12: Buffer — bug fixes, UI polish, interview talking points (Holding vs. derive, plain vs. agentic RAG, transaction handling)

## Production checklist

- [ ] `.env` config
- [ ] Validation / error handling
- [ ] Logging (request + error)
- [ ] Tests (DRF `APITestCase`)
- [ ] README with full API docs (endpoints, request/response examples)
- [ ] Deployment (EC2 + RDS + S3 if needed)

## Open items

- **Auth: Session vs JWT** — not finalized. Recommendation: Session Auth, since the UI is Django templates.

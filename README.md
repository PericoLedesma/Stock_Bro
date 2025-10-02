# Stock_Bro
**Stock_Bro** is a multi-agent investment guidance system that provides portfolio management and market analysis capabilities. The application follows a modern full-stack architecture with a React frontend and FastAPI backend, implementing a microservices-oriented approach for scalability and maintainability.


### Core Principles
- **Multi-Agent Architecture**: Specialized agents for different investment functions
- **Real-time Data Processing**: Live market data integration and analysis
- **Scalable Backend**: FastAPI with async capabilities for high performance
- **Responsive Frontend**: React-based SPA with modern UI/UX
- **Data-Driven Decisions**: Comprehensive analytics and risk assessment


---------
## 📦 Application features

### Portfolio
- Create and maintain a database of the current portfolio.
- Accept user inputs: stock ticker, purchase date, and purchase price.
- Track gains/losses and price performance; compute profitability by time period.
- Provide a brief portfolio analysis:
  - Risks
  - News
  - Sell or hold recommendation

### Search for New Opportunities
- Identify investment trends and momentum.
- Suggest where to invest (e.g., sectors, tickers, ETFs).
- Provide a market overview (breadth, volatility, macro context).

---------

## 🎯 Architecture

Frontend (React) → API Gateway (FastAPI) → Backend → Agents → Database (PostgreSQL)
                                      ↓
                              External APIs (Market Data)

## Basic Folder Structure

  Stock_Bro/
  ├── frontend/               # React SPA (components, routes, state, assets)  
  │   ├── src/  
  │   ├── public/   
  │   └── package.json  
  ├── backend/                # FastAPI app (routers, models, services)  
  │   ├── app/   
  │   │   ├── api/            # Route handlers / controllers  
  │   │   ├── core/           # Settings, security, middlewares  
  │   │   ├── services/       # Business logic  
  │   │   ├── agents/         # Domain agents (analysis, portfolio, news)   
  │   │   ├── db/             # SQLAlchemy models, migrations  
  │   │   └── main.py         # FastAPI entrypoint  
  │   ├── requirements.txt  
  │   └── alembic/  
  ├── api-gateway/            # Optional gateway if separated from backend  
  ├── data/                   # Seeds, fixtures, exported datasets  
  ├── infra/                  # IaC (Terraform), Docker, k8s manifests  
  ├── scripts/                # One-off scripts, CLIs, utilities  
  ├── tests/                  # Backend + e2e tests  
  ├── docs/                   # Architecture, ADRs, runbooks  
  ├── .github/                # CI/CD workflows  
  ├── ARCHITECTURE.md         # High-level architecture overview  
  └── README.md  


### 🖥️ Frontend (react-js)

- **Core Components**
  - **Layout**: App shell, header, sidebar, theme toggle
  - **Navigation**: Topbar, sidebar, route guards
  - **Dashboard**: KPIs, market overview, quick actions
  - **PortfolioTable**: Holdings table, sorting, filtering, pagination
  - **PositionDetails**: Ticker view with price, fundamentals, news
  - **Search**: Ticker/ETF search with autocomplete
  - **Charts**: Price/returns, allocation, drawdown
  - **NewsFeed**: Relevant headlines per portfolio/ticker
  - **Alerts**: Threshold/risk alerts list and settings
  - **Settings**: Profile, preferences, API keys
  - **Auth**: Sign-in, sign-up, forgot password
  - **ErrorBoundary & Loaders**: Graceful errors and skeletons

- **Technology Stack**
  - **Framework**: React + TypeScript
  - **Bundler/Dev**: Vite
  - **Routing**: React Router
  - **State**: Zustand or Redux Toolkit (choose one)
  - **Server State**: TanStack Query (React Query)
  - **UI**: MUI or Tailwind CSS + Headless UI (choose one)
  - **Charts**: Recharts or Chart.js
  - **Forms**: React Hook Form + Zod
  - **Testing**: Vitest/Jest + Testing Library; E2E with Playwright/Cypress
  - **Quality**: ESLint + Prettier + Husky (pre-commit)
  - **i18n (optional)**: i18next

### 🧩 Backend Components and Technology

- **Core Modules**
  - **API Routers**: Versioned endpoints (`/api/v1`) for auth, portfolio, search, market
  - **Schemas**: Pydantic models for request/response validation
  - **Services**: Business logic (portfolio analytics, risk, signals)
  - **Repositories**: Data access layer (SQLAlchemy 2.0 ORM + queries)
  - **Agents**: Specialized agents for analysis, news, recommendations
  - **Market Clients**: External API integrations (price, news, fundamentals)
  - **Tasks**: Background jobs for data refresh, alerts (Celery/RQ)
  - **DB Layer**: PostgreSQL, migrations with Alembic
  - **Caching**: Redis for hot data, rate limiting, and idempotency
  - **Auth/Security**: JWT auth (access/refresh), role-based guards, CORS
  - **Config**: Typed settings via environment (Pydantic Settings)
  - **Observability**: Structured logging, metrics, tracing hooks

- **Technology Stack**
  - **Framework**: FastAPI (async-first)
  - **Runtime**: Python 3.11+
  - **Server**: Uvicorn (dev), Gunicorn+Uvicorn workers (prod)
  - **ORM**: SQLAlchemy 2.x + Alembic
  - **Validation**: Pydantic v2
  - **Background Jobs**: Celery or RQ + Redis
  - **HTTP**: httpx (async external calls), Tenacity (retries)
  - **Auth**: python-jose or Authlib (JWT/OAuth2)
  - **DB**: PostgreSQL
  - **Cache/Queue**: Redis
  - **Testing**: pytest + httpx test client + factory-boy
  - **Quality**: Ruff or Flake8, Black, mypy, pre-commit
  - **Docs**: OpenAPI/Swagger auto-generated by FastAPI

- **Non-Functional**
  - **API Versioning**: `/api/v1` with deprecation policy
  - **Security**: CORS, rate limiting (via proxy/gateway), input sanitization
  - **Resilience**: Timeouts, retries, circuit breakers at client layer
  - **Observability**: Request logging, metrics (Prometheus), error tracking (Sentry)

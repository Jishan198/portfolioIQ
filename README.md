# PortfolioIQ — AI-Powered Stock Portfolio Risk Analyser

> A full-stack Django web application that uses **Google Gemini AI** to analyse stock portfolio risk, identify behavioral traps, and deliver instant AI-generated risk reports — all with a real-time, reactive UI powered by HTMX.

---

## 🖥️ Live Demo

> Run locally at `http://127.0.0.1:8000` after setup.

---

## 📸 Screenshots

| Dashboard | AI Risk Engine |
|-----------|---------------|
| Portfolio overview with P&L tracking | Real-time AI analysis with risk score |

---

## ✨ Features

- 🔐 **Custom Auth System** — Register, login, logout with Django session auth + JWT support for API access
- 📊 **Portfolio Dashboard** — Track holdings, quantities, buy prices, total invested, current value, and P&L in real time
- ➕ **Add / Remove Holdings** — Inline HTMX-powered form that updates the table instantly without page reload
- 🤖 **AI Risk Engine** — Enter any NSE/BSE ticker and get an instant Gemini AI risk report with:
  - Risk score (0–10)
  - Key vulnerabilities
  - Behavioral traps retail investors fall into
  - A punchy final verdict
- 📷 **Portfolio Vision** — Upload a broker screenshot and Gemini visually analyses your entire portfolio
- ⚡ **Async Task Queue** — All AI analysis runs in the background via Celery so the UI never blocks
- 🔄 **Real-time Polling** — HTMX auto-polls every 2 seconds for analysis status until COMPLETED
- 🍩 **Allocation Chart** — Doughnut chart showing portfolio allocation by ticker (Chart.js)
- 🌐 **REST API** — Full DRF-powered API for portfolios and holdings with JWT authentication

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 5.0** | Core web framework |
| **Django REST Framework** | REST API for portfolios and holdings |
| **SimpleJWT** | JWT token auth for API endpoints |
| **Celery** | Async background task queue for AI jobs |
| **Redis (Upstash)** | Celery message broker |
| **PostgreSQL** | Primary relational database |
| **django-environ** | Environment variable management |
| **django-cors-headers** | CORS handling for API |

### AI & Data
| Technology | Purpose |
|------------|---------|
| **Google Gemini 2.0 Flash** | AI risk analysis engine |
| **Gemini Vision API** | Analyses broker screenshots visually |
| **yfinance** | Stock market data fetching |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTMX 1.9** | Reactive UI without writing JavaScript |
| **Tailwind CSS (CDN)** | Utility-first styling |
| **Chart.js** | Portfolio allocation doughnut chart |
| **Django Templates** | Server-side HTML rendering with partials |

---

## 🏗️ Project Architecture

```
ai-powered-stock-portfolio-risk-analysis/
│
├── core/                   # Django project config
│   ├── settings.py         # Environment-based settings
│   ├── urls.py             # Root URL routing
│   └── celery.py           # Celery app initialisation
│
├── users/                  # Custom auth app
│   ├── models.py           # Custom User model
│   ├── views.py            # Login, register, logout views
│   ├── forms.py            # Custom user creation form
│   └── serializers.py      # DRF user serializer
│
├── portfolios/             # Portfolio management app
│   ├── models.py           # Portfolio + Holding models
│   ├── views.py            # Dashboard, add/delete holding views
│   ├── serializers.py      # DRF serializers
│   └── urls.py             # Portfolio API + web routes
│
├── analysis/               # AI risk analysis app
│   ├── models.py           # StockAnalysis model
│   ├── views.py            # Analysis dashboard, trigger, status views
│   ├── services.py         # Gemini API integration (text + vision)
│   ├── tasks.py            # Celery async tasks
│   ├── urls.py             # Analysis routes
│   └── templatetags/       # Custom json_filters template tag
│
└── templates/              # All HTML templates
    ├── layouts/
    │   └── base.html       # Base layout with nav, HTMX, Tailwind
    ├── auth/
    │   ├── login.html
    │   └── register.html
    ├── partials/
    │   └── holdings_table.html   # HTMX partial for live table updates
    ├── dashboard.html            # Main portfolio dashboard
    ├── analysis_dashboard.html   # AI Risk Engine page
    └── analysis_status.html      # HTMX partial for analysis result card
```

---

## ⚙️ How the AI Pipeline Works

```
User enters ticker
       │
       ▼
HTMX POST → /api/v1/trigger/
       │
       ▼
Django creates StockAnalysis(status=PENDING)
       │
       ▼
Celery task fired → analyze_stock_task.delay()
       │
       ▼
services.py → Gemini 2.0 Flash API call
       │
       ▼
JSON response saved → StockAnalysis(status=COMPLETED)
       │
       ▼
HTMX polls /api/v1/status/<id>/ every 2s
       │
       ▼
Result card swapped into page (outerHTML swap)
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL
- Redis (or Upstash Redis cloud URL)
- Google Gemini API key (get free at [aistudio.google.com](https://aistudio.google.com))

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-powered-stock-portfolio-risk-analysis.git
cd ai-powered-stock-portfolio-risk-analysis
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file in root
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/portfolioiq
GEMINI_API_KEY=your-gemini-api-key
CELERY_BROKER_URL=rediss://your-upstash-redis-url
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Start Django server
```bash
python manage.py runserver
```

### 8. Start Celery worker (new terminal)
```bash
celery -A core worker -l info -P eventlet
```

### 9. Visit the app
```
http://127.0.0.1:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/login/` | Web login | No |
| POST | `/api/v1/auth/register/` | Web register | No |
| GET | `/api/v1/portfolios/` | List portfolios | JWT |
| POST | `/api/v1/portfolios/` | Create portfolio | JWT |
| GET | `/api/v1/holdings/` | List holdings | JWT |
| POST | `/api/v1/holdings/add/` | Add holding (web) | Session |
| POST | `/api/v1/holdings/delete/<id>/` | Delete holding | Session |
| GET | `/api/v1/analysis/` | AI Risk Engine page | Session |
| POST | `/api/v1/trigger/` | Trigger AI analysis | Session |
| GET | `/api/v1/status/<id>/` | Poll analysis status | Session |
| POST | `/api/v1/upload/` | Upload screenshot | Session |

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for dev, `False` for prod |
| `DATABASE_URL` | PostgreSQL connection string |
| `GEMINI_API_KEY` | Google Gemini API key |
| `CELERY_BROKER_URL` | Redis URL (local or Upstash) |

---

## 📦 Dependencies

```
django>=5.0
djangorestframework
djangorestframework-simplejwt
django-cors-headers
django-environ
celery
eventlet
redis
google-genai
yfinance
psycopg2-binary
```

---

## 🗺️ Roadmap

- [ ] Live stock prices via yfinance on dashboard
- [ ] Top 5 Nifty stocks with daily AI risk scores
- [ ] Email alerts when risk score crosses threshold
- [ ] Deploy to Railway / Render
- [ ] Stripe freemium — limit free tier to 3 analyses/day

---

## 👤 Author

**Jishan Mohammed**
- 📧 jishanmohammed2003@gmail.com
- 🎓 B.Tech Computer Science, Sangam University (2026)
- 🔗 [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)
- 🐙 [GitHub](https://github.com/YOUR_USERNAME)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

> Built with Django, HTMX, Celery, Redis, PostgreSQL, and Google Gemini AI.

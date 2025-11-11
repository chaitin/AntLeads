# 🐜 AntLeads

**AI-driven lead management and marketing automation system**

AntLeads is an intelligent marketing platform designed to help businesses generate, manage, and convert sales leads through AI-powered automation. The system combines lead scoring, customer journey tracking, embeddable widgets, and data analytics into a unified solution.

---

## 🎯 Project Vision

AntLeads aims to provide a complete marketing automation platform with:

- **AI-Driven Intelligence**: Automated lead scoring, tagging, and prioritization
- **Multi-Channel Lead Collection**: Web forms, widgets, ads, events, and imports
- **Smart CRM**: Sales funnel visualization with automatic task creation and follow-ups
- **Embeddable Widgets**: One-line JavaScript integration for any website
- **Future Growth**: AI content generation, customer profiling, and predictive analytics

---

## ✨ Current Features

### 📊 Lead Collection & CRM Management
- **Multi-source tracking**: Capture leads from web forms, Google Ads, Facebook Ads, events, imports, and more
- **AI-powered scoring**: Automatic 0-100 lead quality scoring based on contact completeness, source, estimated value, and UTM tracking
- **Intelligent tagging**: Auto-tag leads (enterprise/mid-market/smb, hot/warm/cold-lead, decision-maker, etc.)
- **Priority management**: Automatic priority assignment (urgent/high/medium/low)
- **Complete contact info**: Email, phone, company, social profiles, website

### 📈 Sales Funnel & Pipeline
- **7-stage funnel**: NEW → CONTACTED → QUALIFIED → PROPOSAL → NEGOTIATION → CLOSED → LOST
- **Conversion tracking**: Stage-by-stage conversion rates and metrics
- **Pipeline value**: Track estimated revenue through each stage
- **Funnel visualization**: Interactive charts and analytics
- **Historical data**: Filter by date range for trend analysis

### ✅ Task Management & Automation
- **Automatic task creation**: Stage transitions trigger follow-up tasks
  - NEW lead → "Initial contact" task (1 day, High priority)
  - CONTACTED → "Follow-up" task (3 days, Medium)
  - QUALIFIED → "Schedule demo" task (2 days, High)
  - PROPOSAL → "Send proposal" + "Follow-up" tasks (1 day + 5 days)
- **Task types**: Call, email, meeting, demo, follow-up, proposal
- **Status tracking**: Pending, in progress, completed, cancelled
- **Reminders**: Due date and reminder scheduling
- **Assignment**: Assign tasks to team members

### 🌐 Embeddable Web Widget
- **One-line integration**: Add lead collection to any website with a single `<script>` tag
- **Customizable**: Configure colors, position, fields, messages
- **Floating button**: Auto-appears in 4 corner positions (top/bottom, left/right)
- **Element binding**: Bind to any existing button or div on your page
- **Auto-open**: Optionally auto-open modal after configurable delay
- **Form fields**: name, email, phone, company, message (all configurable)
- **AI scoring on submit**: Every submission is automatically scored and tagged
- **UTM tracking**: Captures URL, referrer, and campaign parameters
- **No dependencies**: Pure JavaScript, works everywhere

---

## 🏗️ Architecture

AntLeads follows a **modular monorepo** structure:

```
antleads/
├── apps/
│   ├── api/          # FastAPI backend (Python 3.11+)
│   ├── web/          # React + TypeScript dashboard
│   └── widget/       # Embeddable JavaScript SDK
├── packages/
│   ├── core/         # Shared domain models and schemas
│   └── ml/           # AI scoring engine and future ML models
├── data/
│   ├── sample/       # Sample data for development
│   └── raw/          # Large datasets (gitignored)
├── tests/            # Test suites mirroring source structure
└── docs/             # Architecture Decision Records (ADRs)
```

### Technology Stack

**Backend**
- FastAPI (async Python web framework)
- SQLAlchemy (async ORM with SQLite)
- Pydantic (data validation and schemas)
- AI scoring engine (rule-based, future LLM integration)

**Frontend**
- React 18 + TypeScript 5
- React Router (navigation)
- React Query (data fetching and caching)
- Axios (HTTP client)
- Lucide React (icons)
- Recharts (data visualization)

**Widget SDK**
- Pure JavaScript (no dependencies)
- CORS-enabled public API
- Responsive design with inline styles

**DevOps**
- uv (Python package management)
- pnpm (frontend package management)
- Make (build automation)
- Git (version control)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- pnpm (install: `npm install -g pnpm`)
- uv (install: `pip install uv`)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/chaitin/AntLeads.git
cd AntLeads
```

2. **Install dependencies**
```bash
make bootstrap
```

This will:
- Install Python dependencies via `uv`
- Install frontend dependencies via `pnpm`
- Set up the development environment

### Running the Application

**Start the backend API** (in one terminal)
```bash
make api
# or manually:
cd apps/api && uv run uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Start the frontend** (in another terminal)
```bash
make web
# or manually:
cd apps/web && pnpm run dev
```

**Access the application**
- Frontend Dashboard: http://localhost:3000
- Backend API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Sample Data

Import sample leads and tasks for testing:
```bash
# Generate sample data
python data/sample/generate_sample_data.py

# Import into database
uv run python data/sample/import_sample_data.py
```

---

## 📖 Usage

### Dashboard
Navigate to http://localhost:3000 to access:
- **Dashboard**: Overview with key metrics (total leads, conversion rate, pipeline value)
- **Leads**: Browse, search, filter, and create leads
- **Tasks**: Manage follow-up tasks and reminders
- **Funnel**: Visualize sales pipeline and conversion rates
- **Widgets**: Create and manage embeddable lead collection widgets

### Creating a Lead Collection Widget

1. Go to **Widgets** page
2. Click **Create Widget**
3. Configure:
   - Widget name (for internal use)
   - Form title and description
   - Form fields (name, email, phone, company, message)
   - Primary color and button position
   - Auto-open behavior
4. Copy the embed code:
```html
<script src="http://your-domain.com/static/widget.js"
        data-widget-id="wgt_YOUR_WIDGET_ID"></script>
```
5. Paste before `</body>` tag on your website

**Advanced: Bind to existing element**
```html
<button id="contact-us">Contact Us</button>
<script src="http://your-domain.com/static/widget.js"
        data-widget-id="wgt_YOUR_WIDGET_ID"
        data-bind-to="#contact-us"></script>
```

**Programmatic control**
```javascript
// Open widget
window.AntLeadsWidget.open();

// Close widget
window.AntLeadsWidget.close();

// Check status
if (window.AntLeadsWidget.isOpen()) {
  console.log('Widget is open');
}
```

---

## 🧪 Development

### Code Quality
```bash
# Lint and format
make lint

# Run tests
make test

# Run tests with coverage
make test -- --cov
```

### Project Structure

**Backend API** (`apps/api/`)
```
apps/api/
├── main.py              # FastAPI app initialization
├── config.py            # Settings and environment variables
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy ORM models
├── routes/              # API endpoints
│   ├── leads.py         # Lead CRUD
│   ├── tasks.py         # Task management
│   ├── funnel.py        # Funnel analytics
│   ├── automation.py    # Task automation
│   └── widgets.py       # Widget management
└── services/            # Business logic
    └── task_automation.py
```

**Frontend** (`apps/web/`)
```
apps/web/
├── src/
│   ├── App.tsx          # Main app component with routing
│   ├── pages/           # Page components
│   │   ├── Dashboard.tsx
│   │   ├── LeadsPage.tsx
│   │   ├── TasksPage.tsx
│   │   ├── FunnelPage.tsx
│   │   └── WidgetsPage.tsx
│   ├── services/        # API clients
│   │   ├── api.ts       # Leads, tasks, funnel APIs
│   │   └── widgets.ts   # Widget API
│   └── types.ts         # TypeScript type definitions
```

**Core Models** (`packages/core/`)
```
packages/core/
├── models/
│   ├── lead.py          # Lead domain model
│   ├── task.py          # Task domain model
│   └── widget.py        # Widget configuration model
└── schemas/
    └── widget.py        # Widget API schemas
```

**ML Engine** (`packages/ml/`)
```
packages/ml/
└── lead_scoring.py      # AI scoring and tagging logic
```

---

## 🗺️ Roadmap

### ✅ Phase 1: Lead Collection & CRM (Complete)
- [x] Multi-channel lead source tracking
- [x] AI-powered lead scoring and tagging
- [x] Sales funnel visualization
- [x] Automatic task creation and reminders
- [x] Embeddable web widget

### 🚧 Phase 2: AI Marketing Engine (Planned)
- [ ] LLM-based content generation (product copy, ads, social media)
- [ ] Keyword recommendation and SEO optimization
- [ ] Multi-channel content adaptation (TikTok, Instagram, Google Ads)
- [ ] A/B testing framework for marketing content

### 📅 Phase 3: Customer Data Platform (Planned)
- [ ] Automated customer profiling
- [ ] Lifecycle management (LTV calculations)
- [ ] Multi-channel integration (email, SMS, social)
- [ ] Re-marketing recommendations

### 🔮 Phase 4: Analytics & Intelligence (Planned)
- [ ] Sales forecasting with ML
- [ ] Conversion prediction models
- [ ] Smart action recommendations
- [ ] Market trend analysis and competitor monitoring

### 🤝 Phase 5: Collaboration & Advanced Automation (Planned)
- [ ] Team task assignment and permissions
- [ ] Advanced workflow automation
- [ ] AI assistant for Q&A and report generation
- [ ] Campaign performance optimization

---

## 📝 API Documentation

Once the backend is running, visit **http://localhost:8000/docs** for interactive API documentation (Swagger UI).

### Key Endpoints

**Leads**
- `GET /api/v1/leads/` - List all leads (with pagination, filters)
- `POST /api/v1/leads/` - Create a new lead (auto-scoring enabled)
- `GET /api/v1/leads/{id}` - Get lead details
- `PATCH /api/v1/leads/{id}` - Update lead (triggers automation)
- `DELETE /api/v1/leads/{id}` - Delete lead
- `GET /api/v1/leads/stats/overview` - Get lead statistics

**Tasks**
- `GET /api/v1/tasks/` - List all tasks (with filters)
- `POST /api/v1/tasks/` - Create task
- `PATCH /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

**Funnel**
- `GET /api/v1/funnel/` - Get funnel analytics (with date filters)

**Widgets**
- `POST /api/v1/widgets/` - Create widget configuration
- `GET /api/v1/widgets/` - List all widgets
- `GET /api/v1/widgets/{widget_id}/config` - Get public widget config (CORS-enabled)
- `POST /api/v1/widgets/{widget_id}/submit` - Submit widget form (CORS-enabled)
- `DELETE /api/v1/widgets/{id}` - Delete widget

**Automation**
- `GET /api/v1/automation/overdue` - Get overdue tasks
- `GET /api/v1/automation/reminders` - Get tasks needing reminders
- `POST /api/v1/automation/stale-leads` - Create tasks for stale leads

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Branch naming**: `feature/your-feature-name` or `fix/bug-description`
2. **Commit convention**: Use conventional commits (feat:, fix:, docs:, chore:, test:)
3. **Code style**:
   - Python: Run `make lint` (ruff + black)
   - TypeScript: Prettier + ESLint (runs on save)
4. **Tests**: Add tests for new features (target ≥85% coverage)
5. **Pull requests**: Include description, test results, and link to related issue

---

## 📄 License

This project is currently proprietary. All rights reserved.

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [Recharts](https://recharts.org/) - Charting library
- [Lucide](https://lucide.dev/) - Icon set

---

## 📞 Contact

For questions or support, please open an issue on GitHub.

**Project maintained by Chaitin Tech**

---

<div align="center">
  <p>Built with ❤️ for marketing automation</p>
  <p>🐜 AntLeads - Smart leads, smarter business</p>
</div>

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AntLeads** is an AI-driven online marketing system designed to help businesses generate, manage, and convert product sales leads through intelligent automation. The platform combines AI content generation, lead scoring, customer journey tracking, and data analytics into a unified marketing automation solution.

### Core Value Proposition
- **AI-Driven Content**: Auto-generate marketing copy, ad creatives, product descriptions, and promotional campaigns
- **Intelligent Lead Management**: Real-time lead tracking, scoring, and conversion path analysis
- **Full-Cycle Automation**: From content creation → distribution → lead collection → conversion tracking
- **Data Intelligence**: AI-powered sales funnel analysis, ROI tracking, customer profiling, and strategy optimization

## Architecture Overview

The project follows a modular monorepo structure:

- `apps/api/` - Marketing automation backend (FastAPI or similar Python framework)
- `apps/web/` - Dashboard and UI (React/TypeScript)
- `packages/core/` - Shared domain logic, schemas, and business rules
- `packages/ml/` - AI models for lead scoring, content generation, and predictions
- `tests/` - All test files mirroring the source structure
- `docs/` - Architecture Decision Records (ADRs) and design documentation
- `data/raw/` - Large datasets with provenance documentation
- `data/sample/` - Lightweight fixtures for development and testing

### Key Subsystems

1. **AI Marketing Engine** (`packages/ml/`)
   - LLM-based content generation for product copy, ads, and social media
   - Keyword recommendation and SEO optimization
   - Multi-channel content adaptation (e.g., TikTok, Instagram, Google Ads)

2. **Lead Collection & CRM** (`apps/api/`)
   - Lead source tracking (ads, forms, imports, events)
   - AI-powered lead scoring and segmentation
   - Conversion funnel visualization and stage management

3. **Customer Data Platform**
   - Automated customer profiling based on behavior and transaction data
   - Lifecycle management (LTV calculations, re-marketing recommendations)
   - Multi-channel touchpoint integration (email, SMS, social)

4. **Analytics & Intelligence**
   - Sales forecasting and conversion prediction
   - Smart action recommendations (e.g., "send discount email")
   - Market trend analysis and competitor monitoring

5. **Collaboration & Automation**
   - Team task assignment and permission management
   - Automated workflows (form submission → lead assignment → notification)
   - AI assistant for Q&A, report generation, and campaign suggestions

## Development Commands

All commands are managed via the root `Makefile` or `package.json` scripts. Every command must be idempotent and container-friendly.

### Setup & Installation
```bash
make bootstrap          # Install all dependencies (Python via uv/poetry, frontend via pnpm)
```

### Running Services
```bash
make api               # Launch backend API in hot-reload mode
make web               # Run frontend development server with mocked services
```

### Code Quality
```bash
make lint              # Run formatters and static analysis (ruff + black + prettier + eslint)
make test              # Execute full test suite (unit + integration)
make test -- --cov     # Run tests with coverage report (target ≥85% branch coverage)
```

### Single Test Execution
```bash
# Backend (pytest)
pytest tests/api/test_lead_scoring.py -v
pytest tests/api/test_lead_scoring.py::test_score_calculation -v

# Frontend (vitest)
pnpm test web/components/Dashboard.spec.tsx
```

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI (or similar async framework)
- **Formatting**: `ruff` + `black` (line length 100)
- **Testing**: `pytest` with factory fixtures
- **Naming**: `snake_case.py` for all Python files

### Frontend
- **Language**: TypeScript 5
- **Framework**: React
- **Linting**: `prettier` + `eslint` (Airbnb base config)
- **Testing**: `vitest` + `@testing-library/react` for components, Playwright for E2E (`.e2e.ts`)
- **Naming**: `PascalCase.tsx` for React components

### ML & AI
- **Model Assets**: Store prompts and model configs in `packages/ml/prompts/` with numbered prefixes
- **Data Models**: Use `pydantic` for schemas shared between API and ML layers

## Testing Standards

- **Backend**: `test_<module>.py` pattern, pytest fixtures
- **Frontend Components**: `.spec.tsx` files
- **E2E Tests**: `.e2e.ts` files using Playwright
- **Coverage Target**: Minimum 85% branch coverage
- **External Stubs**: Document all mocked services in `tests/stubs/README.md`

## Git Workflow & Commits

### Commit Convention
Follow Conventional Commits format:
- `feat:` - New features
- `fix:` - Bug fixes
- `chore:` - Maintenance tasks
- `docs:` - Documentation updates
- `test:` - Test additions or modifications

### Pull Request Requirements
Every PR must include:
1. **Problem Summary**: What issue does this solve?
2. **Implementation Notes**: Key technical decisions and approach
3. **Test Output**: Results of `make test` or specific test commands
4. **Issue Link**: `Closes #<issue-number>`
5. **Review**: At least one approval required
6. **UI Changes**: Include screenshots or screen recordings
7. **Architecture Changes**: Link updated ADRs in `docs/`
8. **Clean State**: Remove debug code, ensure CI passes

### Branching
- Rebase feature branches before opening PRs
- Keep commits focused and atomic
- Main branch: `main`

## Important Development Practices

### Data Handling
- Large datasets go in `data/raw/` with a README explaining provenance
- Only commit lightweight fixtures under `data/sample/`
- Never commit sensitive data (API keys, customer PII, credentials)

### Module Organization
- Shared business logic belongs in `packages/core/`
- Keep tests mirroring source structure under `tests/`
- Document architectural decisions in `docs/` as ADRs

### Code Style
- Backend: Use `dataclasses` and `pydantic` models for data structures
- Frontend: Functional components with hooks
- Both: Prefer explicit typing over `any` or dynamic types

## Common Development Workflows

### Adding a New AI Feature
1. Define prompts in `packages/ml/prompts/` with numbered prefix
2. Implement model logic in `packages/ml/`
3. Expose API endpoint in `apps/api/`
4. Create UI components in `apps/web/`
5. Add tests at each layer
6. Update relevant ADRs in `docs/`

### Integrating a New Marketing Channel
1. Add connector logic in `packages/core/integrations/`
2. Update API routes to support new channel
3. Add channel selection in web UI
4. Document API requirements and authentication
5. Add integration tests with stubbed responses

### Modifying Lead Scoring Algorithm
1. Update model in `packages/ml/`
2. Add/update test cases with expected scores
3. Document scoring criteria changes in ADR
4. Ensure backward compatibility or migration path
5. Run full test suite before PR

## External Integrations

The system integrates with multiple external services. All API clients should:
- Use environment variables for credentials
- Implement proper error handling and retries
- Log all external calls for debugging
- Provide stub/mock implementations for testing

Expected integration points include:
- Ad platforms (Google Ads, Meta, TikTok)
- Email/SMS services
- CRM/ERP systems
- E-commerce platforms

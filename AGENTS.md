# Repository Guidelines

## Project Structure & Module Organization
AntLeads is starting from a clean slate; please keep new work under a predictable tree. Use `apps/api/` for the marketing automation backend (FastAPI or similar), `apps/web/` for dashboards, `packages/core/` for shared domain logic, and `packages/ml/` for ranking or recommendation models. Mirror all tests under `tests/` using matching subdirectories. Store design notes and ADRs in `docs/`. Large datasets belong in `data/raw/` with a README describing provenance; check in only lightweight fixtures under `data/sample/`.

## Build, Test, and Development Commands
Add or update the root `Makefile` (or `package.json` scripts) so teammates can rely on scripted workflows:
- `make bootstrap` installs dependencies (Python via `uv`/`poetry`, frontend via `pnpm install`).
- `make api` launches the backend in reload mode.
- `make web` runs the client with mocked services.
- `make lint` runs all formatters and static analysis.
- `make test` executes unit and integration suites.
Every command must be idempotent and work inside a clean container.

## Coding Style & Naming Conventions
Target Python 3.11 and TypeScript 5. Use `ruff` + `black` (line length 100) for backend and `prettier` + `eslint` (Airbnb base) for frontend. Prefer dataclasses and pydantic models for shared schemas. Filenames use `snake_case.py` server-side and `PascalCase.tsx` for React components. Keep prompt or model assets in `packages/ml/prompts/` with numbered prefixes.

## Testing Guidelines
Adopt `pytest` with factory fixtures for the API and `vitest` + `testing-library` for the UI. Name backend tests `test_<module>.py`; use `.spec.tsx` for component tests and `.e2e.ts` for Playwright scenarios. Maintain ≥85% branch coverage (`make test -- --cov`). Record any external service stubs in `tests/stubs/README.md`.

## Commit & Pull Request Guidelines
Follow Conventional Commits (`feat:`, `fix:`, `chore:`). Keep commits focused and rebase before opening a PR. PRs must include a problem summary, implementation notes, test command output, and `Closes #issue`. Request at least one review, attach screenshots for UI changes, and link updated ADRs when architecture shifts. Remove debug assets and ensure CI is green before requesting merge.

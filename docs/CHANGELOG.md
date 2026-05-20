# Changelog

## 2026-05-20 — Initial MVP backend foundation

### Added

- FastAPI backend application.
- SQLite local database setup.
- SQLAlchemy database base and session handling.
- Core database models:
  - counties
  - products
  - farmers
  - buyers
  - farmer_supply
  - buyer_demand
  - tenders
  - matches
- Pydantic schemas for all core models.
- Service layer for creating, reading, and listing records.
- API routes for:
  - health
  - counties
  - products
  - farmers
  - buyers
  - farmer supply
  - buyer demand
  - tenders
  - matches
  - match generation
- Root API route at `/`.
- Health route at `/health`.
- Auto database initialization on API startup.
- Kenya counties seed data.
- MVP product seed data:
  - Maize
  - Beans
  - Potatoes
  - Tomatoes
  - Onions
- Demo data seed script for farmers, buyers, supply, and demand.
- Supply-demand match generation.
- Basic opportunity scoring.
- Basic shortage risk scoring.
- Streamlit dashboard shell.
- Environment example file.
- Requirements file.
- MVP run command documentation.

### Confirmed working

The following commands were confirmed working:

```bash
python -m scripts.init_db
python -m scripts.seed_base_data
python -m scripts.seed_demo_data
uvicorn app.main:app --reload

Confirmed output included:

Sarateal database initialized successfully.
Sarateal base data seeded successfully.
Sarateal demo data seeded successfully. Matches created: 2
Application startup complete.
Notes
The first GET / request originally returned 404 Not Found because no root route existed.
A root route was then added to app/api/health.py.
Tests are intentionally delayed until the MVP flow is stable.
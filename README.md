<p align="center">
  <img src="docs/assets/sarateal-logo.svg" alt="Sarateal logo" width="280" />
</p>

<p align="center">
  Farmer market access and food supply intelligence.
</p>

---

Sarateal is a **stateless, database-free** API for agricultural market
coordination. Reference data (counties, products, markets with published
coordinates) lives in memory; weather signals are fetched live from external
providers on demand. No Postgres, no SQLAlchemy — which keeps startup memory
well under 512 MB.

No demo, simulated, or imputed records are served. Per the STMOI methodology,
all observations (supply, demand, price) are recorded by real users in the
frontend's IndexedDB; the API serves reference data and live signals only.

## What the API serves

- `GET /health` — status and version
- `GET /counties` — Kenya county reference data, all 47 counties with published headquarters coordinates
- `GET /products` — market product reference data
- `GET /markets` — market names, counties, types, and coordinates
- `GET /weather/forecast` — Open-Meteo risk signals for a coordinate
- `GET /market-weather/forecast` — risk signals for a known market
- `GET /county-weather/forecast` — risk signals for a known county

Geocoding is intentionally **not** part of the API — the frontend resolves market
and place names directly against the public [Nominatim](https://nominatim.openstreetmap.org/)
API in the browser, so no coordinates are ever proxied or cached server-side.

The API is read-only by design. All application data is stored in the browser
via IndexedDB on the frontend.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For development/test tooling:

```bash
pip install -r requirements-dev.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run tests

```bash
pytest
```

## Deployment

For hosted environments (Render), use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

`render.yaml` expects only `APP_NAME` and `APP_VERSION` — no database connection
string is needed.

## Licensing note

The `dashboard/` directory is a legacy Streamlit app that depended on the
previous database layer. It is no longer wired into the API or the dependency
list, and it is not needed to run Sarateal.

## Data sources

Sarateal currently integrates with:

- [Open-Meteo](https://open-meteo.com/) for weather forecast data.
# Sarateal Deployment Notes

## Local production-style run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Render

Sarateal includes a `render.yaml` blueprint.

Expected Render settings:

```text
Runtime: Python
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

```text
APP_NAME=Sarateal
APP_VERSION=0.1.0
```

No database connection string is needed. Sarateal is stateless — reference data
and weather signals are fetched on demand, and all application data lives in the
browser (IndexedDB) on the frontend.

If a stale `DATABASE_URL` from an earlier database-backed version is still set in
Render, remove it: it points at an old tenant and is never read by the current
code, but keeping it invites confusion.

## Smoke-test after deployment

Check:

```text
GET /health
GET /counties
GET /products
GET /markets
GET /weather/forecast
GET /market-weather/forecast
GET /county-weather/forecast
```

Also open:

```text
/deploy-url/docs
```
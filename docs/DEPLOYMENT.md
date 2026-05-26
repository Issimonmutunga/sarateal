# Sarateal Deployment Notes

## Local production-style run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
````

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
DATABASE_URL=sqlite:///./sarateal.db
```

## Important database note

SQLite is acceptable for local testing and lightweight demos.

For persistent hosted deployment, switch to a hosted PostgreSQL database later and update:

```text
DATABASE_URL
```

## Pre-deployment checklist

```bash
pytest
git status
git add .
git commit -m "Prepare deployment docs"
git push
```

## Smoke-test after deployment

Check:

```text
GET /health
GET /markets
GET /prices
GET /weather/forecast
GET /market-weather/forecast
GET /county-weather/forecast
GET /geocoding/search
GET /stored-locations
```

Also open:

```text
/deploy-url/docs
```

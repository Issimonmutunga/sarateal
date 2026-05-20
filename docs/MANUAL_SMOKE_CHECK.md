# Manual Smoke Check

## Purpose

This document defines the first manual check for confirming that the Sarateal MVP is still working before formal tests are added.

Use this after major changes to models, services, routes, validation, dashboard forms, or seed scripts.

## 1. Activate environment

From the project root:

```bash
cd C:\Projects\supply\sarateal
````

Activate your virtual environment:

```bash
.teal\Scripts\activate
```

## 2. Install requirements

```bash
pip install -r requirements.txt
```

## 3. Initialize database

```bash
python -m scripts.init_db
```

Expected output:

```text
Sarateal database initialized successfully.
```

## 4. Seed base data

```bash
python -m scripts.seed_base_data
```

Expected output:

```text
Sarateal base data seeded successfully.
```

## 5. Seed demo data

```bash
python -m scripts.seed_demo_data
```

Expected output should be similar to:

```text
Sarateal demo data seeded successfully. New records: 0. Matches created: 0
```

or, on a clean database:

```text
Sarateal demo data seeded successfully. New records: 5. Matches created: 2
```

## 6. Run API

```bash
uvicorn app.main:app --reload
```

Expected output:

```text
Application startup complete.
```

Open:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "Sarateal API is running",
  "docs": "/docs",
  "health": "/health"
}
```

Open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "app": "Sarateal",
  "version": "0.1.0",
  "environment": "development"
}
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

## 7. Check core API routes

In the API docs, confirm these routes appear:

```text
/counties
/products
/farmers
/buyers
/farmer-supply
/buyer-demand
/tenders
/matches
/match-generation/supply-demand
```

## 8. Check route-order fixes

These routes must not be captured by ID routes:

```text
GET /farmer-supply/farmer/1
GET /buyer-demand/buyer/1
GET /tenders/county/Meru
GET /matches/supply/1
```

Expected behavior:

```text
They should return JSON lists, not validation errors saying the path value is not an integer.
```

## 9. Check duplicate validation

Try creating a farmer with an existing phone number:

```text
0700000001
```

Expected error code:

```text
DUPLICATE_RECORD
```

Try creating a buyer with an existing name:

```text
Demo Meru Aggregator
```

Expected error code:

```text
DUPLICATE_RECORD
```

## 10. Check business validation

Try creating farmer supply with:

```text
quantity = 0
```

Expected error code:

```text
BUSINESS_RULE_VIOLATION
```

Try creating buyer demand with:

```text
needed_until earlier than needed_from
```

Expected error code:

```text
BUSINESS_RULE_VIOLATION
```

Try creating a tender with:

```text
source_url = www.example.com
```

Expected error code:

```text
BUSINESS_RULE_VIOLATION
```

## 11. Run dashboard

Open a second terminal from the project root:

```bash
streamlit run dashboard/app.py
```

Expected dashboard sections:

```text
View data
Register farmer
Register buyer
Add supply
Add demand
Add tender
```

## 12. Dashboard checks

Confirm that:

```text
Metrics load without crashing.
Data tables display seeded data.
Generate supply-demand matches button works.
Duplicate farmer phone numbers show clean dashboard errors.
Duplicate buyer names show clean dashboard errors.
Supply and demand forms save valid records.
Tender form saves valid records.
```

## 13. Current expected MVP status

The MVP should now support:

```text
Base data seeding
Demo data seeding
API startup
API docs
Dashboard startup
Farmer registration
Buyer registration
Supply listing
Demand listing
Tender entry
Match generation
Central API error responses
Dashboard-friendly error display
```

## 14. When this passes

Once this manual smoke check passes, the next development step is to add formal tests.

Recommended first test files:

```text
tests/test_health.py
tests/test_scoring.py
tests/test_validation.py
tests/test_match_generation.py
```

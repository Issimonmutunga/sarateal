<p align="center">
  <img src="docs/assets/sarateal-icon.svg" alt="Sarateal icon" width="96" />
</p>

<h1 align="center">Sarateal</h1>

<p align="center">
  Lightweight open-source farmer market access and food supply intelligence.
</p>

---

Sarateal connects supply, demand, prices, tenders, weather signals, and location intelligence into a simple API-first system for agricultural market coordination.

## Features

- Farmer supply and buyer demand records
- Market, product, county, tender, and match workflows
- Price records and CSV price ingestion
- Supply-demand match generation
- Weather-risk signals from forecast data
- Market and county weather lookup
- Geocoding through Nominatim/OpenStreetMap
- Cached and verified location coordinates
- FastAPI backend with tested service layers

## Installation

```bash
git clone https://github.com/<your-org-or-user>/sarateal.git
cd sarateal
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
````

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

## Example endpoints

```text
GET /health
GET /markets
GET /prices
POST /price-ingestion/csv
GET /weather/forecast
GET /market-weather/forecast
GET /county-weather/forecast
GET /geocoding/search
GET /stored-locations
PATCH /stored-locations/{stored_location_id}/verification
```

## Data sources

Sarateal currently integrates with:

* [Open-Meteo](https://open-meteo.com/) for weather forecast data.
* [Nominatim/OpenStreetMap](https://operations.osmfoundation.org/policies/nominatim/) for geocoding, used through a cache-aware adapter with a custom User-Agent.

## Development

The project uses small, tested service and API layers.

```bash
pytest
```

## License

Add a license before public release. MIT or Apache-2.0 are common choices for open-source Python projects.


Run:

```bash
pytest
````

Commit only after tests pass:

```text
Update README with Sarateal icon
```

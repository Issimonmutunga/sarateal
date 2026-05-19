# Sarateal — Kenya Farmer Market Access Radar

## Project path
C:\Projects\supply\sarateal

## Working rule
Responses should be short: maximum 3 points per response, or 1 code file + 1 short one-line commit message.

## Product idea
Sarateal is a lightweight Kenya-wide farmer market access system. It helps real farmers, cooperatives, and vulnerable suppliers find direct market opportunities such as tenders, institutional buyers, food distributors, NGOs, school-feeding programs, hospitals, retailers, aggregators, millers, and county procurement channels.

## Core purpose
The system connects farmer supply to buyer demand while also tracking food-security risk, price movement, supply shortages, climate stress, road/logistics disruption, and tender opportunities.

## Target users
- Farmers and farmer groups
- Cooperatives
- Aggregators
- NGOs and donor programs
- County governments
- Institutional buyers
- Food distributors, millers, and retailers

## Geographic scope
Kenya-wide coverage, structured as:

Country → County → Sub-county → Ward → Market / Farmer cluster / Buyer node

Start with all 47 counties, but keep computation light by working mainly at market, ward, county, and farmer-cluster level.

## MVP commodities
Start with 3–5 high-demand products:
- Maize
- Beans
- Potatoes
- Tomatoes
- Onions

## Main system modules
- Farmer registration
- Buyer registration
- Product supply listing
- Demand/opportunity listing
- Tender/opportunity board
- Market price tracking
- Climate and crop stress signals
- Supply shortage risk scoring
- Buyer-farmer matching
- Delivery cost and route estimate
- Supplier readiness checklist
- Data freshness dashboard

## Core MVP workflow
Farmer registers supply → system reads buyer demand/tenders → matches by product, location, volume, timing, and requirements → estimates margin → flags risks → recommends best opportunities.

## Lightweight architecture
Use a simple modular Python backend first:

- FastAPI for API
- PostgreSQL/PostGIS or DuckDB for data
- Scheduled Python jobs for data pulls
- Streamlit first for dashboard, React later if needed
- GeoParquet/CSV for lightweight spatial and tabular data
- PMTiles later for fast maps

## Suggested folder structure
app/
- api/
- core/
- db/
- models/
- schemas/
- services/
- jobs/
- scoring/
- data_sources/

dashboard/
data/
- raw/
- processed/
- geo/

outputs/
notebooks/
tests/
docs/
scripts/

## Data sources
Use open and low-cost sources first:
- Kenya tenders: tenders.go.ke / e-GP / PPIP where available
- Food prices: WFP VAM, HDX, FEWS NET, local market reports
- Food security: FEWS NET, FAO GIEWS, IPC/CH where available
- Admin boundaries: Kenya counties, sub-counties, wards
- Roads and markets: OpenStreetMap
- Climate: CHIRPS rainfall, ERA5/ERA5-Land, seasonal forecasts
- Crop stress: Sentinel-2 NDVI, MODIS NDVI
- Local verification: farmer reports, cooperative uploads, trader reports, buyer confirmations

## Refresh frequency
- Tenders: daily or weekly
- Prices: weekly where available
- Rainfall: daily or weekly aggregation
- Vegetation: 5–16 days depending on source
- Road/news disruption: daily if available
- Farmer/buyer listings: live user updates
- Risk score: nightly recomputation

## Core database tables
- farmers
- farmer_groups
- buyers
- markets
- products
- farmer_supply
- buyer_demand
- tenders
- prices
- climate_signals
- route_signals
- risk_scores
- matches
- readiness_checks

## First scoring logic
Keep scoring simple before ML:

Opportunity score =
product match + location proximity + volume fit + timing fit + buyer reliability + farmer readiness - transport cost - climate/logistics risk

Shortage risk =
price spike + rainfall anomaly + crop stress + road disruption + low supply reports

## Farmer-facing features
- See nearby buyers
- See active tenders/opportunities
- Add expected harvest
- Estimate likely margin
- Check requirements
- See best market to target
- Get shortage/demand alerts
- Join cooperative or cluster opportunity

## Buyer-facing features
- Find suppliers by product and county
- See farmer clusters
- Check supply reliability
- Track climate/logistics risk
- Verify local sourcing
- Generate supplier shortlist

## Business model
Charge buyers, NGOs, counties, donors, and agribusinesses, not small farmers at first.

Possible pricing:
- Free farmer registration
- Paid buyer dashboard
- Paid tender/opportunity intelligence
- Paid county/NGO dashboards
- Paid API access
- Setup fee for custom region/program
- Verification fee for supplier onboarding

## MVP rule
Do not overbuild. Start with:
- Kenya counties
- 3–5 commodities
- Manual/semi-automated tender input
- Weekly price updates
- Farmer supply registration
- Buyer demand registration
- Simple matching
- Simple risk scoring
- Streamlit dashboard

## Development style
One file at a time.
Each response should include:
- Exact file path
- Full file content
- One short one-line commit message

## Commit style
Use short one-line commits only.

Example:
Add base project scaffold
Add farmer registration schema
Add buyer demand model
Add opportunity scoring logic
Add Kenya county seed data
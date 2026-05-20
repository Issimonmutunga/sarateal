# Sarateal MVP Run Commands

Run these from the project root:

```bash
cd C:\Projects\supply\sarateal
1. Initialize database
python scripts/init_db.py
2. Seed base data
python scripts/seed_base_data.py
3. Seed demo data
python scripts/seed_demo_data.py
4. Run API
uvicorn app.main:app --reload

API docs:

http://127.0.0.1:8000/docs
5. Run dashboard

Open a second terminal:

streamlit run dashboard/app.py

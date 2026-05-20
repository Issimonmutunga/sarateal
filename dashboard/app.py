import pandas as pd
import streamlit as st

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.buyer import Buyer
from app.models.buyer_demand import BuyerDemand
from app.models.farmer import Farmer
from app.models.farmer_supply import FarmerSupply
from app.models.match import Match
from app.models.tender import Tender


st.set_page_config(
    page_title="Sarateal",
    page_icon="🌱",
    layout="wide",
)


def count_rows(db, model) -> int:
    return db.query(model).count()


def load_table(db, model) -> pd.DataFrame:
    rows = db.query(model).all()

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(
        [
            {
                column.name: getattr(row, column.name)
                for column in model.__table__.columns
            }
            for row in rows
        ]
    )


def main() -> None:
    init_db()
    db = SessionLocal()

    try:
        st.title("Sarateal")
        st.caption("Kenya farmer market access radar")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Farmers", count_rows(db, Farmer))
        col2.metric("Buyers", count_rows(db, Buyer))
        col3.metric("Supply listings", count_rows(db, FarmerSupply))
        col4.metric("Demand listings", count_rows(db, BuyerDemand))

        col5, col6 = st.columns(2)
        col5.metric("Tenders", count_rows(db, Tender))
        col6.metric("Suggested matches", count_rows(db, Match))

        st.divider()

        section = st.selectbox(
            "View data",
            [
                "Farmers",
                "Buyers",
                "Farmer supply",
                "Buyer demand",
                "Tenders",
                "Matches",
            ],
        )

        model_map = {
            "Farmers": Farmer,
            "Buyers": Buyer,
            "Farmer supply": FarmerSupply,
            "Buyer demand": BuyerDemand,
            "Tenders": Tender,
            "Matches": Match,
        }

        df = load_table(db, model_map[section])

        if df.empty:
            st.info(f"No {section.lower()} records yet.")
        else:
            st.dataframe(df, use_container_width=True)

    finally:
        db.close()


if __name__ == "__main__":
    main()
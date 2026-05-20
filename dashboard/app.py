from datetime import date
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if "app" in sys.modules:
    loaded_app = sys.modules["app"]
    loaded_app_file = getattr(loaded_app, "__file__", "")

    if loaded_app_file and Path(loaded_app_file).resolve() == Path(__file__).resolve():
        del sys.modules["app"]

import pandas as pd
import streamlit as st

from app.core.exceptions import SaratealError
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.buyer import Buyer
from app.models.buyer_demand import BuyerDemand
from app.models.farmer import Farmer
from app.models.farmer_supply import FarmerSupply
from app.models.match import Match
from app.models.product import Product
from app.models.tender import Tender
from app.schemas.buyer import BuyerCreate
from app.schemas.buyer_demand import BuyerDemandCreate
from app.schemas.farmer import FarmerCreate
from app.schemas.farmer_supply import FarmerSupplyCreate
from app.schemas.tender import TenderCreate
from app.services.buyers import create_buyer
from app.services.buyer_demand import create_buyer_demand
from app.services.farmers import create_farmer
from app.services.farmer_supply import create_farmer_supply
from app.services.match_generation import generate_supply_demand_matches
from app.services.tenders import create_tender


st.set_page_config(
    page_title="Sarateal",
    page_icon="🌱",
    layout="wide",
)


def show_error(error: Exception) -> None:
    if isinstance(error, SaratealError):
        st.error(error.message)

        for detail in error.details:
            field = detail.field or "general"
            value_text = f" Value: {detail.value}" if detail.value is not None else ""
            st.warning(f"{field}: {detail.message}{value_text}")

        if error.context:
            with st.expander("Error context"):
                st.json(error.context)

        return

    st.error("An unexpected error occurred.")
    with st.expander("Technical detail"):
        st.write(error.__class__.__name__)
        st.write(str(error))


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


def get_product_options(db) -> dict[str, int]:
    products = db.query(Product).order_by(Product.name).all()
    return {product.name: product.id for product in products}


def get_farmer_options(db) -> dict[str, int]:
    farmers = db.query(Farmer).order_by(Farmer.full_name).all()
    return {f"{farmer.full_name} — {farmer.county}": farmer.id for farmer in farmers}


def get_buyer_options(db) -> dict[str, int]:
    buyers = db.query(Buyer).order_by(Buyer.name).all()
    return {f"{buyer.name} — {buyer.county}": buyer.id for buyer in buyers}


def render_farmer_form(db) -> None:
    st.subheader("Register farmer")

    with st.form("farmer_form"):
        full_name = st.text_input("Full name")
        phone_number = st.text_input("Phone number")
        county = st.text_input("County")
        sub_county = st.text_input("Sub-county")
        ward = st.text_input("Ward")
        farmer_group = st.text_input("Farmer group")
        is_verified = st.checkbox("Verified farmer")

        submitted = st.form_submit_button("Save farmer")

        if submitted:
            if not full_name or not phone_number or not county:
                st.error("Full name, phone number, and county are required.")
                return

            try:
                farmer_in = FarmerCreate(
                    full_name=full_name,
                    phone_number=phone_number,
                    county=county,
                    sub_county=sub_county or None,
                    ward=ward or None,
                    farmer_group=farmer_group or None,
                    is_verified=is_verified,
                )

                create_farmer(db=db, farmer_in=farmer_in)
                st.success("Farmer registered successfully.")
            except Exception as error:
                show_error(error)


def render_buyer_form(db) -> None:
    st.subheader("Register buyer")

    with st.form("buyer_form"):
        name = st.text_input("Buyer name")
        buyer_type = st.selectbox(
            "Buyer type",
            [
                "institution",
                "aggregator",
                "ngo",
                "county government",
                "retailer",
                "miller",
                "distributor",
                "other",
            ],
        )
        contact_person = st.text_input("Contact person")
        phone_number = st.text_input("Phone number")
        email = st.text_input("Email")
        county = st.text_input("County")
        sub_county = st.text_input("Sub-county")
        ward = st.text_input("Ward")
        is_verified = st.checkbox("Verified buyer")

        submitted = st.form_submit_button("Save buyer")

        if submitted:
            if not name or not buyer_type or not county:
                st.error("Buyer name, buyer type, and county are required.")
                return

            try:
                buyer_in = BuyerCreate(
                    name=name,
                    buyer_type=buyer_type,
                    contact_person=contact_person or None,
                    phone_number=phone_number or None,
                    email=email or None,
                    county=county,
                    sub_county=sub_county or None,
                    ward=ward or None,
                    is_verified=is_verified,
                )

                create_buyer(db=db, buyer_in=buyer_in)
                st.success("Buyer registered successfully.")
            except Exception as error:
                show_error(error)


def render_supply_form(db) -> None:
    st.subheader("Add farmer supply")

    farmer_options = get_farmer_options(db)
    product_options = get_product_options(db)

    if not farmer_options or not product_options:
        st.warning("Add farmers and seed products before creating supply listings.")
        return

    with st.form("supply_form"):
        farmer_label = st.selectbox("Farmer", list(farmer_options.keys()))
        product_label = st.selectbox("Product", list(product_options.keys()))

        quantity = st.number_input("Quantity", min_value=0.0, step=100.0)
        unit = st.text_input("Unit", value="kg")

        available_from = st.date_input("Available from", value=date.today())
        available_until = st.date_input("Available until", value=date.today())

        county = st.text_input("County")
        sub_county = st.text_input("Sub-county")
        ward = st.text_input("Ward")
        expected_price_per_unit = st.number_input(
            "Expected price per unit",
            min_value=0.0,
            step=1.0,
        )

        submitted = st.form_submit_button("Save supply listing")

        if submitted:
            if quantity <= 0 or not county:
                st.error("Quantity and county are required.")
                return

            try:
                supply_in = FarmerSupplyCreate(
                    farmer_id=farmer_options[farmer_label],
                    product_id=product_options[product_label],
                    quantity=quantity,
                    unit=unit,
                    available_from=available_from,
                    available_until=available_until,
                    county=county,
                    sub_county=sub_county or None,
                    ward=ward or None,
                    expected_price_per_unit=expected_price_per_unit or None,
                )

                create_farmer_supply(db=db, supply_in=supply_in)
                st.success("Supply listing created successfully.")
            except Exception as error:
                show_error(error)


def render_demand_form(db) -> None:
    st.subheader("Add buyer demand")

    buyer_options = get_buyer_options(db)
    product_options = get_product_options(db)

    if not buyer_options or not product_options:
        st.warning("Add buyers and seed products before creating demand listings.")
        return

    with st.form("demand_form"):
        buyer_label = st.selectbox("Buyer", list(buyer_options.keys()))
        product_label = st.selectbox("Product", list(product_options.keys()))

        quantity_needed = st.number_input("Quantity needed", min_value=0.0, step=100.0)
        unit = st.text_input("Unit", value="kg")

        needed_from = st.date_input("Needed from", value=date.today())
        needed_until = st.date_input("Needed until", value=date.today())

        county = st.text_input("County")
        sub_county = st.text_input("Sub-county")
        ward = st.text_input("Ward")
        target_price_per_unit = st.number_input(
            "Target price per unit",
            min_value=0.0,
            step=1.0,
        )
        requirements = st.text_area("Requirements")

        submitted = st.form_submit_button("Save demand listing")

        if submitted:
            if quantity_needed <= 0 or not county:
                st.error("Quantity needed and county are required.")
                return

            try:
                demand_in = BuyerDemandCreate(
                    buyer_id=buyer_options[buyer_label],
                    product_id=product_options[product_label],
                    quantity_needed=quantity_needed,
                    unit=unit,
                    needed_from=needed_from,
                    needed_until=needed_until,
                    county=county,
                    sub_county=sub_county or None,
                    ward=ward or None,
                    target_price_per_unit=target_price_per_unit or None,
                    requirements=requirements or None,
                )

                create_buyer_demand(db=db, demand_in=demand_in)
                st.success("Demand listing created successfully.")
            except Exception as error:
                show_error(error)


def render_tender_form(db) -> None:
    st.subheader("Add tender or opportunity")

    buyer_options = {"None": None} | get_buyer_options(db)
    product_options = {"None": None} | get_product_options(db)

    with st.form("tender_form"):
        title = st.text_input("Tender title")
        buyer_label = st.selectbox("Linked buyer", list(buyer_options.keys()))
        product_label = st.selectbox("Linked product", list(product_options.keys()))

        source_name = st.text_input("Source name", value="Manual entry")
        source_url = st.text_input("Source URL")

        county = st.text_input("County")
        quantity = st.number_input("Quantity", min_value=0.0, step=100.0)
        unit = st.text_input("Unit", value="kg")

        opening_date = st.date_input("Opening date", value=date.today())
        closing_date = st.date_input("Closing date", value=date.today())

        requirements = st.text_area("Requirements")

        submitted = st.form_submit_button("Save tender")

        if submitted:
            if not title or not source_name:
                st.error("Tender title and source name are required.")
                return

            try:
                tender_in = TenderCreate(
                    title=title,
                    buyer_id=buyer_options[buyer_label],
                    product_id=product_options[product_label],
                    source_name=source_name,
                    source_url=source_url or None,
                    county=county or None,
                    quantity=quantity or None,
                    unit=unit or None,
                    opening_date=opening_date,
                    closing_date=closing_date,
                    requirements=requirements or None,
                )

                create_tender(db=db, tender_in=tender_in)
                st.success("Tender saved successfully.")
            except Exception as error:
                show_error(error)


def render_data_view(db) -> None:
    section = st.selectbox(
        "View data",
        [
            "Farmers",
            "Buyers",
            "Products",
            "Farmer supply",
            "Buyer demand",
            "Tenders",
            "Matches",
        ],
    )

    model_map = {
        "Farmers": Farmer,
        "Buyers": Buyer,
        "Products": Product,
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


def main() -> None:
    init_db()
    db = SessionLocal()

    try:
        st.title("Sarateal")
        st.caption("Kenya farmer market access radar")

        if st.button("Generate supply-demand matches"):
            try:
                matches = generate_supply_demand_matches(db=db)
                st.success(f"Generated {len(matches)} new match records.")
            except Exception as error:
                show_error(error)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Farmers", count_rows(db, Farmer))
        col2.metric("Buyers", count_rows(db, Buyer))
        col3.metric("Supply listings", count_rows(db, FarmerSupply))
        col4.metric("Demand listings", count_rows(db, BuyerDemand))

        col5, col6, col7 = st.columns(3)
        col5.metric("Tenders", count_rows(db, Tender))
        col6.metric("Suggested matches", count_rows(db, Match))
        col7.metric("Products", count_rows(db, Product))

        st.divider()

        tabs = st.tabs(
            [
                "View data",
                "Register farmer",
                "Register buyer",
                "Add supply",
                "Add demand",
                "Add tender",
            ]
        )

        with tabs[0]:
            render_data_view(db)

        with tabs[1]:
            render_farmer_form(db)

        with tabs[2]:
            render_buyer_form(db)

        with tabs[3]:
            render_supply_form(db)

        with tabs[4]:
            render_demand_form(db)

        with tabs[5]:
            render_tender_form(db)

    finally:
        db.close()


if __name__ == "__main__":
    main()
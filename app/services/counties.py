from sqlalchemy.orm import Session

from app.models.county import County
from app.schemas.county import CountyCreate


def create_county(db: Session, county_in: CountyCreate) -> County:
    county = County(**county_in.model_dump())

    db.add(county)
    db.commit()
    db.refresh(county)

    return county


def list_counties(db: Session) -> list[County]:
    return db.query(County).order_by(County.name).all()


def get_county(db: Session, county_id: int) -> County | None:
    return db.query(County).filter(County.id == county_id).first()


def get_county_by_name(db: Session, name: str) -> County | None:
    return db.query(County).filter(County.name == name).first()
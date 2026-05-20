from sqlalchemy.orm import Session

from app.core.exceptions import duplicate_record_error, record_not_found_error
from app.models.county import County
from app.schemas.county import CountyCreate


def create_county(db: Session, county_in: CountyCreate) -> County:
    existing_code = get_county_by_code(
        db=db,
        code=county_in.code,
    )

    if existing_code:
        raise duplicate_record_error(
            entity="County",
            field="code",
            value=county_in.code,
        )

    existing_name = get_county_by_name(
        db=db,
        name=county_in.name,
    )

    if existing_name:
        raise duplicate_record_error(
            entity="County",
            field="name",
            value=county_in.name,
        )

    county = County(**county_in.model_dump())

    db.add(county)
    db.commit()
    db.refresh(county)

    return county


def list_counties(db: Session) -> list[County]:
    return db.query(County).order_by(County.name).all()


def get_county(db: Session, county_id: int) -> County | None:
    return db.query(County).filter(County.id == county_id).first()


def get_county_or_raise(db: Session, county_id: int) -> County:
    county = get_county(db=db, county_id=county_id)

    if not county:
        raise record_not_found_error(
            entity="County",
            identifier=county_id,
        )

    return county


def get_county_by_name(db: Session, name: str) -> County | None:
    return db.query(County).filter(County.name == name).first()


def get_county_by_code(db: Session, code: str) -> County | None:
    return db.query(County).filter(County.code == code).first()
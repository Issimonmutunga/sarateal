import pytest

from app.core.exceptions import BusinessRuleViolationError
from app.schemas.match import MatchCreate
from app.services.matches import create_match


def test_create_match_rejects_missing_buyer_demand_and_tender_reference(db_session):
    with pytest.raises(BusinessRuleViolationError):
        create_match(
            db=db_session,
            match_in=MatchCreate(
                farmer_supply_id=1,
                buyer_demand_id=None,
                tender_id=None,
                opportunity_score=50,
                estimated_transport_cost=100,
            ),
        )


def test_create_match_rejects_both_buyer_demand_and_tender_reference(db_session):
    with pytest.raises(BusinessRuleViolationError):
        create_match(
            db=db_session,
            match_in=MatchCreate(
                farmer_supply_id=1,
                buyer_demand_id=1,
                tender_id=1,
                opportunity_score=50,
                estimated_transport_cost=100,
            ),
        )


def test_create_match_rejects_negative_transport_cost(db_session):
    with pytest.raises(BusinessRuleViolationError):
        create_match(
            db=db_session,
            match_in=MatchCreate(
                farmer_supply_id=1,
                buyer_demand_id=1,
                tender_id=None,
                opportunity_score=50,
                estimated_transport_cost=-1,
            ),
        )


def test_create_match_rejects_opportunity_score_below_zero(db_session):
    with pytest.raises(BusinessRuleViolationError):
        create_match(
            db=db_session,
            match_in=MatchCreate(
                farmer_supply_id=1,
                buyer_demand_id=1,
                tender_id=None,
                opportunity_score=-1,
                estimated_transport_cost=100,
            ),
        )


def test_create_match_rejects_opportunity_score_above_one_hundred(db_session):
    with pytest.raises(BusinessRuleViolationError):
        create_match(
            db=db_session,
            match_in=MatchCreate(
                farmer_supply_id=1,
                buyer_demand_id=1,
                tender_id=None,
                opportunity_score=101,
                estimated_transport_cost=100,
            ),
        )
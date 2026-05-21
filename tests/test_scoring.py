from app.scoring.opportunity import (
    OpportunityScoreInput,
    calculate_opportunity_score,
    classify_opportunity,
)


def test_opportunity_score_is_clamped_to_zero():
    score = calculate_opportunity_score(
        OpportunityScoreInput(
            product_match=False,
            same_county=False,
            volume_fit_ratio=-10,
            timing_fit=False,
            buyer_verified=False,
            farmer_verified=False,
            transport_risk=100,
            climate_risk=100,
        )
    )

    assert score == 0.0


def test_opportunity_score_is_clamped_to_one_hundred():
    score = calculate_opportunity_score(
        OpportunityScoreInput(
            product_match=True,
            same_county=True,
            volume_fit_ratio=10,
            timing_fit=True,
            buyer_verified=True,
            farmer_verified=True,
            transport_risk=-100,
            climate_risk=-100,
        )
    )

    assert score == 100.0


def test_opportunity_score_returns_value_between_zero_and_one_hundred():
    score = calculate_opportunity_score(
        OpportunityScoreInput(
            product_match=True,
            same_county=False,
            volume_fit_ratio=0.5,
            timing_fit=True,
            buyer_verified=False,
            farmer_verified=True,
            transport_risk=0.2,
            climate_risk=0.2,
        )
    )

    assert 0.0 <= score <= 100.0


def test_opportunity_classification_bands():
    assert classify_opportunity(80) == "strong"
    assert classify_opportunity(60) == "medium"
    assert classify_opportunity(30) == "weak"
    assert classify_opportunity(10) == "poor"
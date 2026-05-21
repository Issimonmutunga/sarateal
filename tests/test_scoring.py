from app.scoring.opportunity import (
    classify_opportunity_score,
    calculate_opportunity_score,
)
from app.scoring.shortage import (
    classify_shortage_score,
    calculate_shortage_score,
)


def test_opportunity_score_is_clamped_to_zero_and_one_hundred():
    low_score = calculate_opportunity_score(
        product_match=False,
        same_county=False,
        volume_fit_ratio=-10,
        timing_fit=False,
        buyer_verified=False,
        farmer_verified=False,
        transport_risk=100,
        climate_risk=100,
    )

    high_score = calculate_opportunity_score(
        product_match=True,
        same_county=True,
        volume_fit_ratio=10,
        timing_fit=True,
        buyer_verified=True,
        farmer_verified=True,
        transport_risk=-100,
        climate_risk=-100,
    )

    assert low_score == 0
    assert high_score == 100


def test_opportunity_score_classification_bands():
    assert classify_opportunity_score(80) == "strong"
    assert classify_opportunity_score(60) == "medium"
    assert classify_opportunity_score(30) == "weak"
    assert classify_opportunity_score(10) == "poor"


def test_shortage_score_is_clamped_to_zero_and_one_hundred():
    low_score = calculate_shortage_score(
        price_spike_ratio=-10,
        rainfall_deficit_ratio=-10,
        crop_stress_ratio=-10,
        road_disruption_ratio=-10,
        low_supply_report_ratio=-10,
    )

    high_score = calculate_shortage_score(
        price_spike_ratio=10,
        rainfall_deficit_ratio=10,
        crop_stress_ratio=10,
        road_disruption_ratio=10,
        low_supply_report_ratio=10,
    )

    assert low_score == 0
    assert high_score == 100


def test_shortage_score_classification_bands():
    assert classify_shortage_score(80) == "critical"
    assert classify_shortage_score(60) == "high"
    assert classify_shortage_score(30) == "medium"
    assert classify_shortage_score(10) == "low"
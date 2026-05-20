from dataclasses import dataclass


@dataclass(frozen=True)
class ShortageRiskInput:
    price_spike_ratio: float = 0.0
    rainfall_deficit_ratio: float = 0.0
    crop_stress_ratio: float = 0.0
    road_disruption_ratio: float = 0.0
    low_supply_report_ratio: float = 0.0


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, value))


def calculate_shortage_risk(score_input: ShortageRiskInput) -> float:
    score = 0.0

    score += score_input.price_spike_ratio * 25.0
    score += score_input.rainfall_deficit_ratio * 25.0
    score += score_input.crop_stress_ratio * 20.0
    score += score_input.road_disruption_ratio * 15.0
    score += score_input.low_supply_report_ratio * 15.0

    return round(clamp_score(score), 2)


def classify_shortage_risk(score: float) -> str:
    if score >= 75:
        return "critical"

    if score >= 50:
        return "high"

    if score >= 25:
        return "medium"

    return "low"
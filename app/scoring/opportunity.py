from dataclasses import dataclass


@dataclass(frozen=True)
class OpportunityScoreInput:
    product_match: bool
    same_county: bool
    volume_fit_ratio: float
    timing_fit: bool
    buyer_verified: bool = False
    farmer_verified: bool = False
    transport_risk: float = 0.0
    climate_risk: float = 0.0


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, value))


def calculate_opportunity_score(score_input: OpportunityScoreInput) -> float:
    score = 0.0

    if score_input.product_match:
        score += 30.0

    if score_input.same_county:
        score += 20.0

    score += min(score_input.volume_fit_ratio, 1.0) * 20.0

    if score_input.timing_fit:
        score += 15.0

    if score_input.buyer_verified:
        score += 7.5

    if score_input.farmer_verified:
        score += 7.5

    score -= score_input.transport_risk * 10.0
    score -= score_input.climate_risk * 10.0

    return round(clamp_score(score), 2)


def classify_opportunity(score: float) -> str:
    if score >= 75:
        return "strong"

    if score >= 50:
        return "medium"

    if score >= 25:
        return "weak"

    return "poor"
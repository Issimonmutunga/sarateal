from app.models.buyer import Buyer
from app.models.buyer_demand import BuyerDemand
from app.models.farmer import Farmer
from app.models.farmer_supply import FarmerSupply
from app.scoring import OpportunityScoreInput, calculate_opportunity_score, classify_opportunity


def calculate_volume_fit_ratio(
    supply_quantity: float,
    demand_quantity: float,
) -> float:
    if demand_quantity <= 0:
        return 0.0

    return min(supply_quantity / demand_quantity, 1.0)


def has_timing_overlap(
    supply: FarmerSupply,
    demand: BuyerDemand,
) -> bool:
    supply_end = supply.available_until or supply.available_from
    demand_end = demand.needed_until or demand.needed_from

    return supply.available_from <= demand_end and demand.needed_from <= supply_end


def score_supply_against_demand(
    supply: FarmerSupply,
    demand: BuyerDemand,
    farmer: Farmer | None = None,
    buyer: Buyer | None = None,
) -> tuple[float, str]:
    score_input = OpportunityScoreInput(
        product_match=supply.product_id == demand.product_id,
        same_county=supply.county.lower() == demand.county.lower(),
        volume_fit_ratio=calculate_volume_fit_ratio(
            supply_quantity=supply.quantity,
            demand_quantity=demand.quantity_needed,
        ),
        timing_fit=has_timing_overlap(supply=supply, demand=demand),
        buyer_verified=buyer.is_verified if buyer else False,
        farmer_verified=farmer.is_verified if farmer else False,
    )

    score = calculate_opportunity_score(score_input)
    label = classify_opportunity(score)

    return score, label
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MatchBase(BaseModel):
    farmer_supply_id: int

    buyer_demand_id: int | None = None
    tender_id: int | None = None

    opportunity_score: float = 0.0
    estimated_transport_cost: float | None = None
    estimated_margin: float | None = None

    risk_level: str = "unknown"
    recommendation: str | None = None

    status: str = "suggested"


class MatchCreate(MatchBase):
    pass


class MatchRead(MatchBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
from app.dataset import get_market, list_markets


def list_markets_service() -> list:
    return list_markets()


def get_market_service(market_id: int):
    return get_market(market_id)
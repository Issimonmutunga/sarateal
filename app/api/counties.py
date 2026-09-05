from fastapi import APIRouter

from app.services.counties import list_counties_service

router = APIRouter(prefix="/counties", tags=["Counties"])


@router.get("/")
def list_counties_endpoint():
    return list_counties_service()
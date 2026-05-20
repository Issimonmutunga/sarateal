from fastapi import APIRouter

from app.core.config import get_settings


router = APIRouter(tags=["Health"])


@router.get("/")
def root() -> dict[str, str]:
    settings = get_settings()

    return {
        "message": f"{settings.app_name} API is running",
        "docs": "/docs",
        "health": "/health",
    }


@router.get("/health")
def health_check() -> dict[str, str]:
    settings = get_settings()

    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
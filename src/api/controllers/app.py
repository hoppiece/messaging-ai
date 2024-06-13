from api import models
from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", response_model=models.HealthCheckResponse)
async def get_health() -> models.HealthCheckResponse:
    return models.HealthCheckResponse()

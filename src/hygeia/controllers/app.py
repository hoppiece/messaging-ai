from fastapi import APIRouter
from hygeia import models

router = APIRouter()


@router.get("/healthz", response_model=models.HealthCheckResponse)
async def get_health() -> models.HealthCheckResponse:
    return models.HealthCheckResponse()

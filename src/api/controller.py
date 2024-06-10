from fastapi import APIRouter

from api import models

router = APIRouter()


@router.get("/healthz", response_model=models.HealthCheckResponse)
def get_health() -> models.HealthCheckResponse:
    return models.HealthCheckResponse()

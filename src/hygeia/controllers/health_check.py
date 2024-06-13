from fastapi import APIRouter
from hygeia.models import HealthCheckResponse

router = APIRouter()


@router.get("/healthz", response_model=HealthCheckResponse)
def get_health() -> HealthCheckResponse:
    return HealthCheckResponse()

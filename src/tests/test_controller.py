from api.models import HealthCheckResponse
from fastapi.testclient import TestClient


def test_get_health(client: TestClient) -> None:
    expected_response = HealthCheckResponse()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == expected_response.model_dump()

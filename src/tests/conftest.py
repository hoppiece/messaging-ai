from typing import Generator

import pytest
from api.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from hygeia.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client

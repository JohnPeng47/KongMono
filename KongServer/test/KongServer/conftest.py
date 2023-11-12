from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.server.routes.graph.route import router as graph_route

import pytest

@pytest.fixture
def test_app_client():
    app = FastAPI()

    # Include your router here
    app.include_router(graph_route)

    with TestClient(app) as client:
        yield client
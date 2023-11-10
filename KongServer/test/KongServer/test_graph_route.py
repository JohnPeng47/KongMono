import pytest
from fastapi import FastAPI, status
from starlette.testclient import TestClient
from unittest.mock import MagicMock, patch

from src.server.routes.auth.service import get_user_from_token
from src.server.routes.graph.service import get_graph

# Assuming your FastAPI app is named 'app' and you have the above routes added to it
# and assuming you have defined 'get_user_from_token' and 'get_graph' dependency functions

# Mock dependencies
@pytest.fixture
def mock_get_user_from_token():
    return MagicMock(return_value={"user_id": "test_user"})

@pytest.fixture
def mock_get_graph():
    mock_graph = MagicMock()
    mock_graph.to_json_frontend.return_value = '{}'
    return mock_graph

@pytest.fixture
def test_app_client(mock_get_user_from_token, mock_get_graph):
    app = FastAPI()

    # Include your router here
    # app.include_router(your_router)

    # Dependency overrides
    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token
    app.dependency_overrides[get_graph] = mock_get_graph

    with TestClient(app) as client:
        yield client

# Test for getting graph metadata
def test_get_graph_metadata_route_success(test_app_client):
    response = test_app_client.get("/metadata/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)  # Should return a list

def test_get_graph_route_success(test_app_client, mock_get_graph):
    graph_id = "test_graph_id"
    response = test_app_client.get(f"/graph/{graph_id}")
    assert response.status_code == status.HTTP_200_OK
    # Confirm that we're returning JSON, mock_get_graph's to_json_frontend returns '{}'
    assert response.json() == {}

# Test for deletion of a graph
def test_delete_graph_route_success(test_app_client):
    graph_id = "test_graph_id"
    with patch('path.to.your.delete_graph_db') as mock_delete_graph_db, \
         patch('path.to.your.delete_graph_metadata_db') as mock_delete_graph_metadata_db:
        mock_delete_graph_db.return_value = None
        mock_delete_graph_metadata_db.return_value = None

        response = test_app_client.get(f"/graph/delete/{graph_id}")
        assert response.status_code == status.HTTP_200_OK
        mock_delete_graph_db.assert_called_once_with(graph_id)
        mock_delete_graph_metadata_db.assert_called_once_with(graph_id)

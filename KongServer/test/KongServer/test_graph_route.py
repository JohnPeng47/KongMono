from src.server.routes.graph.service import get_graph
from src.server.routes.graph.route import router as graph_route
from src.server.routes.graph.service import save_graph, delete_graph_db, get_graph, delete_graph_metadata_db
from src.server.routes.graph.exceptions import GraphNotFound
from src.KongBot.utils.db import KongBotDB
from src.KongBot.bot.base.graph import KnowledgeGraph

from .utils import convert_kg_to_rf

from uuid import uuid4
import pytest
import json

from .conftest import test_app_client

TEST_GRAPH_SMALL = json.loads(open("test/KongServer/data/data.json", "r").read())
KG_ID = TEST_GRAPH_SMALL['id']
NON_EXISTENT_GRAPHID = "1234"

KG_INSTANCE = KnowledgeGraph("Test Curriculum")
KG_INSTANCE.from_json(TEST_GRAPH_SMALL)
PARENT_NODE = KG_INSTANCE.filter_nodes({"children" : 3})[0]

@pytest.fixture
def test_knowledgegraph():
    save_graph(KG_INSTANCE, title="Test Graph")

    yield

    delete_graph_db(KG_ID)
    delete_graph_metadata_db(KG_ID)
    

class TestGetGraphRoute:
    def test_get_graph_route(self, test_app_client, test_knowledgegraph):
        response = test_app_client.get(f"/graph/{KG_ID}")
        assert response.status_code == 200
        assert response.json() is not None

    def test_get_graph_non_exist_id(self, test_app_client, test_knowledgegraph):
        response = test_app_client.get(f"/graph/{NON_EXISTENT_GRAPHID}")
        assert response.status_code == 404
        assert response.json() is not None

@pytest.fixture
def update_add_child():
    save_graph(KG_INSTANCE, title="Test Graph")

    update_kg = KnowledgeGraph("Test Curriculum")
    update_kg.from_json(TEST_GRAPH_SMALL)
    update_kg.add_node({
        "id": str(uuid4()),
        "node_data": {
            "node_type": "NODE",
            "title": "",
            "children": []
        }
    }, parent_node=PARENT_NODE)

    update_payload = convert_kg_to_rf(update_kg)
    print(json.dumps(update_payload.to_json()))

    yield update_payload.to_json()

    delete_graph_db(KG_ID)
    delete_graph_metadata_db(KG_ID)

class TestUpdateGraphRoute:
    def test_add_node(self, test_app_client, update_add_child):
        response = test_app_client.post(f"/graph/update/{KG_ID}", 
                                        json=update_add_child)
        
        assert response.status_code == 200
        assert response.json() is not None

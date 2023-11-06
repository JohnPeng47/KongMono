from typing import Dict
from database import db_conn

from .exceptions import GraphAuthorizationError
from .schema import GraphMetadata
from ..auth.schema import User

from KongBot.bot.base import KnowledgeGraph

from logging import getLogger

logger = getLogger("server")

def insert_graph_metadata_db(graph_id: str, metadata: GraphMetadata):
    return db_conn.get_collection("graph_metadata").update_one(
        {
            "id": graph_id,
        }, {
            "$set": {
                "metadata": metadata,
            }
        },
        upsert=True)

def list_graph_metadata_db(pagination=10):
    return db_conn.get_collection("graph_metadata").find({}).sort("timestamp", -1).limit(pagination)

def get_graph_metadata_db(graph_id):
    return db_conn.get_collection("graph_metadata").find_one({
        "id": graph_id
    })

def delete_graph_metadata_db(graph_id: str):
    return db_conn.get_collection("graph_metadata").delete_one({
        "id": graph_id
    })

def insert_graph_db(graph: dict):
    return db_conn.get_collection("graphs").update_one(
        {
            "id": graph["id"]
        }, {
            "$set": graph
        },
        upsert=True)

def get_graph_db(graph_id: str):
    return db_conn.get_collection("graphs").find_one({
        "id": graph_id,
    })

def delete_graph_db(graph_id: str):
    return db_conn.get_collection("graphs").delete_one({
        "id": graph_id,
    })

# TODO: put all graph related methods here under GraphManager
class GraphManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphManager, cls).__new__(cls)
        return cls._instance
    
    def check_user_permissions(self, user: User, graph_id: str):
        for user_graph in user.graphs:
            if graph_id == user_graph:
                return True
        raise GraphAuthorizationError(graph_id=graph_id, email=user.email)

    # Find better way to pass user
    # @check_user_auth(user: User)
    def get_graph(self, graph_id: str) -> KnowledgeGraph:
        graph = db_conn.get_collection("graphs").find_one({
            "id": graph_id
        })

        curriculum = graph["curriculum"]
        new_graph = KnowledgeGraph(curriculum)
        new_graph.from_json(graph)
        
        return new_graph
    
    def create_graph(self, curriculum: str, title: str) -> KnowledgeGraph:
        new_kg = KnowledgeGraph(curriculum)
        new_kg.add_node({
            "id": "1",
            "node_data": {
                "title": "",
                "node_type" : "ROOT",
                "children": []
            }
        })

        self.save_graph(new_kg, title=title)
        return True
        
    def save_graph(self, graph: KnowledgeGraph, title: str = ""):
        graph_id = graph.get_root()["id"]
        graph_title = graph.get_root()["node_data"]["title"] if not title else title

        print("Saving graph with title: ", graph_title)

        insert_graph_db(graph.to_json())
        insert_graph_metadata_db(graph_id, {
            "curriculum": graph.curriculum,
            "title": graph_title,
            "tree": graph.display_tree()
        })

        logger.debug(f"Saving graph: {graph_id}")
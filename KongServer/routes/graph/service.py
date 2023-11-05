from typing import Dict
from database import db_conn

from .exceptions import GraphAuthorizationError
from .schema import GraphMetadata
from ..auth.schema import User

from KongBot.bot.base import KnowledgeGraph

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

def get_graph_metadata_db(pagination=10):
    return db_conn.get_collection("graph_metadata").find({}).sort("timestamp", -1).limit(pagination)

def get_graph_db(graph_id: str):
    return db_conn.get_collection("graphs").find_one({
        "id": graph_id,
    })

def delete_graph_db(graph_id: str):
    return db_conn.get_collection("graphs").delete_one({
        "id": graph_id,
    })

def delete_graph_metadata_db(graph_id: str):
    return db_conn.get_collection("graph_metadata").delete_one({
        "id": graph_id
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

    def load_graph(self, user: User, graph_id: str) -> KnowledgeGraph:
        self.check_user_permissions(user, graph_id)

        graph = db_conn.get_collection("graphs").find_one({
            "id": id
        })

        curriculum = graph["curriculum"]
        new_graph = KnowledgeGraph(curriculum)
        new_graph.from_json(graph)
        
        return new_graph
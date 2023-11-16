from typing import Dict
import uuid
from collections import defaultdict

from src.server.database.db import db_conn

from fastapi import Depends, Body

from .exceptions import GraphAuthorizationError
from .schema import GraphMetadata, GenSubgraphRequest
from ..auth.schema import User


from src.KongBot.bot.base import KnowledgeGraph

from logging import getLogger
from threading import Lock

logger = getLogger("base")


# Should add user auth check as a dependency here, and use this as the entry point 
# authz on graph_id
# def get_graph_id(request: GenSubgraphRequest = Body(..., embed=True)) -> str:
#     return request.graph_id

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
    metadata = db_conn.get_collection("graph_metadata").find_one({
        "id": graph_id
    })
    if not metadata:
        logger.error("No metadata is found for: ", graph_id)
        raise Exception("No metadata found for graph: ", graph_id)
    
    return metadata

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

def create_graph(curriculum: str, title: str) -> KnowledgeGraph:
    new_kg = KnowledgeGraph(curriculum)
    new_kg.add_node({
        "id": str(uuid.uuid4()),
        "node_data": {
            "title": "",
            "node_type": "ROOT",
            "children": []
        }
    })

    save_graph(new_kg, title=title)
    return True

# Dependencies
def check_graph_user_auth(user: User, graph: KnowledgeGraph) -> KnowledgeGraph:
    # raise authorization error
    return True


# TEMP
def get_graph(graph_id: str, 
    metadata: GraphMetadata = Depends(get_graph_metadata_db)) -> KnowledgeGraph:
    graph_json = db_conn.get_collection("graphs").find_one({
        "id": graph_id
    })

    if not graph_json:
        raise Exception("No graph is found for: ", graph_id)
    
    # this feels kinda weird
    curriculum = metadata["metadata"]["curriculum"]
    graph = KnowledgeGraph(curriculum)
    graph.from_json(graph_json)

    return graph

def save_graph(graph: KnowledgeGraph, title: str = ""):
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

import time

class GraphManager:
    """
    Class that should be used to manage caching and locking graphs
    Should not be called directly by routes but called internally
    by graph db operation on the service side
    """
    _instance = None
    # TODO: sync with Redis cache eviction
    # https://redis.io/docs/manual/keyspace-notifications/

    def __init__(self):
        self.locks = defaultdict(Lock)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphManager, cls).__new__(cls)
        return cls._instance
    
    def acquire_lock(self, graph_id: str):
        lock = self.locks[graph_id]
        lock.acquire()
        logger.debug(f"Lock acquired: {graph_id}")
    
    def release_lock(self, graph_id: str):
        lock = self.locks.get(graph_id, None)
        if lock is None or not lock.locked():
            raise Exception("Attempt to release an unacquired lock")
        lock.release()
        logger.debug(f"Lock released: {graph_id}")

    def get_graph(self,
            graph_id: str) -> KnowledgeGraph:
        graph_json = db_conn.get_collection("graphs").find_one({
            "id": graph_id
        })

        # not sure if this checks for the real graph
        if not graph_json:
            logger.error("No graph is found for: ", graph_id)
            raise Exception("No graph is found for: ", graph_id)
        
        # this feels kinda weird

        metadata = get_graph_metadata_db(graph_id)
        curriculum = metadata["metadata"]["curriculum"]
        graph = KnowledgeGraph(curriculum)
        graph.from_json(graph_json)

        return graph
    
    def save_graph(self, 
                   graph: KnowledgeGraph, 
                   title: str = ""):
        
        lock = self.locks.get(graph_id)
        if not lock:
            logger.error("Lock not found")
            # raise Exception("Shouldnt happen, implies save graph called before get_graph")
            
        try:
            graph_id = graph.get_root()["id"]
            graph_title = graph.get_root()["node_data"]["title"] if not title else title

            print("Saving: ", graph.to_json())
            insert_graph_db(graph.to_json())
            insert_graph_metadata_db(graph_id, {
                "curriculum": graph.curriculum,
                "title": graph_title,
                "tree": graph.display_tree()
            })

            logger.debug(f"Saving graph: {graph_id} with title: {graph_title}")
        except Exception as e:
            logger.error("Error while saving graph: ", e)
            

def get_graph_v2(graph_id: str) -> KnowledgeGraph:
    graph_manager = GraphManager()
    return graph_manager.get_graph(graph_id)

def save_graph_v2(graph: KnowledgeGraph, title: str = ""):
    graph_manager = GraphManager()
    return graph_manager.save_graph(graph)


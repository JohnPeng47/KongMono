from typing import Dict
from common import db_conn

from .schema import GraphMetadata

# does it make sense to store this on graph in separate collection?
# thinking is, we may not want to load the full graph in mem if we just
# want to grab the metadata


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

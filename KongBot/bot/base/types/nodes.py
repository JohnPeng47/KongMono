from utils import gen_unique_id
from typing import List
from enum import Enum

from ..utils import CustomDict

class NodeType(Enum):
    TREE_NODE = "TREE_NODE"

class DataNode(CustomDict):
    def __init__(self, title: str, node_type: NodeType, children: List = [], description: str = ""):
        self.data = {
            "id": gen_unique_id(),
            "node_data" : {
                "title" : title,
                "node_type" : "TREE_NODE",
                "children" : [],
                "description": ""
            }
        }
    
    def to_json(self):
        children = [child.to_json() for child in self.data["node_data"]["children"]]
        self.data["node_data"]["children"] = children
        return self.data
from pydantic import BaseModel
from typing import Optional, List, Dict

class GraphNodeData(BaseModel):
    title: str
    node_type: str
    description: Optional[str]
    entity_relations: Optional[List[Dict]]
    concept: Optional[str]
    color: Optional[str]
    children: List["GraphNode"]

class GraphNode(BaseModel):
    id: str
    data: GraphNodeData

class GraphRootNode(BaseModel):
    id: str
    data: GraphNodeData
    # include some other structures
    curriculum: str
    title: str

GraphNodeData.update_forward_refs()

    

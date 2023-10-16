from pydantic import BaseModel
from typing import Optional, List, Dict


class Position(BaseModel):
    x: int
    y: int
class GraphNodeData(BaseModel):
    title: str
    node_type: str
    description: Optional[str]
    entity_relations: Optional[List[Dict]]
    concept: Optional[str]
    color: Optional[str]
    children: Optional[List["GraphNode"]]

class GraphNode(BaseModel):
    id: str
    hidden: Optional[bool]
    data: GraphNodeData
    position: Position

# used to resolve the forward reference in the children field
GraphNodeData.update_forward_refs()

class GraphMetadata(BaseModel):
    curriculum: str
    title: str

class GraphMetadataResp(BaseModel):
    id: str
    metadata: GraphMetadata

# RFNode 
class RFNode(BaseModel):
    id: str
    data: GraphNodeData
    hidden: bool
    type: str
    position: Position
    positionAbsolute: Position
    height: Optional[int]
    width: Optional[int]
    
class SaveGraphReq(BaseModel):
    title: str
    graph: RFNode

def rfnode_to_kgnode(node: RFNode):
    node_data = node.data
    node_data.children = [rfnode_to_kgnode(child) for child in node_data.children]
    
    return {
        "id": node.id,
        "node_data": node_data.dict()
    }
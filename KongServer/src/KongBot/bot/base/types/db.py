from abc import ABC
from typing import Optional
from .graph import GraphRootNode

class GraphDB(ABC):
    """
    DB interface that supports both trees and Graph types
    """
    def create(self, graph: GraphRootNode) -> GraphRootNode:
        raise NotImplementedError

    def get(self, graphid: str) -> Optional[GraphRootNode]:
        raise NotImplementedError
    
    def update(self, graph: GraphRootNode) -> GraphRootNode:
        raise NotImplementedError

    def delete(self, graphid: str) -> None:
        raise NotImplementedError

    def get_metadata(self, graphid: str) -> GraphRootNode:
        raise NotImplementedError
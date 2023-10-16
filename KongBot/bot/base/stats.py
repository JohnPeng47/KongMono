from bot.base import KnowledgeGraph
from .types.nodes import DataNode

import queue

def get_nodes_from_depth(graph: KnowledgeGraph, depth: int, node_id: str = "root"):
    """
    Get nodes at depth n away from the node at id
    """
    start_node = graph.get_root() if node_id == "root" else graph.get_node(node_id)
    visited = set([node_id])
    node_queue = []
    curr_depth = 0

    node_queue.insert(0, (start_node, curr_depth))

    # check that child node from previous iteration has been dequeue'd and looked at
    while node_queue and curr_depth < depth:
        node, curr_depth = node_queue.pop()
        
        # we have to check visited as well some nodes might have connections back to beginning nodes
        children = [
            graph.get_node(child_id) for child_id in graph.children(node["id"]) 
            if child_id not in visited
        ] 
        for child_node in children:
            node_queue.insert(0, (child_node, curr_depth + 1))
            visited.add(child_node["id"])
    
    return map(lambda x: x[0], node_queue)
            
            

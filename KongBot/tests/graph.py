import pytest
from bot.base import KnowledgeGraph

@pytest.fixture
def knowledge_graph():
    return KnowledgeGraph("context")

def test_add_single_node(knowledge_graph):
    node = {
        "id": "1",
        "node_data": {
            "title": "Node 1",
            "node_type": "type1",
            "children": []
        }
    }
    
    knowledge_graph.add_node(node, {})
    assert knowledge_graph.has_node("1")

def test_add_node_with_parent(knowledge_graph):
    parent = {
        "id": "1",
        "node_data": {
            "title": "Parent Node",
            "node_type": "type1",
            "children": []
        }
    }
    child = {
        "id": "2",
        "node_data": {
            "title": "Child Node",
            "node_type": "type2",
            "children": []
        }
    }

    knowledge_graph.add_node(parent, {})
    knowledge_graph.add_node(child, parent)
    assert knowledge_graph.has_edge("1", "2")

def test_add_node_with_merge(knowledge_graph):
    root = {
        "id": "0",
        "node_data": {
            "title": "Root Node",
            "node_type": "type1",
            "children": []
        }
    }
    parent = {
        "id": "1",
        "node_data": {
            "title": "Parent Node",
            "node_type": "type2",
            "children": []
        }
    }
    child = {
        "id": "1",
        "node_data": {
            "title": "Child Node",
            "node_type": "type3",
            "children": []
        }
    }
    
    knowledge_graph.add_node(root, {})
    knowledge_graph.add_node(parent, root)
    knowledge_graph.add_node(child, merge=True)
    
    assert knowledge_graph.has_edge("0", "1")
    # assert not knowledge_graph.has_node("1")

def test_recursive_add(knowledge_graph):
    parent = {
        "id": "1",
        "node_data": {
            "title": "Parent Node",
            "node_type": "type1",
            "children": [
                {
                    "id": "3",
                    "node_data": {
                        "title": "Child 1",
                        "node_type": "type2",
                        "children": []
                    }
                },
                {
                    "id": "4",
                    "node_data": {
                        "title": "Child 2",
                        "node_type": "type3",
                        "children": []
                    }
                }
            ]
        }
    }

    knowledge_graph.add_node(parent, {})
    
    assert knowledge_graph.has_edge("1", "3")
    assert knowledge_graph.has_edge("1", "4")

def test_add_root_with_merge(knowledge_graph):
    root = {
        "id": "0",
        "node_data": {
            "title": "Root Node",
            "node_type": "ROOT",
            "children": []
        }
    }
    root2 = {
        "id": "0",
        "node_data": {
            "title": "Parent Node",
            "node_type": "ROOT",
            "children": []
        }
    }
    child = {
        "id": "1",
        "node_data": {
            "title": "Child Node",
            "node_type": "type3",
            "children": []
        }
    }
    
    knowledge_graph.add_node(root, {})
    knowledge_graph.add_node(root2, merge=True)
    knowledge_graph.add_node(child, root2)
    
    assert knowledge_graph.has_edge("0", "1")

def test_get_node(knowledge_graph):
    root = {
        "id": "1",
        "node_data": {
            "title": "Parent Node",
            "node_type": "type1",
            "children": [
                {
                    "id": "3",
                    "node_data": {
                        "title": "Child 1",
                        "node_type": "type2",
                        "children": []
                    }
                },
                {
                    "id": "4",
                    "node_data": {
                        "title": "Child 2",
                        "node_type": "type3",
                        "children": []
                    }
                }
            ]
        }
    }

    
    knowledge_graph.add_node(root, {})
    
    graph = knowledge_graph.get_node("1")
    assert "children" in graph["node_data"].keys()


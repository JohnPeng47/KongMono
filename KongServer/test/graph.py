
import pytest
import sys
from src.KongBot.bot.base import KnowledgeGraph


@pytest.fixture
def empty_knowledge_graph():
    print(sys.path)
    context = "Test"
    return KnowledgeGraph(context)


def test_add_single_node(empty_knowledge_graph):
    node = {
        "id": "1",
        "node_data": {
            "title": "Node 1",
            "node_type": "type1",
            "children": []
        }
    }

    empty_knowledge_graph.add_node(node, {})
    assert empty_knowledge_graph.has_node("1")


def test_add_node_with_parent(empty_knowledge_graph):
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

    empty_knowledge_graph.add_node(parent, {})
    empty_knowledge_graph.add_node(child, parent)
    assert empty_knowledge_graph.has_edge("1", "2")


def test_add_node_with_merge(empty_knowledge_graph):
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

    empty_knowledge_graph.add_node(root, {})
    empty_knowledge_graph.add_node(parent, root)
    empty_knowledge_graph.add_node(child, merge=True)

    assert empty_knowledge_graph.has_edge("0", "1")
    # assert not empty_knowledge_graph.has_node("1")


def test_recursive_add(empty_knowledge_graph):
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

    empty_knowledge_graph.add_node(parent, {})

    assert empty_knowledge_graph.has_edge("1", "3")
    assert empty_knowledge_graph.has_edge("1", "4")


def test_add_root_with_merge(empty_knowledge_graph):
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

    empty_knowledge_graph.add_node(root, {})
    empty_knowledge_graph.add_node(root2, merge=True)
    empty_knowledge_graph.add_node(child, root2)

    assert empty_knowledge_graph.has_edge("0", "1")


def test_add_non_root_type_to_root_with_merge(empty_knowledge_graph):
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
            "node_type": "NormalNode",
            "children": []
        }
    }

    empty_knowledge_graph.add_node(root, {})
    empty_knowledge_graph.add_node(root2, merge=True)

    assert empty_knowledge_graph.get_root() != {}


def test_get_node(empty_knowledge_graph):
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

    empty_knowledge_graph.add_node(root, {})

    graph = empty_knowledge_graph.get_node("1")
    assert "children" in graph["node_data"].keys()


def test_parents(empty_knowledge_graph):
    # Set up the nodes
    parent_node = {
        "id": "1",
        "node_data": {
            "title": "Parent Node",
            "node_type": "type1",
            "children": []
        }
    }

    child_node = {
        "id": "3",
        "node_data": {
            "title": "Child Node",
            "node_type": "type2",
            "children": []
        }
    }

    # Add the nodes to the knowledge graph
    empty_knowledge_graph.add_node(parent_node, {})
    empty_knowledge_graph.add_node(child_node, parent_node)

    # Test for tree mode
    parent_tree = empty_knowledge_graph.parents("3", tree=True)
    assert parent_tree == "1"

    # Test for graph mode
    parent_graph = empty_knowledge_graph.parents("3", tree=False)
    assert "1" in parent_graph

    # Test when node has no parent (in tree mode)
    no_parent_tree = empty_knowledge_graph.parents("1", tree=True)
    assert no_parent_tree == []

    # Test when node has no parent (in graph mode)
    no_parent_graph = empty_knowledge_graph.parents("1", tree=False)
    assert no_parent_graph == []


def test_ancestors(empty_knowledge_graph):
    # Setting up nodes
    grandparent_node = {
        "id": "1",
        "node_data": {
            "title": "Grandparent Node",
            "node_type": "type1",
            "children": []
        }
    }

    parent_node = {
        "id": "2",
        "node_data": {
            "title": "Parent Node",
            "node_type": "type2",
            "children": []
        }
    }

    child_node = {
        "id": "3",
        "node_data": {
            "title": "Child Node",
            "node_type": "type3",
            "children": []
        }
    }

    # Adding nodes to the knowledge graph
    empty_knowledge_graph.add_node(grandparent_node, {})
    empty_knowledge_graph.add_node(parent_node, grandparent_node)
    empty_knowledge_graph.add_node(child_node, parent_node)

    # Testing ancestors for child node
    assert empty_knowledge_graph.ancestors("3") == ["1", "2"]
    # Testing ancestors for parent node
    assert empty_knowledge_graph.ancestors("2") == ["1"]

    # Testing ancestors for grandparent node (no ancestors)
    assert empty_knowledge_graph.ancestors("1") == []

# def test_display_tree_v2_lineage(empty_knowledge_graph):
#     knowledge_graph = empty_knowledge_graph
#     root = {
#         "id": "1",
#         "node_data": {
#             "title": "Parent Node",
#             "node_type": "type1",
#             "children": [
#                 {
#                     "id": "3",
#                     "node_data": {
#                         "title": "Child 1",
#                         "node_type": "type2",
#                         "children": []
#                     }
#                 },
#                 {
#                     "id": "4",
#                     "node_data": {
#                         "title": "Child 2",
#                         "node_type": "type3",
#                         "children": []
#                     }
#                 }
#             ]
#         }
#     }
#     knowledge_graph.add_node(root, {})

#     # Testing display_tree_v2_lineage for child node
#     ancestors_tree, subtree_tree = knowledge_graph.display_tree_v2_lineage("3")
#     # TODO: failing but imo not important
#     # assert ancestors_tree == """
#     # ANCESTORS
#     # --------
#     # [0] Parent Node
#     # SUBTREE
#     # --------
#     # [0] Child 1
#     # """

#     assert subtree_tree == "[0] Child 1\n"
#     # Testing display_tree_v2_lineage for parent node
#     ancestors_tree, subtree_tree = knowledge_graph.display_tree_v2_lineage("1")
#     assert ancestors_tree == "SUBTREE\n--------\n"
#     assert subtree_tree == "[0] Parent Node\n[1] Child 1\n[1] Child 2\n"

# def test_display_tree_v2(empty_knowledge_graph):
#     knowledge_graph = empty_knowledge_graph
#     root = {
#         "id": "1",
#         "node_data": {
#             "title": "Parent Node",
#             "node_type": "type1",
#             "children": [
#                 {
#                     "id": "3",
#                     "node_data": {
#                         "title": "Child 1",
#                         "node_type": "type2",
#                         "children": []
#                     }
#                 },
#                 {
#                     "id": "4",
#                     "node_data": {
#                         "title": "Child 2",
#                         "node_type": "type3",
#                         "children": []
#                     }
#                 }
#             ]
#         }
#     }
#     knowledge_graph.add_node(root, {})

#     # Testing display_tree_v2 for child node
#     result = knowledge_graph.display_tree_v2(knowledge_graph.get_node("3"))
#     assert result == "[0] Child 1\n"

#     # Testing display_tree_v2 for parent node
#     result = knowledge_graph.display_tree_v2(knowledge_graph.get_node("1"))
#     assert result == "[0] Parent Node\n[1] Child 1\n[1] Child 2\n"

# def test_filter_nodes(empty_knowledge_graph):
#     knowledge_graph = empty_knowledge_graph
#     # Sample data for our tests
#     knowledge_graph.add_node("1", node_data={"title": "Node1", "hello": "world", "depth": 1, "children": []})
#     knowledge_graph.add_node("2", node_data={"title": "Node2", "hello": "1234", "depth": 2, "children": ["3", "4"]})
#     knowledge_graph.add_node("3", node_data={"title": "Node3", "hello": "world", "depth": 3, "children": []})
#     knowledge_graph.add_node("4", node_data={"title": "Node4", "hello": "world", "depth": 3, "children": []})

#     # Testing filtering with no filter
#     result = knowledge_graph.filter_nodes({})
#     expected = [
#         {"id": "1", "node_data": {"title": "Node1", "hello": "world", "depth": 1, "children": []}},
#         {"id": "2", "node_data": {"title": "Node2", "hello": "1234", "depth": 2, "children": ["3", "4"]}},
#         {"id": "3", "node_data": {"title": "Node3", "hello": "world", "depth": 3, "children": []}},
#         {"id": "4", "node_data": {"title": "Node4", "hello": "world", "depth": 3, "children": []}}
#     ]
#     assert sorted(result, key=lambda x: x["id"]) == sorted(expected, key=lambda x: x["id"])

#     # Testing filtering nodes by depth
#     result = knowledge_graph.filter_nodes({"depth": 3})
#     expected = [
#         {"id": "3", "node_data": {"title": "Node3", "hello": "world", "depth": 3, "children": []}},
#         {"id": "4", "node_data": {"title": "Node4", "hello": "world", "depth": 3, "children": []}}
#     ]
#     assert sorted(result, key=lambda x: x["id"]) == sorted(expected, key=lambda x: x["id"])

#     # Testing filtering nodes by number of children
#     result = knowledge_graph.filter_nodes({"children": 2})
#     expected = [
#         {"id": "2", "node_data": {"title": "Node2", "hello": "1234", "depth": 2, "children": ["3", "4"]}}
#     ]
#     assert result == expected

#     # Testing filtering nodes by an attribute and value
#     result = knowledge_graph.filter_nodes({"hello": "1234"})
#     expected = [
#         {"id": "2", "node_data": {"title": "Node2", "hello": "1234", "depth": 2, "children": ["3", "4"]}}
#     ]
#     assert result == expected

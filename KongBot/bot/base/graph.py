from __future__ import annotations

from networkx.classes import DiGraph
from networkx.algorithms.shortest_paths.generic import shortest_path

from typing import List, Dict, Callable, Optional

from bot.adapters.kg_to_frontend import FrontEndNodeAdapter
from bot.base.exceptions import ConfigInitError

from .utils import CustomDict
from utils import db_conn
from inspect import iscoroutinefunction

import asyncio
import logging

from utils.logger import initialize_logging

import json
import os
import random
from functools import cached_property

import logging

import warnings
warnings.filterwarnings("ignore", message="Numerical issues were encountered ")

# initialize the logger
initialize_logging()

# Considerations and TODOs:
# 1. Currently the node object uses the self.node dictionary representation used
# by networkx. Efforts to define a custom class for this has not been attempted
# because of uncertainty in new methods added to the class


class KnowledgeGraph(DiGraph):
    """
    This data structure contains a set of graph operations for a set of Nodes
    """

    def __init__(self,
                 curriculum: str,
                 generators: List[Callable] = [],
                 graph_id: str = None,
                 config: Dict = {},
                 log_lvl: int = logging.DEBUG
                 ):        
        seed = os.environ.get("RANDOM_SEED", None)
        if seed:
            random.seed(int(seed))

        super().__init__()

        self.curriculum = curriculum
        self.generators = generators
        self.call_costs = {
            "total_tokens": 0,
            "prompt_tokens": 0,
            "complete_tokens": 0,
            "total_cost": 0
        }

        # stat variables
        self.finish_generation = False
        if graph_id != None:
            graph_json = self.load_graph(graph_id)
            if not graph_json:
                raise Exception(f"Graph_id not found: {graph_id}")

            self.from_json(graph_json)

        if config:
            self.validate_config(config)
            self.config = config

    @classmethod
    def get_graphs(cls, run_id: str):
        graphs = db_conn.get_collection("graphs").find({
            "run_id": run_id
        })

        return [
            cls(graph["curriculum"], graph_id=graph["id"]) for graph in graphs
        ]

    @classmethod
    def load_graph(cls, id) -> KnowledgeGraph:
        graph = db_conn.get_collection("graphs").find_one({
            "id": id
        })
        curriculum = graph["curriculum"]
        
        new_graph = cls(curriculum)
        new_graph.from_json(graph)
        
        return new_graph

    def save_graph(self, run_id: str = None, title: str = ""):
        """
        Save graph to mongo
        """
        graph_id = self.get_root()["id"]
        graph_title = self.get_root()["node_data"]["title"] if not title else title

        db_conn.insert_graph(self.to_json(), run_id=run_id)
        db_conn.insert_graph_metadata(graph_id, {
            "curriculum": self.curriculum,
            "title": graph_title,
            "tree": self.display_tree()
        })

        print("Saving graph: ", self.get_root()["id"])

    def write_graph(self, name: str = "graph.json"):
        with open(r"output\{}".format(name), "w") as g:
            frontend_json = self.to_json_frontend()
            g.write(frontend_json)

    def generate_nodes(self):
        """
        This method is for explicitly generating nodes
        TODO: should add error handling here
        """
        error = False
        for g in self.generators:
            if iscoroutinefunction(g):
                asyncio.run(g(self))
            else:
                g(self)

        self.finish_generation = True
        return not error

    def add_generators(self, generators: List):
        """
        Adds generators
        """
        self.generators.extend(generators)

    def add_config(self, config):
        self.validate_config(config)
        self.config = config

    # TODO: make sure to change to Dict
    def filter_nodes(self, node_filter: Dict) -> List[Dict]:
        """ 
        Replace this function later with GraphDB
        For now only supports single atrribute filters
        Single attribute filter on node_data
        kg = KnowledgeGraph()
        kg.add_node("key", node_data={"hello": "woild"})
        kg.add_node("key", node_data={"hello": "1234"})
        kg.filter_nodes({"hello": "1234"})

        Output:
        [('key', {'hello': '1234'})]
        """
        if node_filter == {}:
            return self.nodes.data()

        # only doing single key comparisons for now
        key, value = list(node_filter.keys())[0], \
            list(node_filter.values())[0]

        if value == False and value != 0:
            raise Exception("False as value is not allowed. If negative key condition is desired, \
                            use False instead")

        if key == "depth":
            return self.get_nodes_from_depth(value)

        if key == "children":
            num_children = value

            return list(map(
                lambda node_id: self.get_node(node_id),
                list(filter(lambda node: len(self.children(node))
                     >= num_children, self.nodes))
            ))
        
        return_val = []
        for node in self.nodes.data("node_data"):
            if node[1].get(key, None) == value:
                return_val.append({
                    "id": node[0],
                    "node_data": node[1]
                })

        return return_val

    def filter_nodes_single(self, node_filter: str):
        filtered_node = self.filter_nodes(node_filter)
        if len(filtered_node) > 1:
            raise Exception("Expecting a single, got multiple: ")
        if len(filtered_node) < 1:
            raise Exception("Expecting a single node, got none: ")

        return filtered_node[0]

    def get_node(self, node_id: str) -> Dict:
        return {
            "id": node_id,
            # why does this work with super but not self?
            # super returns
            "node_data": self._node[node_id]["node_data"]
        }

    def remove_node(self, node_id: str):
        """
        Recursively removes a node along with all of its children
        """
        for child_id in self.children(node_id):
            self.remove_node(child_id)

        parents = self.parents(node_id)
        for parent_id in parents:
            super().remove_edge(parent_id, node_id)

        super().remove_node(node_id)

    def add_node(self, child_node: Dict, parent_node: dict = {}, merge: bool = False):
        """
        Recursively adds a node and all its children to graph
        To add parent to an empty graph: 
        Three use cases:
        > Add root
        g.add_node(root, {})
        
        > Add child to parent
        g.add_node(child, parent)

        > Merge node
        g.add_node(node, merge=True)
        """            
        self._validate_node(child_node)
            
        child_id, node_data = child_node["id"], child_node["node_data"]

        # delete children to save space
        # children = node_data.pop("children", [])

        if merge:
            if child_id == self.get_root()["id"]:
                node_data["node_type"] = "ROOT"

            # TODO: we cant assume only one parent for graph
            # assume its one parent for tree
            grandparent_id = self.parents(child_id, tree=True)                
            self.remove_node(child_id)

            super().add_node(child_id, node_data=node_data)
            
            # root nodes have no parents :(
            if grandparent_id:
                super().add_edge(grandparent_id, child_id)
        else:
            super().add_node(child_id, node_data=node_data)
            if parent_node == {}:
                node_data["node_type"] = "ROOT"
            else:
                super().add_edge(parent_node["id"], child_id)

        for c in node_data["children"]:
            self.add_node(c, child_node)

    def add_nodes(self, child_nodes: List[Dict], parent_node: Optional[Dict]):
        for child_node in child_nodes:
            self.add_node(child_node, parent_node)

    def modify_node(self, node_id: str, data: Dict):
        for key in data.keys():
            self._node[node_id]["node_data"][key] = data[key]

    # FAMILY FUNCTIONS
    # kinda weird, since we should be using the node_filter API but w.e....
    def siblings(self, node_id: str):
        """
        Should only support trees
        """
        parent = self.parents(node_id)
        return list(filter(
            lambda sibling_id: sibling_id, self.children(parent)
            # lambda sibling_id: sibling_id != node_id, self.children(parent)
        ))

    def get_num_nodes(self, node_id: str):
        if len(self.children(node_id)) == 0:
            return 1

        children = 0
        for child_id in self.children(node_id):
            my_kids = self.get_num_nodes(child_id)
            children += my_kids

        # add curr node to the total
        children += 1
        return children

    def children(self, node_id: str):
        return list(super().successors(node_id))

    def parents(self, node_id: str, tree: bool = False) -> List | str:
        """
        Returns parents if graph, else returns a single parent if tree
        """
        # if not tree:
        #     raise Exception(
        #         "Think about what you are doing, we WERE only supporting trees")

        parents = list(super().predecessors(node_id))
        if tree:
            try:
                return parents[0]
            except IndexError:
                return []
        return parents

    def ancestors(self, node_id: str, ancestors=None):
        if ancestors is None:
            ancestors = []

        parent_id = self.parents(node_id, tree=True)
        if not parent_id:
            return ancestors

        ancestors: List = self.ancestors(parent_id, ancestors=ancestors)
        ancestors.append(parent_id)
        return ancestors

    # TODO: make sure this returns dict
    def get_root(self) -> Dict:
        nodes = self.filter_nodes({"node_type": "ROOT"})
        return nodes[0] if len(nodes) > 0 else {}

    def _validate_node(self, node: Dict):
        """
        Check that node is the proper structure
        """
        node_id = node["id"]
        if not isinstance(node_id, str):
            raise Exception("Node id is not string: ", node)
        
        # check lvl 1
        required_keys_node = set(["id", "node_data"])
        if not required_keys_node.issubset(set(node.keys())):
            raise Exception("One of these keys are missing: []'id', 'node_data'] ", node)
        # check lvl 2
        else:
            required_keys_node_data = set(["title", "node_type", "children"])
            if not required_keys_node_data.issubset(set(node["node_data"].keys())):
                raise Exception("One of these keys are missing: ", ["title", "node_type", "children"])
            
            if not isinstance(node["node_data"]["children"], list):
                raise Exception("Children is not a list", node)

    # TODO: modify this after changing filter_nodes implementation
    # to avoid raising exceptions on missing keys
    def to_entity_relation_graph(self):
        entity_relations = []
        nodes = self.filter_nodes({"children": 3})
        for node in nodes:
            entity_relations += node["node_data"]["entity_relations"]
        return entity_relations
        
    def to_json_frontend(self, show_all: bool = False, parent_node: Dict = None):
        """
        Convert Graph to representation for ReactFlow Frontend
        """
        knowledgeGraph: KnowledgeGraph = self

        frontend_adapter = FrontEndNodeAdapter(
            knowledgeGraph, show_all=show_all)
        
        frontend_json = self.to_json(parent_node=parent_node,
            modify_node=frontend_adapter.kg_node_to_frontend_adapter)
        
        return json.dumps(frontend_json, indent=4)

    def to_json_frontend_entity_relations(self):
        knowledgeGraph: KnowledgeGraph = self

        frontend_adapter = FrontEndNodeAdapter(knowledgeGraph)
        return json.dumps(self.to_json(modify_node=frontend_adapter.kg_node_to_frontend_adapter), indent=4)

    def to_json(self, parent_node: Dict = None, modify_node=lambda x: x) -> Dict:
        """
        Converts graph to JSON representation thet 
        """
        if not parent_node:
            parent_node = self.get_root()
            parent_node["curriculum"] = self.curriculum
            
            # delete mongo UUID
            if parent_node.get("_id", None):
                del parent_node["_id"]

            # no root node
            if parent_node == {}:
                return parent_node

        parent_node["node_data"]["children"] = []

        for n in super().neighbors(parent_node["id"]):
            child_node = self.get_node(n)
            parent_node["node_data"]["children"].append(
                self.to_json(parent_node=child_node, modify_node=modify_node))
        
        modified_parent = modify_node(parent_node)
        return modified_parent

    def from_json(self, json_data: Dict, parent_node: Dict = None):
        """
        Creates a completely new graph from JSON
        """
        # delete mongo UUID
        if json_data.get("_id", None):
            del json_data["_id"]

        root_node = self.get_root()
        if root_node != {}:
            super().remove_node(root_node["id"])

        if not parent_node:
            json_data["node_data"]["node_type"] = "ROOT"
            self.add_node(json_data, {})

    def validate_config(self, config: Dict):
        """
        Method basically useless right now but keep and modify later
        when we actually know what we want in the configs
        """
        if config == {}:
            print("Empty config")

        print(Config.generators)

        for config_k, _ in config.items():
            # check that there is config key for every generator passed in
            # if config_k not in [g.__name__ for g in self.generators]:
            #     print(f"Generator {config_k} in config not found")
            if config_k not in Config.generators:
                raise ConfigInitError(f"Config {config_k} not found")

    @cached_property
    def leaves(self):
        return [node for node in self.nodes if self.out_degree(node) == 0 and self.in_degree(node) != 0]

    def shortest_path(self, target) -> List[Dict]:
        root_id = self.get_root()["id"]
        path = shortest_path(self, root_id, target)
        return [self.get_node(node_id) for node_id in path]

    def get_random_node(self, node_filter: str = None):
        if node_filter:
            return random.choice(self.filter_nodes(node_filter))
        else:
            root_id = self.get_root()["id"]
            node_ids = self.nodes
            node_ids = list(filter(lambda x: x != root_id, self.nodes))

            node_id = random.choice(node_ids)
            return self.nodes[node_id]

    def get_random_single_path(self, path: List = None, path_len: int = 3) -> List[Dict]:
        if path_len == 1:
            return self.get_random_node()

        if path == None:
            path = []

        node = self.get_root() if path == [] else path[-1]
        child_ids = list(super().neighbors(node["id"]))

        if child_ids == []:
            return path
        else:
            child_id = random.choice(child_ids)
            child = self.get_node(child_id)
            path.append(child)

            return self.get_random_single_path(path=path, path_len=path_len)

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)

    def display_llm_call_costs(self):
        if not self.finish_generation:
            return "NOT finished generating"

        return "".join([str(key) + ":" + str(val) + "\n" for key, val in self.call_costs.items()])

    #### Break this up into another class
    def display_tree_v2_lineage(self,
                                node_id: str = ""):
        ancestors_tree, tree_tree = "", ""
        node = self.get_node(node_id) if node_id else self.get_root()
        ancestors = [self.get_node(id) for id in self.ancestors(node_id)] if node_id else []
        # ancestors.reverse()

        ancestors_tree += "ANCESTORS\n--------\n" if node["node_data"]["node_type"] != "ROOT" else ""

        for i, ancestor in enumerate(ancestors):
            title = ancestor["node_data"]["title"]
            ancestors_tree += f"[{i}] {title}\n"

        ancestors_tree += "SUBTREE\n--------\n"
        tree_tree += self.display_tree_v2(node)
        # need this for pre-conditioning the LLM response
        first_line = tree_tree.split("\n")[0]

        return ancestors_tree, tree_tree, first_line

    # need to write adapter
    def display_tree_v2(self,
                     node: Dict,
                     depth = 0):  
        tree = ""
        title = node["node_data"]["title"]
        tree += f"[{depth}] {title}\n"
        
        for child in node["node_data"]["children"]:
            tree += self.display_tree_v2(child, depth = depth + 1)

        return tree
        
    def display_tree(self,
                     node_id: str = "root",
                     depth: int = 0,
                     stop_depth: int = 100000000,
                     lineage: bool = False):
        INDENT = "--" * depth + "> "

        # terminate if we reach stop
        if stop_depth and stop_depth == depth:
            return ""

        tree_node = self.get_root() if node_id == "root" else self.get_node(node_id)
        node_id = tree_node["id"]

        ancestors = self.ancestors(node_id)
        ancestors_display = ""
        ancestors_depth = 0
        if ancestors and lineage:
            for ancestor in ancestors:
                title = self.get_node(ancestor)["node_data"]["title"]
                INDENT = "--" * ancestors_depth + "> "
                ancestors_display += INDENT + title + "\n"
                ancestors_depth += 1

        # add separator between ancestors and tree
        if lineage:
            ancestors_display += "=========SEPARATOR=========\n"

        # if ancestors, add them to the depth count
        depth = ancestors_depth if depth == 0 else depth
        INDENT = "--" * depth + "> "
        if not tree_node["node_data"]["title"]:
            return ""

        return ancestors_display + INDENT + tree_node["node_data"]["title"] + "\n" + "".join([
            self.display_tree(
                child_id,
                depth=depth + 1,
                lineage=False,
                # increment stop_depth by ancestors_depth to match depth
                stop_depth=stop_depth + ancestors_depth if stop_depth else 100000000) for child_id in self.children(node_id)
        ])
        
    def get_nodes_from_depth(self, depth: int, node_id: str = "root") -> List[Dict]:
        """
        Get nodes at depth n away from the node at id
        """
        start_node = self.get_root() if node_id == "root" else self.get_node(node_id)
        visited = set([node_id])
        node_queue = []
        curr_depth = 0

        node_queue.insert(0, (start_node, curr_depth))

        # check that child node from previous iteration has been dequeue'd and looked at
        while node_queue and curr_depth < depth:
            node, curr_depth = node_queue.pop()
            if curr_depth >= depth:
                # super ghetto, but basically have to do this
                # or else we skip this node and add its children
                node_queue.append((node, curr_depth))
                break

            # we have to check visited as well some nodes might have connections back to beginning nodes
            unvisited_children = [
                self.get_node(child_id) for child_id in self.children(node["id"])
                if child_id not in visited
            ]
            for child_node in unvisited_children:
                node_queue.insert(0, (child_node, curr_depth + 1))
                visited.add(child_node["id"])

        return list(map(lambda x: x[0], node_queue))

    # STATS::
    def display_stats(self):
        return """
Num nodes: {num_nodes}
Max depth: {max_depth}
        """.format(**self.stats())

    def stats(self):
        return {
            "num_nodes": len(self.nodes),
            "max_depth": self.max_depth()
        }

    def max_depth(self) -> int:
        depth = 0
        while self.get_nodes_from_depth(depth):
            depth += 1
        # note that this number starts at 0 indexing
        return depth

    def update_call_costs(self, call_costs: Dict):
        self.call_costs["total_tokens"] += call_costs["total_tokens"]
        self.call_costs["prompt_tokens"] += call_costs["prompt_tokens"]
        self.call_costs["complete_tokens"] += call_costs["complete_tokens"]
        self.call_costs["total_cost"] += call_costs["total_cost"]

class Config:
    generators = [
        "global",
        "generate_tree",
        "generate_sub_trees",
        "generate_subtree_descriptions",
        "generate_entity_relations",
        "generate_short_description",
        "generate_long_description"
    ]    
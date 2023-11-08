# from src.KongBot.bot.base import KnowledgeGraph
import random
from typing import Dict, List


class FrontEndNodeAdapter:
    def __init__(self, kg, show_all: bool = False):
        self.show_all = show_all
        self.kg = kg
        colors = [
            "#FFA630",
            "#399E5A",
            "#5ABCB9",
            "#63E2C6",
            "#6EF9F5",
            "#F18F01",
            "#99C24D",
            "#77A6B6",
            "#D81159",
            "#8A4FFF",
            "#EDAFB8",
            "#56EEF4"
        ]
        # get the targeted node_ids
        self.targeted_ids = [node["id"]
                             for node in kg.filter_nodes({"depth": 1})]
        self.targeted_ids.append(self.kg.get_root()["id"])

        self.parent_colors = {k: v for k, v in zip(
            self.targeted_ids, random.sample(colors, len(self.targeted_ids)))}

    def _get_keywords(self, node_id: str) -> List:
        from functools import reduce
        """
        Only gets list of entities from ancestors for now and set hard max on number of keywords returned
        """
        # Error in this line
        ancestor_entity_relations = reduce(lambda keywords, node_id:
                                           keywords + self.kg.get_node(node_id)["node_data"].get("entity_relations", ""), self.kg.ancestors(node_id), [])
        entities = reduce(lambda entities, entity_relation:
                          entities + [entity_relation["target"], entity_relation["source"]], ancestor_entity_relations, [])

        return list(set(entities[:5])) if set(entities) else []

    def _get_color(self, node_id: str) -> str:
        if self.parent_colors.get(node_id, None):
            return self.parent_colors.get(node_id)

        for ancestor_id in self.kg.ancestors(node_id):
            if ancestor_id in self.parent_colors.keys():
                return self.parent_colors[ancestor_id]

        # this should only happen for root
        # worst color
        return "#2E1503"

    # directly modifying nodes for now
    # but think about how to apply transform later
    # map transforms to node_id and apply using the modify_nodes callback in to_json?
    def get_layout_coords(self, node_id: str):
        X_INTERVAL = 50
        Y_INTERVAL = 50
        # 1. get all the sibling nodes that came before current node
        level = 0
        siblings = [node["id"]
                    for node in self.kg.filter_nodes({"depth": level})]

        # TODO: pretty dumb way, should do len of path to root
        while node_id not in siblings:
            if level > self.kg.max_depth():
                # TODO: random nodes not in graph
                print("Reached max depth and node is not in graph: ", self.kg.get_node(
                    node_id)["node_data"]["title"], "|| ID: ", node_id)
                return 0, 0
                # raise Exception("Reached max depth and node is not in graph")
            level += 1
            siblings = [node["id"]
                        for node in self.kg.filter_nodes({"depth": level})]

        x = level * X_INTERVAL
        # get all nodes
        preceding_nodes = list(self.kg.nodes)[
            :list(self.kg.nodes).index(node_id)]
        preceding_nodes = len(preceding_nodes)

        y = preceding_nodes * Y_INTERVAL
        return x, y

    # TODO: ideally we should probably get rid the knowledgeGraph argument
    def kg_node_to_frontend_adapter(self, node: Dict) -> Dict:
        """
        Adds attributes to nodes for displaying in the front end React UI
        """
        node["node_data"]["color"] = self._get_color(node["id"])
        # node["node_data"]["keywords"] = self._get_keywords(node["id"])

        x, y = self.get_layout_coords(node["id"])
        node["position"] = {
            "x": x,
            "y": y
        }

        # everything else
        if node["id"] in self.targeted_ids:
            # only show ROOT nodes for now
            if node["node_data"]["node_type"] == "ROOT":
                node["hidden"] = False

            node["data"] = node["node_data"]
            del node["node_data"]
            return node
        else:
            # change node to the color of its parent
            if self.show_all:
                node["hidden"] = False

            node["data"] = node["node_data"]
            del node["node_data"]
            return node

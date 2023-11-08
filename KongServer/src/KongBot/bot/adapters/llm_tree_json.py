from src.KongBot.bot.base.types import DataNode, NodeType

from typing import Dict, List


def llm_tree_json_adapter(key, json_data: DataNode) -> Dict | List[Dict]:
    """
    Converts the JSON returned from Tree2FlatJSONQuery into form that can be ingested by KnowledgeGraph
    """
    # realistically this only happens for the root
    if isinstance(json_data, list):
        child_nodes = [DataNode(key, NodeType.TREE_NODE)] * len(json_data)
        for child in child_nodes:
            for child_key, child_value in child.items():
                child["node_data"]["children"].append(
                    llm_tree_json_adapter(child_key, child_value))
        return child_nodes
    else:
        child_node = DataNode(key, NodeType.TREE_NODE)
        try:
            for child_key, child_value in json_data.items():
                child_node["node_data"]["children"].append(
                    llm_tree_json_adapter(child_key, child_value))

        except Exception as e:
            print(json_data)
            print("Key: ", key)
            raise e
        return child_node

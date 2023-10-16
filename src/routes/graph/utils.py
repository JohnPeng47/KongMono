from typing import Dict

def merge_tree_ids(subtree_node, tree_node):
    def find_node_with_value(node: Dict, field, val):
        if node["node_data"][field] == val:
            return node
        for child in node["node_data"]["children"]:
            node = find_node_with_value(child, field, val)
            if node:
                return node
        return None
        
    stack = [subtree_node]
    while stack:
        curr_node = stack.pop()
        print(curr_node)
        curr_id, curr_title = curr_node["id"], curr_node["node_data"]["title"]

        node = find_node_with_value(tree_node, "title", curr_title)
        if node:
            node["id"] = curr_id

        stack.extend(curr_node["node_data"]["children"])
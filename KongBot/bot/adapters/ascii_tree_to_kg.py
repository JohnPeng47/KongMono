import json
import re
import uuid
from typing import Dict
from bot.base.exceptions import GeneratorException

def ascii_tree_to_kg_v2(tree: str, subtree_og: Dict, parent_node: Dict):
    pattern = re.compile(r'\[(\d+)\] (.*)')
    lines = tree.split('\n')
    data = []
    roots = 0

    for line in lines:
        try:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            depth, title = match.groups()
            if int(depth) == 0:
                roots += 1
            data.append((int(depth), title))
            
        except Exception:
            # error = "NO MATCH ERROR: \n"
            # error += "ORIGINAL:\n"
            # error += "\n".join(lines)
            # error += "\n_________________________________ \n"
            # with open("error.txt", "a") as error_file:
            #     error_file.write(error)
            raise GeneratorException("NO MATCH!")
            
    # the case where we have multiple roots and subtree_og has a parent (ie. not the root node)
    if roots > 1 and not parent_node:
        root_id, root_title = parent_node["id"], parent_node["node_data"]["title"]
    else:
        # this effectively handles both case where LLM generated tree starts at 1 or 0
        root_id, root_title = subtree_og["id"], subtree_og["node_data"]["title"]
        start_depth, _ = data[0]
        if start_depth == 0:
            data.pop(0)

        # need to realign depths so they all start at zero because we rely on strict 0-based
        # array indexing to determine depth level
        for i, (depth, title) in enumerate(data):
            # print(depth, title)
            data[i] = (depth - 1, title)
            if depth - 1 < 0:
                # error = "BELOW ZERO: \n"
                # error += "ORIGINAL:\n"
                # error += "\n".join(lines)
                # error += "\n_________________________________ \n"
                # with open("error.txt", "a") as error_file:
                #     error_file.write(error)
                raise GeneratorException("Error index is below zero")


    root_node = {
        "id": root_id, 
        "node_data": {
            "title" : root_title,
            "children" : [],
            "node_type" : "TREE_NODE",
            "description": ""
        }
    }

    level_index = [root_node["node_data"]["children"]]
    for depth, title in data:
        node_id = find_id(subtree_og, title)
        if not node_id:
            node_id = str(uuid.uuid4())

        node = {
            "id": node_id, 
            "node_data": {
                "title" : title,
                "children" : [],
                "node_type" : "TREE_NODE",
                "description": ""
            }
        }
        
        # Add the new node to the appropriate parent's children
        level_index[depth].append(node)

        # Update level_index for potential future children of this node
        # We ensure that `level_index` always contains the right "children" list at the depth index
        if len(level_index) > depth + 1:
            level_index[depth + 1] = node["node_data"]["children"]
        else:
            level_index.append(node["node_data"]["children"])
    
    return root_node

def find_id(node: Dict, title: str):
    if node["node_data"]["title"] == title:
        return node["id"]
    
    for child in node["node_data"]["children"]:
        id = find_id(child, title)
        if id:
            return id
        
    return None


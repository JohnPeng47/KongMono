from uuid import uuid4

def dash_tree_to_json(ascii_tree, context):
    lines = ascii_tree.strip().split("\n")
    root = {
        "id" : str(uuid4()),
        "node_data": {
            "node_type": "ROOT",
            "title": context,
            "children": []
        }
    }

    stack = [(root["node_data"]["children"], -1)]  # Stack of (current_node, indentation level)

    for line in lines:
        if not line:
            continue
        indent = line.count('--')  # Count the number of '-' to determine the level
        remove_index = line.index(">") + 1
        node_type, title = line[remove_index:].split(':')
        node_type = node_type.strip()
        title = title.strip()
        node = {
            "id": str(uuid4()),  # ID to be filled in later
            "node_data": {
                "node_type": node_type.upper(),
                "title": title,
                "children": []
            }
        }

        # Find the right parent level
        while stack and stack[-1][1] >= indent:
            stack.pop()

        # Add the node to the appropriate parent
        parent, _ = stack[-1]
        parent.append(node)

        # Push the current node onto the stack
        stack.append((node["node_data"]["children"], indent))

    return root


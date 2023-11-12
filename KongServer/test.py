import json
from uuid import uuid4

def parse_ascii_tree(ascii_tree):
    lines = ascii_tree.strip().split("\n")
    root = []
    stack = [(root, -1)]  # Stack of (current_node, indentation level)

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

# Example usage
ascii_tree = """
> SECTION: Introduction to the First Mongol Invasion of Europe
  --> PARAGRAPH: Historical Context
      ----> CONTENT: Overview of Mongol Empire before the invasion
      ----> CONTENT: Political and social situation in Europe pre-invasion

  --> PARAGRAPH: Motivations and Objectives
      ----> CONTENT: Genghis Khan's expansion policy
      ----> CONTENT: Strategic and economic goals of the Mongols

> SECTION: Chronology of the Invasion
  --> PARAGRAPH: Initial Incursions
      ----> CONTENT: Mongol tactics and early victories
      ----> CONTENT: European responses and initial clashes

  --> PARAGRAPH: Major Battles and Campaigns
      ----> CONTENT: Siege of Kiev and its impact
      ----> CONTENT: Battles in Eastern Europe
      ----> CONTENT: Mongol strategies and European military reactions

> SECTION: Sociopolitical Impact of the Invasion
  --> PARAGRAPH: Short-term Effects
      ----> CONTENT: Immediate aftermath in affected regions
      ----> CONTENT: Military and political changes in Europe

  --> PARAGRAPH: Long-term Consequences
      ----> CONTENT: Influence on European warfare and defense strategies
      ----> CONTENT: Changes in European perception of the Mongol Empire
      ----> CONTENT: Impact on trade and cultural exchanges

> SECTION: Conclusion
  --> PARAGRAPH: Summarizing the Mongol Invasion
      ----> CONTENT: The invasion's role in shaping Eurasian history
      ----> CONTENT: Legacy and historical interpretations
"""

# Parse the ASCII tree and convert it into JSON
json_structure = parse_ascii_tree(ascii_tree)

# Print the JSON structure
print(json.dumps(json_structure, indent=4))

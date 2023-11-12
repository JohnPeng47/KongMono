GEN_ESSAY_FROM_TREE = """
Given the following context:
{context}

Generate an essay using the following tree as a structural guide
{tree}
"""

GEN_ESSAY_ROOT_TREE = """
Given the following background context, complete the task:
BACKGROUND CONTEXT:
{context}

TASK:
Given the context above, generate a tree diagram that represents the structural component of an essay on the context. 

TREE:
The tree should be generated such that each subsequent lower level features more
topics than the one above it Each sublevel should be ranked in order of
importance to the parent top-level topic
Node Types:
There are going to be 3 different kind of nodes in this tree. 
1. SECTION: indicates a group of paragraphs, under a common theme
2. PARAGRAPH: indicates a paragraph in final essay
3. CONTENT: indicates the content of the paragraph

Output:
Should look like
> SECTION: Introduction to the War of the Orders
--> PARAGRAPH: Background of the Conflict
----> CONTENT: Overview of Roman society pre-conflict
----> CONTENT: Key figures and classes involved
"""

SECTION_EXPANSION_RULE = """
SECTIONS can hold multiple PARAGRAPHS, not recursively
--> SECTION:
----> PARAGRAPH
----> PARAGRAPH
"""

PARAGRAPH_EXPANSION_RULE = """
PARAGRAPHS can hold multiple CONTENT, not recursively
--> PARAGRAPH:
----> CONTENT
----> CONTENT
"""

CONTENT_EXPANSION_RULE = """
Expand the last NODE of the given subtree, by using the following rule for its
expansion:
CONTENT can hold multiple CONTENT, recursively. For example:
--> CONTENT: Mongol tactics
----> CONTENT: Mastery of Cavalry Tactics
------> CONTENT: Superior horse archery techniques
------> CONTENT: Utilization of rapid maneuvering and feigned retreats
----> CONTENT: Siegecraft and Psychological Warfare
"""

SINGLE_NODE_EXPANSION = """
Expand the last NODE of the given subtree, by applying the following expansion rules to respective nodes of that type:
{rule}

Add 3 sublevels to each node type, according to the rules laid out above

The context of the subtree is:
{context}

Subtree:
{subtree}
"""
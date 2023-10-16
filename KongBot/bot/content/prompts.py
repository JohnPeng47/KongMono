GENERATE_TREE_TEXT = """
Given the following text, generate a hierarchal tree representing its contents.
Branches on the same level of the tree should be generated in the order that
they appear in the text.

{text_chunk}

The tree should have these properties: 
1. There must be a single root node. Make sure you do this at the end after you have generated every else.
Prefix it with: ROOT_NODE = ...
2. At each level, the tree nodes should be ranked with the order that they occur in the text 
3. Each child node must be related to the parent node that it is filed under, in a way that makes sense
4. The titles for each tree level should reflect events that might be interesting to the reader
5. Use "-->" to denote an additional level in the tree

For example:
----> George Bissell's role
----> Establishment of the Pennsylvania Rock-Oil Company
----> Analysis of local oil by Professor Benjamin Silliman, Jr.
----> Challenge of finding sizable quantities of petroleum
ROOT_NODE = Birth of the petroleum industry

"""

GENERATE_TREE_JSON = """

"""

TREE_TEXT_SUMMARY = """
The following tree represents a summarization of the accompanying text. 
{tree}
Now, identify the segments in the text that correspond to each node in the tree. Given the following text,
generate a new output each branch in the tree acts as a heading for the relevant text segment.
{text}
Given your response in JSON, where each key represents the topic/subtopic in the tree and the value
is the relevant passage in the text 
"""
from pydantic import BaseModel
from enum import Enum


TREE_CONTEXT = """
You are tasked with writing a science_fiction novel . A prompt will be given, that 
will describe the context for which you will


Given the following background context, :
BACKGROUND CONTEXT:
{context}
    
TASK:
Given the context above, generate a tree diagram focusing on the historical
background leading up to these events. The tree should have these properties: 
- Use "-->" to denote an additional level in the tree
- Each sublevel should be ranked in order of importance to the parent top-level topic
- For each level, there should be 4 sublevels
"""

TREE_PLOT = """
Given the following background context, complete the task:
BACKGROUND CONTEXT:
{context}
    
TASK:
Given the context above, generate a tree diagram focusing on the historical
background leading up to these events. The tree should have these properties: 
- Use "-->" to denote an additional level in the tree
- Each sublevel should be ranked in order of importance to the parent top-level topic
- For each level, there should be 4 sublevels
"""

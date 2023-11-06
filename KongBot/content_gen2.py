import json
from bot.base import KnowledgeGraph
import bot.explorationv2.generators.generators as GENERATORS
# from bot.explorationv2 import generate_tree, generate_sub_trees_v2, generate_subtree_descriptions, generate_entity_relations, \
#     generate_details_hierarchal, generate_keywords
from bot.explorationv2.llm import GenSubTreeQuery, Tree2FlatJSONQuery, GenSubTreeQueryV2

context = """
Generate something about the origin of electronic music. Focus on the history techno
"""
context2 = """
Generate a text about ray peat's views on energy and metabolism
"""
context3 = """
Generate a lesson about effective project management
"""
context4 = """
Generate text that focuses on modern psychology. Focus on:
- psychoanalysis
- cognitive science
"""


russia_context = """
You are a member of the Russian Provisional Government under the faction of the Bolsheviks

The setting is pre-revolution Russia, when the Tsar has just abdicated the throne and the Russian Provisional government has just been
assembled. You are about to engage in parliamentary debates with the other factions to push across your legislative agenda on issue of:
Russia's Participation in the Great War

Create a briefing that will prepare your members for the debate
"""

goal = """
"""

# NOTES:
# Subtree breadth/depth
# - theoretically, a subtree can be arbitrarily deep or wide, but subtrees that are too wide
# might affect generation quality since the number of subtopics to generate for can be too much
config = {
    "global": {
        "nodes": 200,
        # currently only used to control the selection size of subtrees for
        # generation steps, but in future, could also be used to hard cap the
        # the size of the generated subtrees
        "subtree_size": 2
    },
    "generate_tree": {
        "cache_policy": "CACHE",
        "goal": goal,
        "model": "gpt4"
    },
    "generate_short_description": {
        "cache_policy": "default",
        "model": "gpt3",
    },
    "generate_entity_relations": {
        "cache_policy": "default",
        "model": "gpt4",
    },
    "generate_long_description": {
        "cache_policy": "default",
        "model": "gpt4",
    }
}

# contexts = [context, context2, context3, context4]
# ids = []
# for ctx in contexts:
# kg = KnowledgeGraph(russia_context, config=config)
# kg.add_generators([
#     GENERATORS.generate_tree,
#     # GENERATORS.generate_long_description,
#     # GENERATORS.generate_short_description,
#     GENERATORS.generate_entity_relations
# ])
# kg.generate_nodes()

kg = KnowledgeGraph("Russia")
kg.add_node( {
    "id": "1",
    "node_data": {
        "title": "",
        ""
        "children": []
    }
})
print(kg.to_json())
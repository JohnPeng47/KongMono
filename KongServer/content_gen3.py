from src.KongBot.bot.base import KnowledgeGraph
import src.KongBot.bot.explorationv2.generators.generators as GENERATORS
# from src.KongBot.explorationv2 import generate_tree, generate_sub_trees_v2, generate_subtree_descriptions, generate_entity_relations, \
#     generate_details_hierarchal, generate_keywords
from src.KongBot.bot.explorationv2.llm import GenSubTreeQuery, Tree2FlatJSONQuery, GenSubTreeQueryV2
from src.KongBot.bot.adapters import ascii_tree_to_kg
from src.KongBot.bot.essay_gen.generator import generate_tree

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
        "nodes": 100,
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
        "model": "gpt4",
    },
    "generate_entity_relations": {
        "cache_policy": "default",
        "model": "gpt4",
    },
    "generate_long_description": {
        "cache_policy": "default",
        "model": "gpt4",
    },
    "generate_sub_trees": {
        "cache_policy": "default",
        "model": "gpt3",
    },
    "gen_tree_essay" : {
        "model" : "gpt4"
    }
}

# kg = KnowledgeGraph("The first Mongol invasion of Europe")
# kg.add_config(config)
# kg.add_generators([
#     generate_tree,
#     # generate_details_hierarchal
# ])
# kg.generate_nodes()
# print(kg.display_tree())
# # # kg.save_graph()

import json

data = open("test/KongServer/data/data.json", 'r')
data = json.loads(data.read())
kg = KnowledgeGraph("Attaturk and the origins of the modern Turkish State")
kg.from_json(data)
print(kg.display_tree("cc2f7a97-bb67-4a88-90f3-358e843f426c", lineage=True))
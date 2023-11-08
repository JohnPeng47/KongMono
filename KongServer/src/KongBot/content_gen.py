from src.KongBot.explorationv2.llm import Tree2FlatJSONQuery
import json
from src.KongBot.bot.base import KnowledgeGraph
from src.KongBot.explorationv2 import generate_tree, generate_sub_trees, generate_subtree_descriptions, generate_entity_relations, generate_long_details

context = """
You are a member of the Russian Provisional Government under the faction of the Bolsheviks

The setting is pre-revolution Russia, when the Tsar has just abdicated the throne and the Russian Provisional government has just been
assembled. You are about to engage in parliamentary debates with the other factions to push across your legislative agenda on issue of:
Russia's Participation in the Great War

Create a briefing that will prepare your members for the debate
"""

goal = """
"""

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

config = {
    "global": {
        "nodes": 20,
        "subtree_size": 3
    },
    "generate_tree": {
        "cache_policy": "default",
        "goal": goal,
        "model": "gpt3"
    },
    "generate_tree_details": {
        "cache_policy": "CACHE",
        "depth": 1,
        "model": "gpt4"
    },
    "generate_sub_trees": {
        "cache_policy": "CACHE",
        "depth": 1,
        "model": "gpt3"
    },
    "generate_detailed_descriptions": {
        "cache_policy": "default",
        "model": "gpt3",
        "num_children": 2
    },
    "generate_entity_relations": {
        "cache_policy": "default",
        "model": "gpt3",
        "num_children": 2
    },
    "generate_details_hierarchal": {
        "cache_policy": "default",
        "model": "gpt3",
        "num_children": 2
    }
}

# # for ctxt in [context, context2, context3, context4]:
kg = KnowledgeGraph.load_graph("63ac2243-d204-4c3e-aa0f-e9265afdf1b9")
kg.add_config(config)
kg.add_generators([
    generate_tree,
    generate_sub_trees,
    # generate_details_hierarchal
    # generate_entity_relations
    # generate_details_hierarchal
])
kg.generate_nodes()
print(kg.display_tree())

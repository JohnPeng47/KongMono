import json
from bot.base import KnowledgeGraph
from bot.explorationv2 import generate_tree, generate_sub_trees, generate_subtree_descriptions, generate_entity_relations, \
    generate_details_hierarchal
from bot.explorationv2.llm import GenSubTreeQuery, Tree2FlatJSONQuery, GenSubTreeQueryV2
from bot.adapters import ascii_tree_to_kg, ascii_tree_to_kg_v2

context = """
Generate something about the origin of electronic music. Focus on the history techno
"""
# context2 = """
# Generate a text about ray peat's views on energy and metabolism
# """
# context3 = """
# Generate a lesson about effective project management
# """
# context4 = """
# Generate text that focuses on modern psychology. Focus on:
# - psychoanalysis
# - cognitive science
# """


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
        "nodes": 120,
        # currently only used to control the selection size of subtrees for
        # generation steps, but in future, could also be used to hard cap the
        # the size of the generated subtrees
        "subtree_size": 2
    },
    "generate_tree": {
        "cache_policy": "default",
        "goal": goal,
        "model": "gpt4"
    },
    "generate_tree_details": {
        "cache_policy": "CACHE",
        "depth": 1,
        "model": "gpt4"
    },
    "generate_sub_trees": {
        "cache_policy": "default",
        "depth": 1,
        "model": "gpt4"
    },
    "generate_subtree_descriptions": {
        "cache_policy": "default",
        "model": "gpt4",
    },
    "generate_entity_relations": {
        "cache_policy": "default",
        "model": "gpt4",
    },
    "generate_details_hierarchal":{
        "cache_policy": "default",
        "model": "gpt4",
    }
}

# contexts = [context, context2, context3]
# for ctx in contexts:

# kg = KnowledgeGraph(russia_context, config=config)
# kg.add_generators([
#     # TODO: look into issue again root tree is throwing
#     # away nodes
#     generate_tree,
#     generate_sub_trees,
#     # generate_subtree_descriptions,
#     # generate_entity_relations,
#     generate_details_hierarchal
# ])
# kg.generate_nodes()
# kg.save_graph()
# print(kg.display_tree())


# kg = KnowledgeGraph.load_graph("e45cd912-37a7-4eb4-9c72-c24345f07f2f")
# print(kg.display_tree())
# print(kg.display_tree_v2_lineage())
# node_id = kg.filter_nodes({"title" : "Public disillusionment with monarchy"})[0]["id"]
# tree_parents, tree_tree = kg.display_tree_v2_lineage(node_id)
# print(tree_parents, tree_tree)


kg = KnowledgeGraph.load_graph("f110ccd3-3dcc-4078-be35-dff094494a90")
kg.add_config(config)
kg.add_generators([
    generate_details_hierarchal
])
kg.generate_nodes()
print(json.dumps(kg.to_json(), indent=4))
from ..llm import GenSubTreeQuery, Tree2FlatJSONQuery, SubtreeSingleLineDescJSONQuery, \
    GenTreeQuery, GenTreeQueryV2, SubtreeDescriptionMultiQuery, GenEntityRelationsJSONQuery, \
    GenDetailedDecrSubtreeQuery, GenExpandedTextDescription, GenSubTreeQueryV2, GenerateKeywords

from networkx.algorithms.traversal.depth_first_search import dfs_tree
from bot.base import KnowledgeGraph
from .utils import convert_tree_to_json
from typing import Dict, List

from bot.adapters.ascii_tree_to_kg import ascii_tree_to_kg_v2
import random


import logging

logger = logging.getLogger("base")

# we will modify this later
# going to have a recursive generation model that is going to be controlled
# from generate_nodes method from KG


# TODO: to make this comply with the GeneratorArg interface, first add a root node
# use that as the GeneratorArg into the graph
def generate_treev2(graph: KnowledgeGraph):
    config: Dict = graph.config["generate_treev2"]
    cache_policy = config.get("cache_policy", "default")
    goal = config.get("goal", "")
    model = config.get("model", "gpt4")

    tree_query = GenTreeQueryV2(graph.curriculum,
                                goal=goal,
                                cache_policy=cache_policy,
                                model=model)
    tree: str = tree_query.get_llm_output()
    tree_json_query = Tree2FlatJSONQuery(tree,
                                         cache_policy=cache_policy,
                                         model=model)
    tree_json: Dict = tree_json_query.get_llm_output()

    graph.update_call_costs(tree_query.get_llm_call_costs())
    graph.update_call_costs(tree_json_query.get_llm_call_costs())

    print("Tree JSON: ", tree_json)
    graph.from_json(tree_json)
    print(graph.display_tree())

### REFACTORED GENERATORS
# TODO:
# Consider: moving the config interface out to BaseLLMQuery
from bot.base.types import GeneratorArg, GeneratorResult
def generate_tree(graph: KnowledgeGraph):
    config: Dict = graph.config["generate_tree"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")

    tree_query = GenTreeQuery(graph.curriculum,
                              cache_policy=cache_policy,
                              model=model)
    tree: str = tree_query.get_llm_output()

    # tree_json_query = Tree2FlatJSONQuery(tree,
    #                                cache_policy=cache_policy,
    #                                model=model)
    # tree_json: Dict = tree_json_query.get_llm_output()

    tree_json = convert_tree_to_json(tree, cache_policy, model)
    # TODO: move cost updates to inside BaseLLMQuery
    # graph.update_call_costs(tree_query.get_llm_call_costs())
    # graph.update_call_costs(tree_json_query.get_llm_call_costs())
    graph.from_json(tree_json)

def generate_sub_trees(graph: KnowledgeGraph):
    global_config: Dict = graph.config["global"]
    config: Dict = graph.config["generate_sub_trees"]
    model = config.get("model", "gpt4")

    cache_policy = config.get("cache_policy", "default")
    target_num_nodes = global_config["nodes"]
    depth = config.get("depth", graph.max_depth() - 1)

    curr_num_nodes = graph.stats()["num_nodes"]
    curr_depth_nodes = [node for node in graph.get_nodes_from_depth(depth)]

    while curr_num_nodes < target_num_nodes:
        if not curr_depth_nodes:
            # update depth to move one down
            depth = graph.max_depth() - 1
            curr_depth_nodes = [node for node in graph.get_nodes_from_depth(depth)]

        node_index = random.randint(0, len(curr_depth_nodes) - 1)
        subtree_root = curr_depth_nodes.pop(node_index)
        subtree_id = subtree_root["id"]
        subtree = graph.display_tree(subtree_id)
        subtree = GenSubTreeQueryV2(graph.curriculum,
                                  subtree,
                                  cache_policy=cache_policy,
                                  model=model).get_llm_output()
        
        # if no parent, means we are the root of the tree
        parent = graph.parents(subtree_id)[0] if graph.parents(subtree_id) else subtree_root
        retry = 3
        while retry > 0:
            try:
                subtree_node_new = ascii_tree_to_kg_v2(subtree, subtree_root, parent)
                break
            except Exception as e:
                retry -= 1
                logger.error("Generate subtree exception: ", e)
                logger.error("Retrying...")
                continue

        graph.add_node(subtree_node_new, merge=True)
        print(
            f"#Nodes before: {curr_num_nodes}, #Num nodes now: {graph.stats()['num_nodes']}")
        curr_num_nodes = graph.stats()["num_nodes"]


def generate_long_description(graph: KnowledgeGraph):
    global_config = graph.config["global"]
    subtree_size = global_config["subtree_size"]

    config: Dict = graph.config["generate_long_description"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")

    mt_input_args = [
        GeneratorArg(
            node_id = node_id, 
            data = {
                "subtree": graph.display_tree(node_id, lineage=True, stop_depth=subtree_size)
            }
        ) for node_id in list(graph.nodes)
        if not graph.get_node(node_id)["node_data"].get("long_description")
    ]

    logger.debug(f"Generating {len(mt_input_args)} short descriptions")
    
    nodes_details_query = GenExpandedTextDescription.mt_init(cache_policy=cache_policy, model=model)
    results: List[GeneratorResult] = nodes_details_query.mt_get_llm_output(mt_input_args)
    
    # this should probably be a return
    for res in results:
        node_id = res.node_id
        description = res.data
        graph.modify_node(node_id, {
                            "long_description": description})

def generate_short_description(graph: KnowledgeGraph):
    global_config = graph.config["global"]
    subtree_size = global_config["subtree_size"]

    config: Dict = graph.config["generate_short_description"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")
    
    mt_input_args = [
        GeneratorArg(
            node_id = node_id,
            data = {
                    "subtree": graph.display_tree(node_id, lineage=True, stop_depth=subtree_size),
                }
        ) for node_id in list(graph.nodes)
        if not graph.get_node(node_id)["node_data"].get("description")
    ]    

    nodes_details_query = GenDetailedDecrSubtreeQuery.mt_init(cache_policy=cache_policy,
                                                              model=model)

    results: List[GeneratorResult] = nodes_details_query.mt_get_llm_output(mt_input_args)

    for res in results:
        node_id = res.node_id
        description = res.data
        graph.modify_node(node_id, {
                            "description": description})

def generate_entity_relations(graph: KnowledgeGraph):
    global_config = graph.config["global"]
    subtree_size = global_config["subtree_size"]

    config: Dict = graph.config["generate_entity_relations"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")

    mt_input_args = [
        GeneratorArg(
            node_id = node_id, 
            data = {
                "text": graph.get_node(node_id)["node_data"]["description"],
                # we are filtering for the
            }
        ) for node_id in list(graph.nodes)
        if graph.get_node(node_id)["node_data"].get("description")
    ]

    entity_relations_query = GenEntityRelationsJSONQuery.mt_init(cache_policy=cache_policy,
                                                                 model=model)

    results = entity_relations_query.mt_get_llm_output(mt_input_args)

    for node_id, entity_relation_json in results:
        graph.modify_node(node_id, {"entity_relations": entity_relation_json})


# def generate_keywords(graph: KnowledgeGraph):
#     mt_input_args = [
#         GeneratorArg(     
#             node_id = node_id, 
#             data = {
#                 "long_description": graph.get_node(node_id)["node_data"]["long_description"]
#             }
#         ) for node_id in list(graph.nodes)[:1] if graph.get_node(node_id)["node_data"].get("long_description")
#     ]

#     keywords_query = GenerateKeywords.mt_init()
#     results: List[GeneratorResult] = keywords_query.mt_get_llm_output(mt_input_args)

#     for res in results:
#         node_id = res.node_id
#         keywords = res.data
#         print("Keywords: ", keywords)
#         graph.modify_node(node_id, {
#                             "keywords": description})
        


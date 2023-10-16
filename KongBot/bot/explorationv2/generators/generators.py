from ..llm import GenSubTreeQuery, Tree2FlatJSONQuery, SubtreeSingleLineDescJSONQuery, \
    GenTreeQuery, GenTreeQueryV2, SubtreeDescriptionMultiQuery, GenEntityRelationsJSONQuery, \
    GenDetailedDecrSubtreeQuery

from bot.base import KnowledgeGraph
from .utils import convert_tree_to_json
from typing import Dict, List

import logging

logger = logging.getLogger("logger")

# we will modify this later
# going to have a recursive generation model that is going to be controlled
# from generate_nodes method from KG


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
    # print(graph.display_tree())

# we will modify this later
# going to have a recursive generation model that is going to be controlled
# from generate_nodes method from KG


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


def generate_tree_details(graph: KnowledgeGraph):
    config: Dict = graph.config["generate_tree_details"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")

    tree = graph.display_tree()
    node_details_query = SubtreeSingleLineDescJSONQuery(tree,
                                                        cache_policy=cache_policy,
                                                        model=model)
    node_details: Dict = node_details_query.get_llm_output()
    graph.update_call_costs(node_details_query.get_llm_call_costs())

    for node_title, generated_desc in node_details.items():
        try:
            target_node = graph.filter_nodes_single({"title": node_title})
            target_id = target_node["id"]

            graph.modify_node(target_id, {"description": generated_desc})
        except:
            continue

# merge ids
def merge_tree_ids(subtree_node, tree_node):
    def find_node_with_value(node: Dict, field, val):
        if node["node_data"][field] == val:
            return node
        for child in node["node_data"]["children"]:
            node = find_node_with_value(child, field, val)
            if node:
                return node
        return None
        
    stack = [subtree_node]
    while stack:
        curr_node = stack.pop()
        print(curr_node)
        curr_id, curr_title = curr_node["id"], curr_node["node_data"]["title"]

        node = find_node_with_value(tree_node, "title", curr_title)
        if node:
            node["id"] = curr_id

        stack.extend(curr_node["node_data"]["children"])
        
# TODO: make a multithreaded version of this to generate nodes in parallel
# but to do so, we need to modify prompt to accept number of nodes to generate
# so we dont overshoot the config
def generate_sub_trees(graph: KnowledgeGraph):
    global_config: Dict = graph.config["global"]
    config: Dict = graph.config["generate_sub_trees"]
    model = config.get("model", "gpt4")

    cache_policy = config.get("cache_policy", "default")
    target_num_nodes = global_config["nodes"]
    depth = config.get("depth", graph.max_depth() - 1)

    curr_num_nodes = graph.stats()["num_nodes"]

    # generate subtrees for all nodes at the same depth first
    # before updating max_depth aka. breadth first vs. depth first
    # NOTE: it still is uneven because initial generation is uneven
    # possibly could enforce this constraints during tree generation phase
    # but also, maybe preferrable to let GPT do its thing
    curr_depth_nodes = (graph.get_nodes_from_depth(depth))

    print("Before: ", graph.display_tree())

    while curr_num_nodes < target_num_nodes:
        if not curr_depth_nodes:
            depth = graph.max_depth() - 1
            curr_depth_nodes = (graph.get_nodes_from_depth(depth))

        # node_index = random.randint(0, len(curr_depth_nodes) - 1)
        node_index = 0

        subtree_root = curr_depth_nodes.pop(node_index)
        subtree_id = subtree_root["id"]

        subtree_node = graph.get_node(subtree_id)
        subtree = graph.display_tree(subtree_id)

        subtree = GenSubTreeQuery(graph.curriculum,
                                  subtree,
                                  cache_policy=cache_policy,
                                  model=model).get_llm_output()

        # TODO: need to make all of JSON query LLM implement the same DataNode interface
        # so we can just add one without running the other to graph
        # TODO: need to use DataNode more
        new_subtree_node = Tree2FlatJSONQuery(subtree,
                                          cache_policy=cache_policy,
                                          model=model).get_llm_output()
        
        # need this to match titles to ids in the newly generated subtree
        merge_tree_ids(subtree_node, new_subtree_node)
        graph.add_node(new_subtree_node, merge=True)

        # subtree_detailed = GenDetailedDescriptionJSONQuery(subtree,
        #                                                    cache_policy=cache_policy,
        #                                                    model=model).get_llm_output()
        # for node_title, generated_desc in subtree_detailed.items():
        #     try:
        #         target_node = graph.filter_nodes_single({"title": node_title})
        #         target_id = target_node["id"]

        #         graph.modify_node(target_id, {"description": generated_desc})
        #     except:
        #         continue

        print(
            f"#Nodes before: {curr_num_nodes}, #Num nodes now: {graph.stats()['num_nodes']}")
        curr_num_nodes = graph.stats()["num_nodes"]

                

# FOr now we are only targetting subtrees with two or more children
def generate_subtree_descriptions(graph: KnowledgeGraph):
    """
    Only generates descriptions for nodes with subtree_size
    """
    global_config = graph.config["global"]
    subtree_size = global_config.get("subtree_size", 2)

    config: Dict = graph.config["generate_subtree_descriptions"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")

    node_ids = [node["id"]
                for node in graph.filter_nodes({"children": subtree_size})]
    subtrees = [
        graph.display_tree(node_id, stop_depth=2, lineage=True) for node_id in node_ids
    ]

    for subtree in subtrees:
        print(subtree)

    mt_input_args = {
        node_id: {
            "subtree": subtree,
        } for node_id, subtree in zip(
            node_ids,
            subtrees
        )
    }

    node_details_query = SubtreeDescriptionMultiQuery(subtrees[0],
                                                      cache_policy=cache_policy,
                                                      model=model)
    results = node_details_query.mt_get_llm_output(mt_input_args)

    for node_id, description in results:
        print("DESCRIPTION: ", description)
        graph.modify_node(node_id, {"description": description})

    print(graph.__str__())


def generate_entity_relations(graph: KnowledgeGraph):
    global_config = graph.config["global"]
    subtree_size = global_config["subtree_size"]

    config: Dict = graph.config["generate_entity_relations"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")

    mt_input_args = {
        node["id"]: {
            "text": node["node_data"]["description"],
            # we are filtering for the
        } for node in graph.filter_nodes({"children": subtree_size})
    }

    entity_relations_query = GenEntityRelationsJSONQuery.mt_init(cache_policy=cache_policy,
                                                                 model=model)

    results = entity_relations_query.mt_get_llm_output(mt_input_args)

    for node_id, entity_relation_json in results:
        graph.modify_node(node_id, {"entity_relations": entity_relation_json})


def generate_details_hierarchal(graph: KnowledgeGraph):
    global_config = graph.config["global"]
    subtree_size = global_config["subtree_size"]

    config: Dict = graph.config["generate_entity_relations"]
    cache_policy = config.get("cache_policy", "default")
    model = config.get("model", "gpt4")

    # TODO: should probably make this more robust ie. changing the type of node
    # to type: PARENT_NODE or something
    mt_input_args = {
        node["id"]: {
            "subtree": graph.display_tree(node["id"], lineage=True, stop_depth=2),
        } for node in graph.filter_nodes({"children": subtree_size})
    }

    nodes_details_query = GenDetailedDecrSubtreeQuery.mt_init(cache_policy=cache_policy,
                                                              model=model)

    results = nodes_details_query.mt_get_llm_output(mt_input_args)

    for node_id, details in results:
        for title, detailed_description in details.items():
            print("Title: ", title, "\nDetailed description: ",
                  detailed_description)
            target_node = graph.filter_nodes({"title": title})
            if target_node:
                target_node = target_node[0]
                # ids are different here
                print("Modifying node_id: ",
                      target_node["id"], detailed_description)
                graph.modify_node(target_node["id"], {
                                  "description": detailed_description})
                print(graph.__str__())

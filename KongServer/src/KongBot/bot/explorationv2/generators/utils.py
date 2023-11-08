from ..llm import Tree2FlatJSONQuery, AddRootToJSON

from src.KongBot.bot.base import KnowledgeGraph

from typing import Dict
import json


def convert_tree_to_json(tree, cache_policy, model):
    tree_json = Tree2FlatJSONQuery(tree,
                                   cache_policy=cache_policy,
                                   model=model).get_llm_output()

    if not isinstance(tree_json, list):
        return tree_json

    tree_root_json = AddRootToJSON(tree_json,
                                   cache_policy=cache_policy,
                                   model=model).get_llm_output()
    return tree_root_json

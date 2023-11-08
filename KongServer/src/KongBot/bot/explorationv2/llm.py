from ..base import BaseLLM

from typing import Dict

from .prompts import CONVERT_TO_JSON, ADD_ROOT_TO_JSON, TREE, TREE_V2, \
    SUBTREE, SUBTREE_DESCRIPTION_MULTI, SUBTREE_DESCRIPTION_SINGLE, ENTITY_RELATIONS, \
    SUBTREE_DETAILED_DESCRIPTION, SUBTREE_DETAILED_DESCRIPTION_SCHEMA, SUBTREE_V2, SUBTREE_DETAILED_TEXTBOOK_SINGLE, \
    KEYWORD_EXTRACTION, SUBTREE_DETAILED_DESCRIPTION_SINGLE_V1

from src.KongBot.bot.adapters import llm_tree_json_adapter
from src.KongBot.bot.base.query import BaseLLMQuery, BaseLLMQueryV2

import json
import logging


class GenTreeQuery(BaseLLMQuery):
    def __init__(self, context: str, cache_policy: str = "default", model: str = "gpt4"):
        print("INitlaiizng tree with cache_pouc", cache_policy)
        super().__init__(cache_policy=cache_policy, model=model)
        super().init_prompt(TREE, context=context)


class GenTreeQueryV2(BaseLLMQuery):
    def __init__(self, context: str, goal: str, cache_policy: str = "default", model: str = "gpt4"):
        super().__init__(cache_policy=cache_policy, model=model)
        super().init_prompt(TREE_V2, context=context, goal=goal)

    # def get_llm_output(self):
    #     return "hey kratos"


class GenSubTreeQuery(BaseLLMQuery):
    def __init__(self, context: str, subtree: str, cache_policy: str = "default", model: str = "gpt4"):
        super().__init__(cache_policy=cache_policy, model=model)
        super().init_prompt(SUBTREE, context=context, subtree=subtree)


class GenSubTreeQueryV2(BaseLLMQuery):
    def __init__(self,
                 context: str, subtree: str, cache_policy: str = "default", model: str = "gpt4"):

        super().__init__(cache_policy=cache_policy, model=model)
        super().init_prompt(SUBTREE_V2, context=context, subtree=subtree)


class Tree2FlatJSONQuery(BaseLLMQuery):
    """
    Generate a flat JSON structure from a tree and its children. 
    """

    def __init__(self, tree: str, cache_policy: str = "default", model: str = "gpt3"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=True)
        super().init_prompt(CONVERT_TO_JSON, tree=tree)

    def get_llm_output(self):
        query_json: Dict = super().get_llm_output()
        # logger.debug("JSON output from LLM: " + json.dumps(query_json, indent=4))

        root_key = list(query_json.keys())[0]
        return llm_tree_json_adapter(root_key, query_json[root_key])

    # never want this to be cached
    def key(self):
        import random
        return random.randint(0, 10000000)


class AddRootToJSON(BaseLLMQuery):
    """
    Several tree nodes without any parents, add a common parent based on their content
    """

    def __init__(self, tree: str, cache_policy: str = "default", model: str = "gpt3"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=True)
        super().init_prompt(ADD_ROOT_TO_JSON, tree=tree)


class SubtreeSingleLineDescJSONQuery(BaseLLMQuery):
    """
    Given a subtree, generates a short description for each of its children
    """

    def __init__(self, tree: str, cache_policy: str = "default", model: str = "gpt3"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=True)
        super().init_prompt(SUBTREE_DESCRIPTION_SINGLE, tree=tree)


class SubtreeDescriptionMultiQuery(BaseLLMQuery):
    """
    Given a subtree, generates a long formed detailed description about the subtree
    """

    def __init__(self,
                 subtree: str,
                 cache_policy: str = "default",
                 model: str = "gpt3"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=False)
        super().init_prompt(SUBTREE_DESCRIPTION_MULTI, subtree=subtree)


class GenEntityRelationsJSONQuery(BaseLLMQueryV2):
    """
    Generate a entity relations JSON graph from a long detailed subtree description
    """

    def __init__(self,
                 description: str,
                 cache_policy: str = "default",
                 model: str = "gpt3"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=True)
        super().init_prompt(ENTITY_RELATIONS, text=description)

# Idea: we can take a related prompt (as determined by shared entities in the ER graph) and
# use a single prompt to generate a detailed description of their connection
# This would allows us to use the shared context


class GenDetailedDecrSubtreeQuery(BaseLLMQueryV2):
    """
    Generates a detailed description that takes a subtree and generates a full text
    description for it
    """

    def __init__(self,
                 subtree: str,
                 cache_policy: str = "default",
                 model: str = "gpt4"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=False)
        super().init_prompt(SUBTREE_DETAILED_DESCRIPTION_SINGLE_V1, subtree=subtree)


class GenExpandedTextDescription(BaseLLMQueryV2):
    """
    Generates a long textbook level explanation
    """

    def __init__(self,
                 subtree: str,
                 cache_policy: str = "default",
                 model: str = "gpt4"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=False)
        super().init_prompt(SUBTREE_DETAILED_TEXTBOOK_SINGLE, subtree=subtree)


class GenerateKeywords(BaseLLMQueryV2):
    """
    Generate keywords from long text description
    """

    def __init__(self,
                 long_description: str,
                 cache_policy: str = "default",
                 model: str = "gpt4"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=False)
        super().init_prompt(KEYWORD_EXTRACTION, long_description=long_description)

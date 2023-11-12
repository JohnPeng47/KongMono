from src.KongBot.bot.base.query import BaseLLMQueryV2
from .prompts import *

class GenTree(BaseLLMQueryV2):
    """
    Generate a tree from the context
    """
    def __init__(self, 
                 context: str,                  
                 model: str = "gpt3",
                 cache_policy: str = "default",
                 json_output: bool = False,
                 evaluate: bool = True):
        super().__init__(json_output=False)
        super().init_prompt(GEN_ESSAY_ROOT_TREE, context=context)

class GenEssayFromTree(BaseLLMQueryV2):
    """
    Generate an essay from the tree outline
    """
    def __init__(self,
                 context: str,
                 tree: str,
                 cache_policy: str = "default",
                 model: str = "gpt4"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=False)
        super().init_prompt(GEN_ESSAY_FROM_TREE, context=context, tree=tree)

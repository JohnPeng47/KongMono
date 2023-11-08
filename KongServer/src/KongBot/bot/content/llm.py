from src.KongBot.bot.base.query import BaseLLMQuery
from .prompts import GENERATE_TREE_TEXT


class GenerateTrees(BaseLLMQuery):
    """
    Generate a tree for a chunk of text
    """

    def __init__(self, text_chunk: str, cache_policy: str = "default", model="gpt4"):
        super().__init__(cache_policy=cache_policy, model=model, json_output=False)
        super().init_prompt(GENERATE_TREE_TEXT, text_chunk=text_chunk)

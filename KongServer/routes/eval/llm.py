from typing import List

from KongBot.bot.base.query import BaseLLMQueryV2

from .prompts import EVAL_QUESTIONS_MC

class GenEvalQuestionMC(BaseLLMQueryV2):
    """
    Generates a multiple choice question
    """
    def __init__(self,
                 topics: List[str],
                 config: dict):
        super().__init__(**config)
        super().init_prompt(EVAL_QUESTIONS_MC, topics=topics)

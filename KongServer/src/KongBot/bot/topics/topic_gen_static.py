from src.KongBot.bot.base import BaseLLM
from src.KongBot.utils import logger

from src.KongBot.models.models import openai_model, browser_model
from langchain import LLMChain, PromptTemplate
from .prompts.prompts import ITERATIVELY_GENERATE_TOPICS


class TopicGeneratorStatic(BaseLLM):
    def __init__(self, topics="", model="openai"):
        self.set_args({"topics": topics})

        prompt = PromptTemplate(
            template=ITERATIVELY_GENERATE_TOPICS,
            input_variables=["topics"]
        )

        self.llm = LLMChain(
            prompt=prompt,
            llm=openai_model if model == "browser" else browser_model
        )

    def _parse(self, text: str):
        try:
            super()._parse(text)
        except:
            logger.error("Error, expected JSON but got the following:")
            logger.info(text)

from .topic_generation import BaseTopicGenerator
from langchain import LLMChain, PromptTemplate, OpenAI
from src.KongBot.models.models.browserGPT.BrowserGPTLLM import BrowserGPTLLM
import time
import random
import re
from typing import List, Dict

from prompts.topic_generation import ENTITY_EXTRACTOR
from src.KongBot.models.models import openai_model, browser_model


class EntityExtractor(BaseTopicGenerator):
    def __init__(self, model="openai"):
        self.module_type = "ENTITY_EXTRACTOR"

        self.topic_descriptions = []

        self.args_required = True

        prompt = PromptTemplate(
            template=ENTITY_EXTRACTOR,
            input_variables=["text"]
        )

        self.llm = LLMChain(
            prompt=prompt,
            llm=openai_model if model == "openai" else browser_model
        )

    def parse(self, text: str):
        pattern = r"ENTITY: (.*?)</ENTITY>"
        matches = re.findall(pattern, text)

        return matches

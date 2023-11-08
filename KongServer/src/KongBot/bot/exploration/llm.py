
from ..base import BaseLLM

from .prompts import INITIAL_EXPLORATORY_CONCEPTS, GENERATE_TOPICS, GENERATE_SECTIONS, \
    GENERATE_EXPAND
from .schema import GENERATE_SECTION_SCHEMA, EXPAND_TEXT_SCHEMA, EXPAND_SUBTREE_DETAILS

from src.KongBot.utils.helper import double_encode_json


class ConceptsLLMQuery(BaseLLM):
    def __init__(self, curriculum: str, model="openai"):
        self.curriculum = curriculum

        super().__init__(INITIAL_EXPLORATORY_CONCEPTS, curriculum=curriculum)


class TopicsLLMQuery(BaseLLM):
    def __init__(self, curriculum: str, concept: str, description: str, number: int = 4, model: str = "gpt3"):
        self.curriculum = curriculum
        self.concept = concept

        super().__init__(GENERATE_TOPICS, curriculum=curriculum,
                         description=description, concept=concept, num=number, model=model)

    def key(self):
        return self.curriculum[:15] + "_topics" + self.concept[:10]


class SectionsLLMQuery(BaseLLM):
    def __init__(self, topic: str, description: str, number: int = 4):
        self.topic = topic
        self.description = description
        self.set_schema(GENERATE_SECTION_SCHEMA)
        encoded_schema = double_encode_json(GENERATE_SECTION_SCHEMA)

        super().__init__(GENERATE_SECTIONS, topic=topic,
                         description=description, schema=encoded_schema, num=number)

    def key(self):
        return self.topic[:15] + "_sections" + self.description[:15]


class ExpandLLMQuery(BaseLLM):
    def __init__(self, curriculum: str, section: str, number: int = 4):
        self.curriculum = curriculum
        self.section = section
        self.set_schema(EXPAND_TEXT_SCHEMA)
        encoded_schema = double_encode_json(EXPAND_TEXT_SCHEMA)

        super().__init__(GENERATE_EXPAND, curriculum=curriculum,
                         section=section, schema=encoded_schema, num=number)

    def key(self):
        return self.curriculum[:15] + "_expansion" + self.section[:15]


# class TopicsLLMQuery(BaseLLM):
#     def __init__(self, curriculum: str, text: str, model="openai"):
#         self.curriculum = curriculum
#         self.text = text

#         super().__init__(ENTITY_EXTRACTOR, curriculum=curriculum, text=text)

#     def key(self):
#         return self.curriculum + "_" + self.text[:15]

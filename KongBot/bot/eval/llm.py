from bot.base import BaseLLM
from .prompt import CIVCS_LESSON_DESCRIPTION, COMPARE_NODE_ARISTOTLE_TEXT

class GenerateCurriculumQuery(BaseLLM):
    def __init__(self, model="gpt3"):
        super().__init__(CIVCS_LESSON_DESCRIPTION, num_lessons=1, model=model)

class NodeComparisonAristotleQuery(BaseLLM):
    def __init__(self, topic1: str = "", topic2:str = "", model="gpt3"):
        super().__init__(COMPARE_NODE_ARISTOTLE_TEXT, topic1=topic1, topic2=topic2, model=model, json=False)
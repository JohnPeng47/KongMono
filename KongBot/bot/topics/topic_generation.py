from langchain import LLMChain, PromptTemplate, OpenAI
from models.browserGPT.BrowserGPTLLM import BrowserGPTLLM
import time
import random
from typing import List, Dict

from .prompts.prompts import TOPIC_GEN_START, TOPIC_GEN_CONTINUATION
from models import openai_model, browser_model

from logging import Logger
from utils import logger

# TODO: refactor this to make it better lol
class BaseTopicGenerator:
    # the type ofmodule
    module_type = ""
    # arguments check
    args_required: bool = False
    # llmchain: openAI or BrowserGPT
    llm: LLMChain
    # list of topic and descriptions
    topic_descriptions: List[Dict[str, str]] = []
    # list of args to pass to the Langchain PromptTemplate
    prompt_args: Dict = {}
    
    selected_topic: Dict[str, str] = {}

    # time for generating the LLM response
    time: float

    # # write the logger method to log the:
    # # 1. parent topic
    # # 2. generated topic
    # # 3. selected topic
    log: Logger = logger

    def timing_decorator(func):
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            self.time = execution_time  # Update self.time with the execution time
            # print("Function '{}' executed in {:.2f} seconds.".format(func.__name__, execution_time))
            return result
        return wrapper

    def parse(self, text: str):
        start_keyword = "TOPIC:"
        end_keyword = "DESCRIPTION:"

        topic_descriptions = []

        # Find the first occurrence of the start keyword and the occurence of the next one
        start_index = text.find(start_keyword)
        next_start_index = text.find(start_keyword, start_index + len(start_keyword))
        while start_index != -1:
            # Find the index of the end keyword after the start index
            end_index = text.find(end_keyword, start_index)

            if end_index == -1:
                break  # End keyword not found, exit the loop

            # Extract the topic and description text
            topic = text[start_index + len(start_keyword):end_index].strip()
            description = text[end_index + len(end_keyword): next_start_index].strip()

            topic_descriptions.append({
                "topic" : topic, 
                "description": description}
            )  # Add to the list

            # Find the next occurrence of the start keyword
            start_index = text.find(start_keyword, end_index)
            next_start_index = text.find(start_keyword, start_index + len(start_keyword))

        return topic_descriptions
    
    def get_module_type(self):
        return self.module_type

    def get_random_topic(self):
        for i, topic in enumerate(self.topic_descriptions):
            logger.info(str(i + 1) + ") Topic" + ":" + topic["topic"])
            logger.info("Description" + ":" + topic["description"])

        rand_indx = random.randint(0, len(self.topic_descriptions) - 1)
        logger.okay("Chosen topic: " + self.topic_descriptions[rand_indx]["topic"])
        return self.topic_descriptions[rand_indx]
    
    def choose_topic(self):
        for i, topic in enumerate(self.topic_descriptions):
            logger.info(str(i + 1) + ") Topic" + ":" + topic["topic"])
            logger.info("Description" + ":" + topic["description"])

        input_str = input("Choose a topic: ")
        chosen_indx = int(input_str) - 1
        if chosen_indx > len(self.topic_descriptions):
            raise Exception("Topic index out of range")
        
        logger.okay("Chosen topic: " + self.topic_descriptions[chosen_indx]["topic"])
        return self.topic_descriptions[chosen_indx - 1]
    
    def set_args(self, args):
        self.prompt_args = args
        
    def get_llm_output(self):
        if (self.args_required and self.prompt_args == {}):
            raise Exception("Arguments required for this topic generator")
        
        llm_response = self.llm.run(self.prompt_args)
        self.topic_descriptions = self.parse(llm_response)
        return self.topic_descriptions
    
class TopicGenerator(BaseTopicGenerator):
    def __init__(self, model="openai"):
        self.id = int(time.time())

        self.module_type = "TOPIC_GENERATOR"

        self.topic_descriptions = []

        prompt = PromptTemplate(
            template=TOPIC_GEN_START,
            input_variables=[]
        )

        self.llm = LLMChain(
            prompt=prompt,
            llm=openai_model if model == "openai" else browser_model
        )

    def to_string(self):
        return "\n".join([
            x["topic"] + "\n" + x["description"] for x in self.topic_descriptions
        ])


class TopicContinuation(BaseTopicGenerator):
    def __init__(self, model="openai"):
        self.id = int(time.time())

        self.module_type = "TOPIC_CONTINUATION"

        self.topic_descriptions = []

        self.args_required = True

        prompt = PromptTemplate(
            template=TOPIC_GEN_CONTINUATION,
            input_variables=["topic"]
        )

        self.llm = LLMChain(
            prompt=prompt,
            llm=openai_model if model == "openai" else browser_model
        )

from __future__ import annotations


import jsonschema
from langchain import LLMChain, PromptTemplate
from langchain.callbacks import get_openai_callback
from .cache import cache_result
from src.KongBot.utils import db_conn

import tiktoken

from typing import Dict

import asyncio

from src.KongBot.utils import logger
from src.KongBot.models.models import gpt3, gpt4, deterministic_openai_model

import json
import os

TRAVERSE_PROBABILITY = 0.7


class BaseLLM:
    # the type ofmodule
    module_type = ""

    # arguments check
    prompt_args: Dict[str, str]

    # llmchain: openAI or BrowserGPT
    llm: LLMChain

    # list of args to pass to the Langchain PromptTemplate
    prompt_args: Dict = {}

    # langchain prompttemplate
    prompt: PromptTemplate

    # template
    template: str

    # schema to validate LLM output
    schema: Dict = None

    # whether to assume output json from LLM
    json_output: bool = False

    # stats for the LLM call including num of tokens and cost
    call_stats: Dict = {}

    def __init__(self, model, cache_policy, json_output, async_mode=False):
        # select model
        if model == "gpt3":
            self.openai_model = gpt3
        elif model == "gpt4":
            self.openai_model = gpt4
        else:
            raise Exception(f"Requested mode: {self.model} does not exist")

        self.cache_policy = cache_policy
        self.json_output = json_output
        self.async_mode = async_mode

    def init_prompt(self, template, **prompt_args):
        self.template = template
        # set args that are used later for promptetemplate
        self.prompt_args = ({k: v for k, v in prompt_args.items()})

        if not template:
            raise Exception("No prompt template specified")

        self.prompt = PromptTemplate(
            template=template,
            input_variables=[arg for arg in prompt_args.keys()]
        )

        self.llm = LLMChain(
            prompt=self.prompt,
            llm=deterministic_openai_model if os.environ.get(
                "OPENAI_DETERMINISTIC", None) == "1" else self.openai_model
        )

    # assumes json formatting
    def _parse(self, text: str):
        if self.json_output == False:
            return text

        try:
            # logger.debug(text)
            j = json.loads(text)
            # lazy, realistically we shud validate all schemas
            if self.schema:
                jsonschema.validate(j, self.schema)
            return j
        except json.JSONDecodeError as json_err:
            print("Error parsing the follwing to JSON: vvvvv\n", text)
            raise json_err
        except jsonschema.exceptions.ValidationError as validate_err:
            print("Error validating the following as JSON: vvvvv\n",
                  validate_err.__str__())
            raise validate_err

    def get_module_type(self):
        return self.module_type

    def get_llm_type(self):
        return self.__class__.__name__

    def get_llm_call_costs(self):
        return self.call_stats

    def set_schema(self, schema):
        self.schema = schema

    # TODO: prompt_args passed in as args will fuck with other methods
    # such as key that depends on static prompt_args on caching
    @cache_result
    def get_llm_output(self, prompt_args: Dict = None):
        retry = 3
        output = None
        prompt_args = prompt_args if prompt_args else self.prompt_args
        while retry > 0 and output is None:
            try:
                with get_openai_callback() as cb:
                    llm_response = self.llm.run(prompt_args)
                    output = self._parse(llm_response)

                    self.update_call_costs(
                        cb.total_tokens,
                        cb.prompt_tokens,
                        cb.completion_tokens,
                        cb.total_cost
                    )
            except Exception as e:
                retry -= 1
                if retry == 0:
                    raise e
                else:
                    print("LLM parsing failure, retrying...")
                    # logger.log_llm_stats(self.get_llm_type(), "failed")
        return output

    def update_call_costs(self,
                          total_tokens: int,
                          prompt_tokens: int,
                          complete_tokens: int,
                          total_cost: int):
        self.call_stats = {
            "total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "complete_tokens": complete_tokens,
            "total_cost": total_cost
        }

    def get_num_tokens(self):
        filled_prompt = self.prompt.format(**self.prompt_args)
        return self.num_tokens_from_string(filled_prompt, "cl100k_base")

    def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
        """
        Returns the number of tokens in a text string
        """
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def key(self):
        import hashlib

        filled_prompt = self.prompt.format(**self.prompt_args)
        hasher = hashlib.md5()
        hasher.update(filled_prompt.encode('utf-8'))
        return hasher.hexdigest()

    def save_prompt(self):
        """
        Saves the exact prompt used if no parsing errors where to occur
        """
        filled_prompt = self.prompt.format(**self.prompt_args)

        return self.__class__.__name__

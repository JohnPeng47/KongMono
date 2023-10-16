import os
import sys

import sys
sys.path.insert(0, r'C:\Users\jpeng\Documents\business\kongyiji\kongbot')

from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain import LLMChain, PromptTemplate
from bot.exploration.llm import ConceptsLLMQuery

deterministic_openai_model = OpenAI(
    model_name="gpt-3.5-turbo-0613",
    temperature = 0.0,
    openai_api_key="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"
)

prompt = PromptTemplate(
    template="Tell me a {joke}",
    input_variables=["joke"]
)

chain = LLMChain(
    prompt=prompt,
    llm = deterministic_openai_model,
)

with get_openai_callback() as cb:
    query = ConceptsLLMQuery("mathematics")

    print(query.get_llm_output())
    print(cb.total_tokens)
    print(cb.prompt_tokens)
    print(cb.completion_tokens)
    print(cb.total_cost)


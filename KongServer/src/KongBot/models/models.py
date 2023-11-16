from langchain import OpenAI
from langchain.callbacks.openai_info import OpenAICallbackHandler

gpt3 = OpenAI(
    model_name="gpt-3.5-turbo-0613",
    temperature=0.7,
    openai_api_key="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"
)

gpt4 = OpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key="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"
)

deterministic_openai_model = OpenAI(
    model_name="gpt-3.5-turbo-0613",
    temperature=0.0,
    openai_api_key="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"
)

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

from pydantic import BaseModel, validator
from typing import Union, Literal, List
from enum import Enum

class QuestionTypes(Enum):
    MULTIPLE_CHOICE = "mc"
    SHORT_ANSWER = "sa"

class MCQuestion(BaseModel):
    options: List[str]
    answer: int  # Initially just an int, will be validated to be an index

    @validator("answer")
    def check_answer_within_options(cls, value, values):
        if not (0 <= value < len(values['options'])):
            raise ValueError(f'answer must be an index within the range of options')
        return value
    
class EvalQuestion(BaseModel):
    type: QuestionTypes
    question: Union[MCQuestion, str]

    @validator('question')
    def validate_question(cls, value, values):
        if values.get('type') == QuestionTypes.MULTIPLE_CHOICE and not isinstance(value, MCQuestion):
            raise ValueError(f'question must be an instance of MCQuestion for type {QuestionTypes.MULTIPLE_CHOICE.value}')
        # if values.get('type') == QuestionTypes.SHORT_ANSWER and not isinstance(value, str):
        #     raise ValueError(f'question must be a str for type {QuestionTypes.SHORT_ANSWER.value}')
        return value
    
class GenQuestionRequest(BaseModel):
    type: str
    graph_id: str
    node_ids: List[str]

class GenQuestionResponse(BaseModel):
    questions: List[EvalQuestion]    


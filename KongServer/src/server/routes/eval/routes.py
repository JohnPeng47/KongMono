from fastapi import APIRouter, Depends

from typing import List
from logging import getLogger

from .schema import GenQuestionRequest, GenQuestionResponse, EvalQuestion, QuestionTypes, MCQuestion
from ..auth.service import get_user_from_token
from .service import generate_questions

logger = getLogger("base")
router = APIRouter()

@router.post("/eval/questions", 
            response_model=List[GenQuestionResponse])
def get_eval_questions(request: GenQuestionRequest, user = Depends(get_user_from_token)):
    pass
    # node_ids, graph_id = request.node_ids, request.graph_id
    # # perform authorization on user here
    # graph = graph_manager.load_graph(user, graph_id)
    # questions = generate_questions(node_ids, graph)

    # return GenQuestionResponse(questions=[
    #     EvalQuestion(
    #         type=QuestionTypes, 
    #         question=MCQuestion(options=question["options"], 
    #                             answer=question["answer"]))
    #     for question in questions 
    # ])

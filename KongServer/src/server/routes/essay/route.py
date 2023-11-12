from fastapi import APIRouter, Depends
from src.server.routes.graph.service import get_graph
from src.KongBot.bot.base import KnowledgeGraph
from src.KongBot.bot.essay_gen.generator import generate_essay_from_tree
router = APIRouter()

@router.get("/essay/{graph_id}")
def get_graph_route(graph_id: str, 
                    kg: KnowledgeGraph = Depends(get_graph)):
    essay = generate_essay_from_tree(kg)

    return {
        "essay" : essay
    }     

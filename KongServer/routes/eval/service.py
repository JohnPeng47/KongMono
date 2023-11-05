from typing import List
from KongBot.bot.base import KnowledgeGraph
from .llm import GenEvalQuestionMC

def generate_questions(node_ids: List[str], graph: KnowledgeGraph):
    config = {}

    topics = " and ".join([graph.get_node(node_id)["node_data"]["title"] for node_id in node_ids])
    questions = GenEvalQuestionMC(topics=topics, config=config)


    
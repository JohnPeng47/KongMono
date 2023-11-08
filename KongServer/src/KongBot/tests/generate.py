import pytest
import os

from src.KongBot.utils.db import db_conn
from tests.utils import equal
from src.KongBot.bot.base import KnowledgeGraph
from src.KongBot.explorationv2 import generate_treev2, generate_tree_details, generate_sub_trees


def test_gen_tree_v2():
    context = """
You are a member of the Russian Provisional Government under the faction of the Bolsheviks

The setting is pre-revolution Russia, when the Tsar has just abdicated the throne and the Russian Provisional government has just been
assembled. You are about to engage in parliamentary debates with the other factions to push across your legislative agenda on issue of:
Russia's Participation in the Great War

Create a briefing that will prepare your members for the debate
"""

    goal = """"""
    config = {
        "graph": {
            "nodes": 20,
        },
        "generate_treev2": {
            "cache_policy": "default",
            "goal": goal,
            "model": "gpt3"
        },
        "generate_tree_details": {
            "cache_policy": "CACHE",
            "depth": 1,
            "model": "gpt3"

        },
        "generate_sub_trees": {
            "cache_policy": "CACHE",
            "depth": 1,
            "model": "gpt3"
        }
    }

    kg = KnowledgeGraph(context, generators=[
        generate_treev2,
        generate_tree_details,
        generate_sub_trees
    ], config=config)

    assert kg.stats["num_nodes"] > config["graph"]["nodes"]


if __name__ == "__main__":
    pytest.main()

from .utils import is_csv_files_equal, is_yaml_files_equal
from .examples.small_graph import graph as knowledge_graph_data
from src.KongBot.eval import Eval
import yaml
import csv
import os
import pytest

TEST_GRAPH_ID = "41f826b1-fbd4-4f7b-bbed-9240d144bd35"


os.environ["RANDOM_SEED"] = "456"
test_csv_file = "examples/single_path.csv"
test_yaml_file = "examples/promptfooconfig.yaml"


class MockKnowledgeGraph:
    def __init__(self, curriculum, graph_id=None):
        self.curriculum = curriculum
        self.graph_data = knowledge_graph_data

    def get_random_single_path(self):
        # This is a mock version, it returns the same path each time for simplicity
        # In reality, you'd traverse the graph to get a path
        return [
            self.graph_data["node_data"],
            self.graph_data["node_data"]["children"][0]["node_data"],
            self.graph_data["node_data"]["children"][1]["node_data"]
        ]


@pytest.fixture
def evaluator():
    return Eval()


def test_eval_single_graph(evaluator):
    # Arrange
    graph_id = "41f826b1-fbd4-4f7b-bbed-9240d144bd35"

    # Act
    evaluator.eval_single_graph(graph_id)

    # Assert
    assert os.path.exists(
        evaluator.single_path_csv), "single_path.csv was not generated."
    assert os.path.exists(
        evaluator.single_path_yaml), "promptfooconfig.yaml was not generated."
    assert os.path.exists(
        evaluator.prompt_txt), "prompt.txt was not generated."

    # Read and verify CSV
    assert is_csv_files_equal(
        test_csv_file, evaluator.single_path_csv), "CSV file is not correct."
    assert is_yaml_files_equal(
        test_yaml_file, evaluator.single_path_yaml), "YAML file is not correct."

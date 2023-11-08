from src.KongBot.bot.base import KnowledgeGraph
from src.KongBot.utils.db import db_conn

from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
import json

from .llm import ConceptsLLMQuery, TopicsLLMQuery, SectionsLLMQuery, ExpandLLMQuery, BaseLLM

from src.KongBot.utils.exceptions import LLMJsonOutputError
from src.KongBot.utils import gen_unique_id


class Generator(ABC):
    """
    Base class for all generators, performing function of passing arguments to LLMQuery class,
    and persisting prompt template parameters for reproducing evals
    """
    llm: BaseLLM

    def __init__(self, graph: KnowledgeGraph, llm: BaseLLM, node_filter: Dict, llm_args: List):
        self.graph = graph
        self.attachto_nodes = graph.filter_nodes(node_filter)

        max, retrieve_mode = self.get_config()

        self.llm = self._init_llm(llm, llm_args + max)
        self.llm.retrieve_mode = retrieve_mode

    def generate(self) -> List[Dict]:
        llm_results = self.llm.get_llm_output()
        return self.gen_nodes(self.attachto_nodes, llm_results)

    def _init_llm(self, llm: BaseLLM, *llm_args):
        return llm(*llm_args)

    # implement parameter persistence here
    def _call_llm(self, *llm_args) -> List[Dict]:
        return self.llm.get_llm_output(*llm_args)

    def get_input_nodes(self) -> List[Dict]:
        pass

    def get_config(self) -> Tuple[int, str]:
        print("Getting config for class name: ", self.__class__.__name__)
        config: Dict = self.graph.config[self.__class__.__name__]
        max = config.get("max", 100000)
        retrieve_mode = config.get("retrieve_mode", "CACHE")

        return max, retrieve_mode

    @abstractmethod
    def gen_nodes(self, attachto_nodes: List[Dict], llm_result: List[Dict]) -> List[Dict]:
        pass

# class GenerateConcepts(Generator):
#     def gen_nodes(self, attachto_nodes: List[Dict], llm_result: List[Dict]) -> List[Dict]:
#         root_node = attachto_nodes[0]
#         try:
#             concepts = self.llm.get_llm_output()
#             children = [{
#                     "id": gen_unique_id(),
#                     "node_data" : {
#                         "title": c["concept"],
#                         "concept": c["concept"],
#                         "node_type": "CONCEPT_NODE"
#                     }
#                 } for c in concepts]
#             graph.add_nodes(children, attach_to_node)

#         except KeyError as missing_key:
#             raise LLMJsonOutputError("LLM output is missing a key: " + str(missing_key))


def generate_concepts(graph: KnowledgeGraph, retrieve_mode: str = "CACHE"):
    attach_to_node = graph.get_root()

    # get the specfic generator config
    config = graph.config["generate_concepts"]
    max = config.get("max", 100000)
    retrieve_mode = config.get("retrieve_mode", "CACHE")
    concepts = config.get("concepts", None)

    print("Generating topics config: ", max)

    result = ConceptsLLMQuery(graph.curriculum)
    result.retrieve_mode = retrieve_mode

    # TODO: need to define a cache key for LLM generated queries
    try:
        concepts = concepts if concepts else result.get_llm_output()
        children = [{
            "id": gen_unique_id(),
            "node_data": {
                    "title": c["concept"],
                    "concept": c["concept"],
                    "description": c["description"],
                    "node_type": "CONCEPT_NODE"
                    }
        } for c in concepts]
        graph.add_nodes(children, attach_to_node)

    except KeyError as missing_key:
        raise LLMJsonOutputError(
            "LLM output is missing a key: " + str(missing_key))


def generate_topics(graph: KnowledgeGraph, retrieve_mode: str = "CACHE"):
    attach_to_nodes = graph.filter_nodes({"node_type": "CONCEPT_NODE"})

    # get the specfic generator config
    config = graph.config["generate_topics"]
    max = config.get("max", 100000)
    model = config.get("model", "gpt3")
    print("Generating topics config: ", max)

    if len(attach_to_nodes) == 0:
        raise Exception(f"No concept nodes found in graph")

    try:
        for concept_node in attach_to_nodes:
            concept = concept_node["node_data"]["concept"]
            description = concept_node["node_data"]["description"]

            # TODO: arguable sus to have the graph hold curriculum here as well
            result = TopicsLLMQuery(
                graph.curriculum, concept, description, max, model)
            result.retrieve_mode = retrieve_mode

            content = result.get_llm_output()
            children = [
                {
                    "id": gen_unique_id(),
                    "node_data":
                        {
                            "title": c["topic"],
                            "description": c["description"],
                            "node_type": "TOPIC_NODE"
                    }
                }
                for c in content
            ]
            graph.add_nodes(children, concept_node)

    except KeyError as missing_key:
        raise LLMJsonOutputError(
            "LLM output is missing a key: " + str(missing_key))
    except Exception as e:
        print("Error in parsing LLM output: ", json.dumps(content, indent=4))
        raise e


def generate_sections(graph: KnowledgeGraph, retrieve_mode: str = "CACHE", max: int = 1000000):
    attach_to_nodes = graph.filter_nodes({"node_type": "TOPIC_NODE"})

    if len(attach_to_nodes) == 0:
        raise Exception(f"No concept nodes found in graph")

    # get the specfic generator config
    config = graph.config["generate_topics"]
    max = config.get("max", 100000)
    print("Generating topics config: ", max)

    try:
        count = 0
        for i, topic_node in enumerate(attach_to_nodes):
            topic = topic_node["node_data"]["title"]
            description = topic_node["node_data"]["description"]

            # TODO: arguable sus to have the graph hold curriculum here as well
            result = SectionsLLMQuery(topic, description, max)
            result.retrieve_mode = retrieve_mode

            sections = result.get_llm_output()

            children = [
                {
                    "id": gen_unique_id(),
                    "node_data":
                        {
                            "title": section["name"],
                            "section": section["section"],
                            "keywords": section["keywords"],
                            "node_type": "SECTION_NODE"
                    }
                }
                for section in sections
            ]

            count += 1
            graph.add_nodes(children, topic_node)

        print("Generated <<<<<<<<<", count, " sections")

    except KeyError as missing_key:
        raise LLMJsonOutputError(
            "LLM output is missing a key: " + str(missing_key))
    except Exception as e:
        print("Error in parsing LLM output: ", json.dumps(sections, indent=4))
        raise e


def generate_expansion(graph: KnowledgeGraph, retrieve_mode: str = "CACHE", max=190900000):
    attach_to_nodes = graph.filter_nodes({"node_type": "SECTION_NODE"})

    if len(attach_to_nodes) == 0:
        raise Exception(f"No concept nodes found in graph")

    # get the specfic generator config
    config = graph.config["generate_expansion"]
    max = config.get("max", 100000)
    print("Generating topics config: ", max)

    try:
        count = 0
        for i, section_node in enumerate(attach_to_nodes):
            print(f"Generating {i}th expansion node")

            section = section_node["node_data"]["section"]

            # TODO: arguable sus to have the graph hold curriculum here as well
            result = ExpandLLMQuery(graph.curriculum, section, max)
            result.retrieve_mode = retrieve_mode

            out = result.get_llm_output()

            children = [
                {
                    "id": gen_unique_id(),
                    "node_data":
                        {
                            "title": e["expansion"],
                            "paragraph": e["section"],
                            "node_type": "EXPANDED_TEXT_NODE",
                            "keywords": e["keywords"],
                    }
                }
                for e in out
            ]
            count += 1
            graph.add_nodes(children, section_node)
        print("Generated <<<<<<<<<", count, " expansions")
    except KeyError as missing_key:
        raise LLMJsonOutputError(
            "LLM output is missing a key: " + str(missing_key))
    except Exception as e:
        print("Error in parsing LLM output: ", json.dumps(out, indent=4))
        raise e

# TODO:
# def generate_expansion_long(graph: KnowledgeGraph, retrieve_mode: str = "CACHE", max = 190900000):
#     import random
#     PROBABILITY = 0.8
#     GEN_LEN = 3

#     attach_to_nodes = graph.filter_nodes({"node_type": "SECTION_NODE"})

#     if len(attach_to_nodes) == 0:
#         raise Exception(f"No concept nodes found in graph")

#     # get the specfic generator config
#     config = graph.gen_config["generate_expansion"]
#     max = config.get("max", 100000)
#     print("Generating topics config: ", max)

#     try:
#         count = 0
#         for i, section_node in enumerate(attach_to_nodes):
#             chance = random.randint(0, 1)
#             if chance < PROBABILITY:
#                 continue

#             print(f"Generating {i}th expansion node")

#             section = section_node["node_data"]["section"]

#             iteration = 0
#             while iteration < GEN_LEN:
#                 # TODO: arguable sus to have the graph hold curriculum here as well
#                 result = ExpandLLMQuery(graph.curriculum, section, max)
#                 result.retrieve_mode = retrieve_mode

#                 out = result.get_llm_output()

#                 children = [
#                     {
#                         "id": gen_unique_id(),
#                         "node_data":
#                             {
#                                 "title": e["expansion"],
#                                 "paragraph": e["section"],
#                                 "node_type": "EXPANDED_TEXT_NODE",
#                                 "keywords": e["keywords"],
#                             }
#                     }
#                     for e in out
#                 ]
#                 count += 1
#                 graph.add_nodes(children, section_node)


#         print("Generated <<<<<<<<<", count, " expansions")
#     except KeyError as missing_key:
#         raise LLMJsonOutputError("LLM output is missing a key: " + str(missing_key))
#     except Exception as e:
#         print("Error in parsing LLM output: ", json.dumps(out, indent=4))
#         raise e

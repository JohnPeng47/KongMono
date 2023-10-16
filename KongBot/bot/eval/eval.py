from typing import List, Dict, Optional
import csv
import os
import yaml
import glob

from bot.base import KnowledgeGraph
from utils import db_conn, logger

from .llm import GenerateCurriculumQuery

from functools import reduce


class Eval:
    def __init__(self, output_folder="MY_PROVIDER", num_tests:int = 10):
        self.PATH_LEN = 0
        self.NUM_TESTS = num_tests
        self.output_folder = os.path.join("C:\\Users\\jpeng\\Documents\\business\\kongyiji\\testing\\promptfoo\\examples\\", output_folder)
        self.single_path_csv =  os.path.join(self.output_folder, "single_path.csv")
        self.single_path_yaml = os.path.join(self.output_folder, "promptfooconfig.yaml")
        self.prompt_txt = os.path.join(self.output_folder, "prompt.txt")
        self.single_path_provider = lambda i: "provider{}.py".format(i)

        if os.path.exists(self.output_folder):
            self.clean_dir()
        else:
            os.makedirs(self.output_folder)

    def clean_dir(self):
        for filename in os.listdir(self.output_folder):
            file_path = os.path.join(self.output_folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

    def _get_data_field(self, node: Dict) -> str:
        node_data: Dict = node["node_data"]
        text_fields = ["description", "section", "paragraph", "concept"]
        for field in text_fields:
            if node_data.get(field, None):
                return node_data[field]
            
        print("No text field found in data: ", node_data)
        raise Exception("No text field found in data")
    
    def _get_title_field(self, node: Dict) -> str:
        return node["node_data"]["title"] 

    def _generate_prompt_txt(self, prompt: List = []):
        with open(self.prompt_txt, 'w') as file:
            if prompt:
                file.write("{{question}}\n")
            else:
                file.write(prompt[0])

    def _generate_single_path_csv(self, paths: List[Dict]):
        for path in paths:
            data_fields = [self._get_data_field(data).replace("\\n", "") for data in path]
            title_fields = [self._get_title_field(data) for data in path]
            csv_fields = ["TITLE: " + title_fields[i] + ": " + data_fields[i] for i in range(len(path))]

            with open(self.single_path_csv, 'a', newline='') as file:
                writer = csv.writer(file, delimiter="|")
                writer.writerow(csv_fields) # Writing each string as a row

    def _generate_yaml(self, path_len, num_paths, prompts):
        providers = [f"exec:python provider{i}.py" for i in range(path_len)]

        # hack: because we want to put curriculum name on the first column of the table
        # we have to stick it in here with the variables
        tests = reduce(lambda x,y: x + y, 
            [
                [
                    {"vars": {"question": "{}".format(prompt + ";-;" + str(i))}} for i in range(num_paths)
                ] for prompt in prompts
            ]
        )

        data = {
            "prompts": "prompt.txt",
            "providers": providers,
            "tests": tests
        }

        with open(self.single_path_yaml, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    def _generate_path_provider_files(self, path_len: int):
        for column in range(path_len):
            template = \
f"""
import sys
import csv

column = {column}
row = int(sys.argv[1].split(";-;")[1])

with open('single_path.csv', newline='') as csvfile:
    csvf = csv.reader(csvfile, delimiter='|')
    csvf = list(csvf)
    row = csvf[row]
    print(row[column].replace("\\n", " "))
"""
            with open(os.path.join(self.output_folder, self.single_path_provider(column)), 'w') as outfile:
                outfile.write(template)
    
    # def _eval_pairs(self, kg: KnowledgeGraph):
    #     from .prompt import COMPARE_NODE_ARISTOTLE_TEXT
    #     # TODO: filter out same node pairs
    #     pairs = [
    #         [kg.get_random_single_path(path_len=1) for _ in range(self.NUM_TESTS)],
    #         [kg.get_random_single_path(path_len=1) for _ in range(self.NUM_TESTS)],
    #     ]
        
    #     # generate paths
    #     self._generate_single_path_csv(pairs)
    #     # generate provider files
    #     self._generate_yaml(
    #         path_len, 
    #         self.NUM_TESTS * len(kg_list),
    #         prompts
    #     )
    #     self._generate_prompt_txt(prompt=prompts)


    #     self._eval_graph([kg], paths=pairs, prompts=[COMPARE_NODE_ARISTOTLE_TEXT])        

    def _eval_graph(
        self,
        kg_list: List[KnowledgeGraph],
        paths: List[List[Dict]] = [],
        prompts: List[str] = []
    ):
        """
        Construct a promptfoo config folder for a single graph
        """
        # ASSUMPTION: all graphs have the same path length
        path_len = len(kg_list[0].get_random_single_path())

        # accumulate all paths into a single list
        paths = reduce(lambda x, y: x + y, 
            [
                [
                    [
                        node for node in graph.get_random_single_path()
                    ]
                    for _ in range(self.NUM_TESTS)
                ] 
                for graph in kg_list
            ]
        ) if not paths else paths

        # likewise with the curriculums
        if len(prompts) == 0:
            prompts = [graph.curriculum for graph in kg_list]

        # generate paths
        self._generate_single_path_csv(paths)
        # generate provider files
        self._generate_path_provider_files(path_len)
        self._generate_yaml(
            path_len, 
            self.NUM_TESTS * len(kg_list),
            prompts
        )
        self._generate_prompt_txt(prompt=prompts)

    def eval_single_graph(
        self,
        graph_id
    ):
        """
        USed to evaluate single graph so we don't really care about what goes inside
        curriculum field
        """
        kg = KnowledgeGraph("Test Curriculum", graph_id=graph_id)
        self._eval_graph([kg])

    def eval_multi_graphs(
        self,
        run_id
    ):
        """
        Construct a promptfoo config folder for multiple graphs. The curriculum parameter
        is used to populate prompts.txt, which are the questions that's used to evaluate 
        the promptfoo testcases
        """
        graphs = KnowledgeGraph.get_graphs(run_id)
        self._eval_graph(graphs)


    def gen_diff_graphs(self, lesson_themes: List[str] = None):
        from bot.base import BaseLLM
        from bot.exploration import generate_concepts, generate_topics, generate_sections, generate_expansion
        from .prompt import CIVCS_LESSON_DESCRIPTION
        from utils import gen_unique_runid

        run_id = gen_unique_runid()
        config = {
            "generate_concepts" : {
                "retrieve_mode" : "NORMAL"
            },
            "generate_topics" : {
                "retrieve_mode": "NORMAL",
                "max": 1,
                "model": "gpt4"
            },
            "generate_sections" : {
                "retrieve_mode": "NORMAL",
                "max" : 1     
            },
            "generate_expansion":{
                "retrieve_mode": "NORMAL",
                "max" : 1
            }
        }
        
        curriculums = GenerateCurriculumQuery(model="gtp3").get_llm_output() if not lesson_themes else lesson_themes

        for curriculum in curriculums:

            graph = KnowledgeGraph(curriculum,
                generators=[
                    generate_concepts,
                    generate_topics,
                    generate_sections,
                    # generate_expansion
                ],
                config=config
            )
            
            graph.save_graph(run_id = run_id)

        logger.info(f"Generated eval graphs: {run_id}")

        return run_id
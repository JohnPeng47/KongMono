# might want to extend something on top of Graph
import random
from src.KongBot.eval import Eval
from src.KongBot.bot.base import KnowledgeGraph
from src.KongBot.exploration import generate_concepts, generate_topics, generate_sections, generate_expansion
from src.KongBot.utils import DBConnection

# fine-tune
# test_file = Path("bot/content/pdfs/government.txt")
# content = gen_fine_tune_data(test_file)

#### MAIN CODE ####
# build graph from scratch and insert into db
db_conn = DBConnection()
collection = db_conn.get_collection("test")

curriculum = """
describe fundamental beliefs and values associated with democratic citizenship in Canada, including
democracy, human rightds, freedom, and the rule of law, identifying some of their
key historical foundations, and explain ways in which these beliefs and values
are reflected in citizen actions 
"""

# kg = KnowledgeGraph("hello", graph_id="4eb623af-7c9e-43c0-a5c0-8c8872173442")

eval = Eval(
    output_folder="test_graph_gen"
)
# run_id = eval.gen_diff_graphs()
eval.eval_multi_graphs("run-id::bc4e9570-c6cd-4a16-a97f-b112f1ff57e1")

# graph = db_conn.get_all_graphs()[-1][0]
# kg = KnowledgeGraph("test", graph_id="8ca234ec-f65b-4c6a-ae86-72e21969bb65")

# sections = kg.filter_nodes({"node_type": "SECTION_NODE"})
# section_choice = [random.choice(sections) for _ in range(4)]
# print("Section nodes:")
# for section in section_choice:
#     print(section["node_data"]["title"])
#     print(section["node_data"]["section"])
# expands_nodes = kg.filter_nodes({"node_type": "EXPANDED_TEXT_NODE"})

# print("Text nodes:")
# expands = [random.choice(expands_nodes) for _ in range(3)]
# for e in expands:
#     print(e["node_data"]["title"])
#     print(e["node_data"]["paragraph"])

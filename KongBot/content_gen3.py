from bot.base import KnowledgeGraph
from bot.explorationv2 import generate_treev2, generate_tree_details, generate_sub_trees

with open("saved_graphs.txt", "r") as graph_ids:
    graph_ids = graph_ids.read().split("\n")
    for graph_id in graph_ids:
        if graph_id:
            print(graph_id)
            # try:
            #     kg = KnowledgeGraph(graph_id=graph_id)
            #     print(kg.curriculum)
            # except Exception as e:
            #     print(e)

# kg = KnowledgeGraph(context, generators=[
#     generate_treev2,
#     generate_tree_details,
#     generate_sub_trees
# ], config = config)
# kg.save_graph()
# print(kg.display_llm_call_costs())

# # kg = KnowledgeGraph("context", graph_id="a6de2871-27fe-4869-b42b-f7f5c010be9c")
# s = kg.to_json_frontend()
# kg.write_graph()
# # print(s)
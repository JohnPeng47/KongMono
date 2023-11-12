from src.KongBot.bot.base.graph import KnowledgeGraph
import json

TEST_GRAPH_SMALL = json.loads(open("test/KongServer/data/data.json", "r").read())
KG_ID = TEST_GRAPH_SMALL['id']
NON_EXISTENT_GRAPHID = "1234"

KG_INSTANCE = KnowledgeGraph("Test Curriculum")
KG_INSTANCE.from_json(TEST_GRAPH_SMALL)

def convert_kg_to_rf(kg: KnowledgeGraph):
    root = kg.get_root()
    
    node_data = root["node_data"]
    root["data"] = node_data
    root["hidden"] = False
    root["position"] = {
        "x" : 0,
        "y" : 0
    }
    root["positionAbsolute"] = {
        "x" : 0,
        "y" : 0
    }
    
    print(root["hidden"])

    kg.add_node(root, merge=True)
    print(kg.to_json())
    return kg

convert_kg_to_rf(KG_INSTANCE)
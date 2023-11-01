from pydantic import BaseModel
from fastapi import APIRouter

from .schema import GraphMetadataResp, GraphNode, RFNode, SaveGraphReq, rfnode_to_kgnode
from .db import get_graph_metadata_db, get_graph_db, delete_graph_db, delete_graph_metadata_db 

from fastapi.requests import Request
import uuid

from .utils import merge_tree_ids

from KongBot.bot.base import KnowledgeGraph
from KongBot.bot.explorationv2.llm import GenSubTreeQuery, Tree2FlatJSONQuery, GenSubTreeQueryV2
from KongBot.bot.adapters.ascii_tree_to_kg import ascii_tree_to_kg_v2
from KongBot.bot.explorationv2 import generate_short_description
from KongBot.bot.base.exceptions import GeneratorException

from typing import List
import json

from langchain import LLMChain, PromptTemplate, OpenAI

router = APIRouter()

@router.get("/metadata/", response_model=List[GraphMetadataResp])
def get_graph_metadata():
    metadata_list = []
    # consider returning a cursor here to be more memory efficient
    # although the pagination limit should do the trick?
    metadatas = get_graph_metadata_db(pagination=6)
    for document in metadatas:
        metadata_list.append(document)
    return metadata_list

@router.get("/graph/{graph_id}", response_model=GraphNode)
def get_graph(graph_id: str, request: Request):
    """
    This should be the 
    """
    if not request.app.curr_graph or request.app.curr_graph != graph_id:
        print("Loading graph: ", graph_id)
        request.app.curr_graph = KnowledgeGraph.load_graph(graph_id)

    kg: KnowledgeGraph = request.app.curr_graph
    
    return json.loads(kg.to_json_frontend())

@router.get("/graph/generate/{graph_id}")
def generate_graph(graph_id: str, request: Request):
    kg: KnowledgeGraph = request.app.curr_graph
    title = kg.get_root()["node_data"]["title"]

    config = {
        "global": {
            "subtree_size": 2
        },
        "generate_details_hierarchal": {
            "cache_policy": "default",
            "model": "gpt4",
        }
    }
    kg.add_config(config=config)
    kg.add_generators([
        generate_short_description
    ])
    success = kg.generate_nodes()
    kg.save_graph(title=title)

    return success

@router.post("/graph/update")
def update_graph(rf_graph: RFNode, request: Request):
    import random    
    kg: KnowledgeGraph = request.app.curr_graph
    
    kg_graph = rfnode_to_kgnode(rf_graph)
    kg.add_node(kg_graph, merge=True)
    print(kg.display_tree())

# TODO: Remove graph_id from this function and move delete button on UI to
# treeNode page once the graph has been selected
@router.get("/graph/delete/{graph_id}")
def delete_graph(graph_id: str, request: Request):
    delete_graph_db(graph_id)
    delete_graph_metadata_db(graph_id)

@router.post("/graph/save")
def update_graph(save_req: SaveGraphReq, request: Request):
    curr_kg: KnowledgeGraph = request.app.curr_graph

    rf_graph, title = save_req.graph, save_req.title
    

    kg_graph = rfnode_to_kgnode(rf_graph)
    # assign different ID so it gets saved as a new graph
    kg_graph["id"] = str(uuid.uuid4())

    curriculum = curr_kg.curriculum
    new_kg: KnowledgeGraph = KnowledgeGraph(curriculum)
    new_kg.from_json(kg_graph)
    new_kg.save_graph(title = title)

@router.post("/gen/subgraph/", response_model=GraphNode)
def gen_subgraph(rf_subgraph: RFNode, request: Request):
    kg: KnowledgeGraph = request.app.curr_graph

    rf_subgraph_json = rfnode_to_kgnode(rf_subgraph)

    kg.add_node(rf_subgraph_json, merge=True)
    tree1, tree2 = kg.display_tree_v2_lineage(rf_subgraph_json["id"])

    print("Subtree to generate: ", tree1, tree2)

    # GENERATE SUBTREE
    subtree = GenSubTreeQueryV2(kg.curriculum,
                                tree1 + tree2,
                                model="gpt4").get_llm_output()
    
    ## TODO: want to make sure that this error gets logged in our observability stack
    retry = 3
    while retry > 0:
        try:
            parent_ids = kg.parents(rf_subgraph_json["id"])
            parent = kg.get_node(parent_ids[0]) if len(parent_ids) > 0 else {}
            subtree_node_new = ascii_tree_to_kg_v2(subtree, rf_subgraph_json, parent)
            break
        except GeneratorException as e:
            print("Retrying...")
            print("Print exception: ", e)
            continue
            
    kg.add_node(subtree_node_new, merge=True)
    ## TODO: consider just returning the subgraph
    return json.loads(kg.to_json_frontend(parent_node=subtree_node_new))    
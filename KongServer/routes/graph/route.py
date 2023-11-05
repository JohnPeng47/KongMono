from fastapi import APIRouter, Depends

from .schema import GraphMetadataResp, GraphNode, RFNode, SaveGraphReq, rfnode_to_kgnode
from .service import get_graph_metadata_db, get_graph_db, delete_graph_db, delete_graph_metadata_db 

from fastapi.requests import Request
from fastapi import HTTPException

import uuid

from KongBot.bot.base import KnowledgeGraph
from KongBot.bot.explorationv2.llm import GenSubTreeQueryV2
from KongBot.bot.adapters.ascii_tree_to_kg import ascii_tree_to_kg_v2
from KongBot.bot.explorationv2 import generate_short_description

# from KongBot.bot.base.exceptions import GeneratorException
# TODO: have to import exceptions from here or else they conflict
# need to fix Python module setup
from bot.base.exceptions import GeneratorException

from typing import List
import json
from logging import getLogger

from ..auth.service import get_user_from_token

logger = getLogger("base")

router = APIRouter()

@router.get("/metadata/", 
            response_model=List[GraphMetadataResp])
# def get_graph_metadata(user = Depends(get_user_from_token)):
def get_graph_metadata(user = Depends(get_user_from_token)):
    metadata_list = []
    # consider returning a cursor here to be more memory efficient
    # although the pagination limit should do the trick?
    metadatas = get_graph_metadata_db()
    for document in metadatas:
        metadata_list.append(document)
    return metadata_list


@router.get("/graph/{graph_id}", response_model=GraphNode)
def get_graph(graph_id: str, request: Request):
    if not request.app.curr_graph or request.app.curr_graph != graph_id:
        print("Loading graph: ", graph_id)
        request.app.curr_graph = KnowledgeGraph.load_graph(graph_id)

    kg: KnowledgeGraph = request.app.curr_graph

    return json.loads(kg.to_json_frontend())

# TODO: Remove graph_id from this function and move delete button on UI to
# treeNode page once the graph has been selected
@router.get("/graph/delete/{graph_id}")
def delete_graph(graph_id: str, request: Request):
    delete_graph_db(graph_id)
    delete_graph_metadata(graph_id)

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
    new_kg.save_graph(title=title)

### These routes actually perform graph modification
@router.get("/graph/generate/{graph_id}")
def generate_graph(graph_id: str, request: Request):
    kg: KnowledgeGraph = request.app.curr_graph
    title = get_graph_metadata(graph_id)["metadata"]["title"]
    config = {
        "global": {
            "subtree_size": 2
        },
        "generate_short_description": {
            "cache_policy": "default",
            "model": "gpt3",
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
    kg: KnowledgeGraph = request.app.curr_graph

    kg_graph = rfnode_to_kgnode(rf_graph)
    kg.add_node(kg_graph, merge=True)

    kg.save_graph()


@router.post("/gen/subgraph/", response_model=GraphNode)
def gen_subgraph(rf_subgraph: RFNode, request: Request):
    kg: KnowledgeGraph = request.app.curr_graph

    rf_subgraph_json = rfnode_to_kgnode(rf_subgraph)

    kg.add_node(rf_subgraph_json, merge=True)
    tree1, tree2, _ = kg.display_tree_v2_lineage(rf_subgraph_json["id"])

    retry, success = 6, False
    default_model = "gpt3"
    while retry > 0 and not success:
        try:
            subtree = GenSubTreeQueryV2(kg.curriculum,
                                        tree1 + tree2,
                                        cache_policy="default",
                                        model=default_model).get_llm_output()

            parent_ids = kg.parents(rf_subgraph_json["id"])
            parent = kg.get_node(parent_ids[0]) if len(parent_ids) > 0 else {}
            subtree_node_new = ascii_tree_to_kg_v2(
                subtree, rf_subgraph_json, parent)

            kg.add_node(subtree_node_new, merge=True)
            # TODO: consider just returning the subgraph
            kg.save_graph()
            return json.loads(kg.to_json_frontend(parent_node=subtree_node_new))
        except GeneratorException as e:
            # to increment it by one
            logger.error(
                f"Retry attempt {6 - retry + 1}, use model: {default_model}, error: {e}")
            retry -= 1
            if retry <= 3:
                default_model = "gpt4"
            continue

    raise HTTPException(status_code=500, detail="Internal server error")

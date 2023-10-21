import { BackendNode } from "../common/common-types";
import { Node } from "reactflow";
import { 
  RFNodeData,
  RFEdge 
} from "../common/common-types";
import {
  CreateNode as CreateTreeNode,
  CreateEdge as CreateTreeEdge
} from "./processTree";
import {
  CreateNode as CreateMapNode,
  CreateEdge as CreateMapEdge
} from "./processMap";

export type GraphType = "Tree" | "ConceptMap";

export const CreateNode = (
  node: BackendNode,
  opType: GraphType
): Node<RFNodeData> => {
  if (opType === "Tree") {
    return CreateTreeNode(node);
  } else if (opType === "ConceptMap") {
    return CreateMapNode(node);
  }
}

export const CreateEdge = (
  node: BackendNode,
  parentId: string,
  opType: GraphType
): RFEdge => {
  if (opType === "Tree") {
    return CreateTreeEdge(node, parentId);
  } else if (opType === "ConceptMap") {
    return CreateMapEdge(node, parentId);
  }
}
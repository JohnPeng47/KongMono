import { BackendNode } from "../../common/common-types";
import { Node } from "reactflow";
import {
  RFNodeData,
  RFEdge,
  RFNode
} from "../../common/common-types";
import {
  ConvertNode as ConvertTreeNode,
  ConvertEdge as ConvertTreeEdge,
  CreateNode as CreateTreeNode,
  CreateEdge as CreateTreeEdge
} from "./processTree";
import {
  ConvertNode as ConvertMapNode,
  ConvertEdge as ConvertMapEdge
} from "./processMap";

export type GraphType = "Tree" | "ConceptMap";

export const ConvertNode = (
  node: BackendNode,
  opType: GraphType
): Node<RFNodeData> => {
  if (opType === "Tree") {
    return ConvertTreeNode(node);
  } else if (opType === "ConceptMap") {
    return ConvertMapNode(node);
  }
}

export const ConvertEdge = (
  node: BackendNode,
  parentId: string,
  opType: GraphType
): RFEdge => {
  if (opType === "Tree") {
    return ConvertTreeEdge(node, parentId);
  } else if (opType === "ConceptMap") {
    return ConvertMapEdge(node, parentId);
  }
}
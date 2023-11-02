import { CSSProperties } from "react";
import {
  BackendNode,
  RFNode,
  RFEdge,
  NodeType,
  RFNodeData
} from "../../common/common-types";

import { MarkerType, Node } from "reactflow";
import { generateUUID } from "../../common/utils";

export type GraphType = "Tree" | "ConceptMap";
export const ConvertNode = (
  node: BackendNode,
): Node<RFNodeData> => {
  // console.log(node.position.x);
  return {
    id: node.id,
    data: {
      title: node.data.title,
      node_type: node.data.node_type,
      description: node.data.description,
      // TODO: id is repeated here but kinda need it for the custom node which only takes
      // the data argument
      id: node.id,
      color: "white",
      // children : ["hello"]
      children: node.data.children
    },
    position: {
      x: 0,
      y: 0
      // x: node.position.x ? node.position.x : 0,
      // y: node.position.y ? node.position.y : 0
    },
    // need to change this
    type: NodeType.TreeNode,
    hidden: false
  }
}

export const ConvertEdge = (
  rfNode: any,
  parentId: string,
): RFEdge => {
  return {
    id: `e${parentId}-${rfNode.id}`,
    source: parentId,
    target: rfNode.id,
    type: "step",
    style: {
      stroke: rfNode.data.color,
      strokeDasharray: "5,5",
      color: "white",
      strokeWidth: 1,
    },
  };
}

type CreateNodeArg = Omit<RFNode, "id">;
export const CreateNode = (
  rfNode: CreateNodeArg
): RFNode => {
  const id = generateUUID();
  console.log("Generating node with id: ", id);
  return {
    ...rfNode,
    id: id,
    data: {
      ...rfNode.data,
      node_type: "treeNode",
      id: id
    }
  }
}

type CreateEdgeArg = Omit<RFEdge, "id">
export const CreateEdge = (
  rfEdge: CreateEdgeArg
): RFEdge => {
  return {
    ...rfEdge,
    id: generateUUID(),
    type: "step",
    style: {
      stroke: "black",
      strokeDasharray: "5,5",
      strokeWidth: 1,
    },
  }
}
import { CSSProperties } from "react";
import {
  BackendNode,
  RFNode,
  RFEdge,
  NodeType,
  RFNodeData
} from "../common/common-types";

import { MarkerType, Node } from "reactflow";
export type GraphType = "Tree" | "ConceptMap";

export const CreateNode = (
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

export const CreateEdge = (
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
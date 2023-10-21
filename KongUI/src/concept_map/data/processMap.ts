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
      color:  node.data.color,
      children: node.data.children
    },
    position: {
      x: 0,
      y: 0
      // x: node.position.x ? node.position.x : 0,
      // y: node.position.y ? node.position.y : 0
    },
    // need to change this
    type: !node.hidden && node.hidden !== null ? NodeType.AttachedNode : NodeType.UnattachedNode,
    hidden: !node.hidden && node.hidden ? false : node.hidden === null || node.hidden
  }
}

export const CreateEdge = (
  rfNode: any,
  parentId: string,
): RFEdge => {
  // Add an edge if there is a parent ID
  return {
    id: `e${parentId}-${rfNode.id}`,
    source: parentId,
    target: rfNode.id,
    markerEnd: {
      type: MarkerType.Arrow,
    },
    style: {
      stroke: rfNode.data.color,
      strokeDasharray: "5,5",
      strokeWidth: 4,
    },
  };
}

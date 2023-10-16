import { CSSProperties } from "react";
import {
  BackendNode,
  RFNode,
  RFEdge,
  NodeType,
} from "../common/common-types";

import { MarkerType } from "reactflow";

export type GraphType = "Tree" | "ConceptMap";

export const CreateNode = (
  node: BackendNode,
  opType: GraphType
): RFNode => {
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
      color:
        opType === "ConceptMap"
          ? node.data.color
          : "white",
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
    type:
      opType === "ConceptMap"
        ? !node.hidden && node.hidden !== null ? NodeType.AttachedNode : NodeType.UnattachedNode
        // Assume Tree if not ConceptMap
        : NodeType.TreeNode,
    hidden:
      opType === "ConceptMap"
        ? !node.hidden && node.hidden ? false : node.hidden === null || node.hidden
        // Assume Tree if not ConceptMap
        : false
  }
}

export const CreateEdge = (
  rfNode: any,
  parentId: string,
  opType: GraphType
): RFEdge => {
  // Add an edge if there is a parent ID
  if (opType === "ConceptMap") {
    if (parentId) {
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
  } else if (opType === "Tree") {
    if (parentId) {
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
  }
}

function generateRandomString(length = 4) {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";

  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }

  return result;
}

// export const processJsonEntities = (
//   json: JSONNode,
// ): { initialNodes: any[]; initialEdges: any[] } => {
//   const initialNodes: ReactFlowNode[] = [];
//   const initialEdges: ReactFlowEdge[] = [];

//   const isInNodesArray = (label: string) => {
//     return initialNodes.find((node) => node.data.label === label);
//   };

//   const traverse = (node: JSONNode, parentId?: string) => {
//     const addNode = (label: string) => {
//       const node_id = generateRandomString();
//       initialNodes.push({
//         id: node_id,
//         data: {
//           label: label,
//           id: node_id,
//           color: node.data.color ? node.data.color : "#3F301D",
//           description: "",
//         },
//         data: node.data,
//         position: {
//           x: 0,
//           y: 0,
//         },
//         hidden: false,
//         type: NodeType.AttachedNode,
//       });
//       return node_id;
//     };
//     const addEdge = (source_id: string, target_id: string, label: string) => {
//       initialEdges.push({
//         id: `e${source_id}-${target_id}`,
//         source: source_id,
//         target: target_id,
//         data: {
//           label: label,
//         },
//         markerEnd: {
//           type: MarkerType.Arrow,
//         },
//         style: {
//           stroke: node.data.color,
//           strokeDasharray: "5,5",
//           strokeWidth: 4,
//         },
//       });
//     };

//     if (node.data.entity_relations) {
//       // only add entity relations
//       node.data.entity_relations.forEach((entity: EntityNode) => {
//         const {
//           target: target_label,
//           source: source_label,
//           relation: relation_label,
//         } = entity;

//         const targetNode = isInNodesArray(target_label);
//         const sourceNode = isInNodesArray(source_label);

//         if (!targetNode && !sourceNode) {
//           const target_nodeid = addNode(target_label);
//           const source_nodeid = addNode(source_label);
//           addEdge(source_nodeid, target_nodeid, relation_label);
//         } else if (!targetNode && sourceNode) {
//           const target_nodeid = addNode(target_label);
//           addEdge(sourceNode.id, target_nodeid, relation_label);
//         } else if (targetNode && !sourceNode) {
//           const source_nodeid = addNode(source_label);
//           addEdge(source_nodeid, targetNode.id, relation_label);
//         } else {
//           console.log("Im am adding edge betewen existing");
//           addEdge(sourceNode.id, targetNode.id, relation_label);
//         }
//       });

//       // Recursively process children if any
//       if (node.data.children) {
//         node.data.children.forEach((child) => traverse(child, node.id));
//       }
//     }
//   };

//   traverse(json);
//   return { initialNodes, initialEdges };
// };

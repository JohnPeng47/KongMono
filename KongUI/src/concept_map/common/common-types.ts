import { CSSProperties } from "react";
import { EdgeMarker, MarkerType } from "reactflow";
import { Backend } from "./Backend";
import { Node } from "reactflow";


// basically typescript enums
export type SchemaId = string & { readonly __schemaId: never };
export type InputId = number & { readonly __inputId: never };

export type Mutable<T> = { -readonly [P in keyof T]: T[P] };

export type InputValue = InputSchemaValue | undefined;
export type InputSchemaValue = string | number;
export type NodeID = string

export type Position = {
  x : number,
  y : number
}
// Node data received from server
export type BackendNode = {
  id: string;
  attached?: boolean;
  hidden?: boolean;
  position: Position
  data: BackendNodeData;
};

export type BackendNodeData = {
  title: string;
  node_type: string;
  children?: BackendNode[];
  concept?: string;
  description?: string;
  color?: string;
  entity_relations?: EntityNode[];
}

// Used for reactFlow nodes
export type RFNodeData = BackendNodeData & {
  id: string,
};

// This is only used in initial conversion from the backend
export type RFNode = {
  id: string;
  data: RFNodeData,
  type: string;
  position?: {
    x: number;
    y: number;
  };
  hidden: boolean;
};

export type EntityNode = {
  source: string;
  target: string;
  relation: string;
};

export type RFEdge = {
  id: string;
  source: string;
  target: string;
  style?: CSSProperties;
  type?: string;
  markerEnd?: EdgeMarker,
  data?: {
    label?: string;
  };
};

export enum NodeType {
  AttachedNode = "attachedNode",
  UnattachedNode = "unattachedNode",
  TreeNode = "treeNode"
}

const COLORS = [
  "#F18F01",
  "#99C24D",
  "#77A6B6",
  "#D81159",
  "#8A4FFF",
  "#EDAFB8",
  "#56EEF4",
];

export type SetState<T> = React.Dispatch<React.SetStateAction<T>>;


function getRandomElements(arr, n) {
  // Fisher-Yates shuffle
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.slice(0, n);
}

export function getColors(n: number) {
  return getRandomElements(COLORS, n);
}
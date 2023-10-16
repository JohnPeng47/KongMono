import React, { useCallback } from "react";

import { 
  useState, 
  useMemo, 
  useEffect,
} from "react";

import { 
  Node, 
  Handle, 
  Position, 
  useReactFlow, 
} from 'reactflow';

import { 
  RFNodeData,
  NodeType
} from "../../common/common-types";

import Box from '@mui/material/Box';

type UnattachedNodeProps = {
  data: RFNodeData;
  isConnectable: boolean;
};

function UnattachedNode({ data: currData, isConnectable }: UnattachedNodeProps) {    
  const { getEdges, getNodes, setNodes, setEdges } = useReactFlow();
  const { id } = currData;

  const { source: parentId } = getEdges()
    // hack because root node does not have parent
    .find((edge) => edge.target === currData.id) ?? { id: "fake" }

  // memoize this
  const siblings = getNodes()
    .filter((node) => 
      getEdges()
        .filter((edge) => edge.source === parentId)
        .map((edge) => {
          return edge.target
        })
        .some((id) => id === node.id) && node.id !== currData.id
    )
  
  const selectCurrNode= useCallback(() => {
    const attachHideNodes = getNodes().map((node) => {
      if (node.id === id) {
        return {
          ...node,
          type: NodeType.AttachedNode
        };
      } 
      else if (siblings.some((sibling) => node.id === sibling.id) && node.type !== NodeType.AttachedNode) {
        return {
          ...node,
          hidden: true
        };
      }
      return node;
    })
    setNodes(attachHideNodes);

    const hideEdges = getEdges().map((edge) => {
      return siblings.some((sibling) => sibling.id === edge.target && sibling.type !== NodeType.AttachedNode)
        ? {
          ...edge,
          hidden: true
        }
        : edge
    })
    setEdges(hideEdges)

    } , [setEdges, setNodes, siblings, id])

    return (
      <Box className="text-updater-node-unattached" onClick={() => selectCurrNode()}>
        <div>{currData.title}</div>
        <Handle type="target" position={Position.Top} isConnectable={true} />
        <Handle type="source" position={Position.Bottom} isConnectable={true} />
      </Box>
    )
  }
  
export default UnattachedNode;
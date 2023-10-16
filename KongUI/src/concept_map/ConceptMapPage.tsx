import React, { useState, useEffect, useMemo } from "react";
import ReactFlow, {
  ReactFlowProvider,
  Panel,
  useNodesState,
  useEdgesState,
  applyNodeChanges,
  NodeChange,
  EdgeChange,
  OnNodesChange,
  applyEdgeChanges,
  OnEdgesChange,
} from "reactflow";
import { useContext } from "use-context-selector";
import { GlobalContext, GlobalProvider } from "./provider/globalProvider";
import AttachedNode from "./components/node/AttachedNode";
import UnattachedNode from "./components/node/UnattachedNode";
import useForceLayout from "./layout/useForceLayout";
import { getColors } from "./common/common-types";

import { useParams } from "react-router-dom";

import "reactflow/dist/style.css";
import TreeNode from "./components/node/TreeNode";

// let {initialEdges, initialNodes} = processJsonEntities(entity_relations);

const nodeTypes = {
  attachedNode: AttachedNode,
  unattachedNode: UnattachedNode,
  treeNode: TreeNode
};

const ConceptMapPage = () => {
  let initialNodes = [];
  let initialEdges = [];

  const { mapId } = useParams();
  const [ initialized, setInitialized ] = useState<boolean>(false);

  const { setSelectedNode, downloadGraph} = useContext(GlobalContext);

  // const [dataFetched, setDataFetched] = useState(false);

  const [nodes, setNodes] = useNodesState([]);
  const [edges, setEdges] = useEdgesState([]);

  if (!initialized)
    downloadGraph(mapId, "ConceptMap")

  // useAutoLayout({direction:"TB"});
  useForceLayout({ strength: -1, distance: 150 });

  if (!initialized && initialNodes.length > 0) {
    const rootNode = nodes[0];
    setSelectedNode(rootNode.id);

    const outEdges = edges.filter((edge) => edge.source === rootNode.id);
    const topLevelParents = nodes.filter((node) => {
      return outEdges.some((edge) => edge.target === node.id);
    });

    // give top level parent random color
    const colors = getColors(topLevelParents.length);
    setNodes(
      nodes.map((node) => {
        if (topLevelParents.some((parent) => parent.id === node.id)) {
          return {
            ...node,
            data: {
              ...node.data,
              color: colors.pop(),
            },
          };
        } else {
          return node;
        }
      })
    );
  }

  const onNodesChange: OnNodesChange = (changes: NodeChange[]) => {
    setNodes((nodes) => applyNodeChanges(changes, nodes));
  };

  const onEdgesChange: OnEdgesChange = (changes: EdgeChange[]) => {
    setEdges((edges) => applyEdgeChanges(changes, edges));
  };

  if (!initialized) setInitialized(true);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      nodeTypes={nodeTypes}
      fitView
    >
      <Panel position="top-right">
        {/* <button onClick={onLayout}>layout</button> */}
      </Panel>
    </ReactFlow>
  );
};

// export default ConceptMapPage;

export default function () {
  return (
    <ConceptMapPage />
  );
}

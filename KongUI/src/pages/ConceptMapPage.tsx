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
import AttachedNode from "../concept_map/components/node/AttachedNode";
import UnattachedNode from "../concept_map/components/node/UnattachedNode";
import useForceLayout from "../concept_map/layout/useForceLayout";
import { getColors } from "../concept_map/common/common-types";

import { useParams } from "react-router-dom";

import "reactflow/dist/style.css";
import TreeNode from "../concept_map/components/node/TreeNode";

import useCytoScapeLayout from "../concept_map/layout/CytoscapeLayout";
import { ConceptMapProvider, ConceptMapContext } from "../concept_map/provider/ConceptMapProvider";

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

  const { setSelectedNode, downloadGraph } = useContext(ConceptMapContext);

  // const [dataFetched, setDataFetched] = useState(false);

  const [nodes, setNodes] = useNodesState([]);
  const [edges, setEdges] = useEdgesState([]);

  if (!initialized)
    downloadGraph(mapId, "ConceptMap")

  // useAutoLayout({direction:"TB"});
  // useForceLayout({ strength: -1, distance: 150 });
  useCytoScapeLayout();

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
    <ConceptMapProvider>
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
    </ConceptMapProvider>
  );
};

// export default ConceptMapPage;

export default function () {
  return (
    <ConceptMapProvider>
      <ConceptMapPage />
    </ConceptMapProvider>
  );
}

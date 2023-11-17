import { useCallback, useEffect, useState } from "react";
import { useContext } from "use-context-selector";
import ReactFlow, {
    applyNodeChanges,
    applyEdgeChanges,
    ReactFlowProvider,
    useNodesState,
    useEdgesState
} from "reactflow";
import { useParams } from "react-router-dom";
import TreeNode from "../concept_map/components/node/TreeNode";
import { Fab } from "@mui/material";
import QuizIcon from "@mui/icons-material/Add";
import { TreeEditMapContext, TreeEditMapProvider } from "../concept_map/provider/TreeEditMapProvider";
import SideMenu from "../concept_map/components/sidebar";


const nodeTypes = {
  treeNode : TreeNode
}

function TreeEditMapPage() {
  const [ initialized, setInitialized ] = useState(false);
  const [ sideMenuOpen, setSideMenuOpen ] = useState(false);

  const { mapId } = useParams();
  // const [dataFetched, setDataFetched] = useState(false);

  const [nodes, setNodes] = useNodesState([]);
  const [edges, setEdges] = useEdgesState([]);
  const { downloadGraph } = useContext(TreeEditMapContext);

  if (!initialized) {
    downloadGraph(mapId, "Tree");
    setInitialized(true);
  }

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );
  
  return (
    <div style={{ height: '100%' }}>
      <ReactFlow
        nodes={nodes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        edges={edges}
        nodeTypes={nodeTypes}
        deleteKeyCode={null}
        zoomOnDoubleClick={null}
        // disable dragging
        nodesDraggable={false}
      >
      </ReactFlow>
      <Fab color="primary" aria-label="add" 
        onClick={() => setSideMenuOpen(open => !open)}
        sx={{
         position: 'fixed', 
         bottom: 100, 
         right: 70,
        }}>
        <QuizIcon />
      </Fab>
      <SideMenu 
        isOpen={sideMenuOpen} 
        setIsOpen={setSideMenuOpen}></SideMenu>
    </div>
  );
}
  
export default function () {
  return (
    <TreeEditMapProvider>
      <TreeEditMapPage />
    </TreeEditMapProvider>
  );
}
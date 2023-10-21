import React, { 
    memo, 
    useCallback, 
    useState, 
    useRef,
  } from "react";
  import { createContext, useContext } from "use-context-selector";
  import { useMemoObject } from "../hooks/useMemo";
  import { 
    useReactFlow, 
    Node,
  } from "reactflow";
  import { NodeType } from "../common/common-types";
  import { GraphUtils } from "../graph/graphUtils";
  import { GraphType } from "../data/processNodes";
  import { BackendContext } from "./backendProvider";
  
  interface ConceptMap {
    //TODO: figure out what this does
    showHideUnattachedChildren: (childNodes: Node[]) => void;
    setSelectedNode: (any) => any;
    downloadGraph: (graphID: string, graphType: GraphType) => void;
  }
  
  export const ConceptMapContext = createContext<Readonly<ConceptMap>>({} as ConceptMap);
  export const ConceptMapProvider = memo(
    ({
      children,
    }: React.PropsWithChildren) => {  
      const { backend } = useContext(BackendContext);
      const { 
        setNodes, 
        setEdges, 
        getNodes, 
        getEdges, 
      } = useReactFlow();
    
      const graph = useRef(new GraphUtils(getNodes, getEdges)).current;
      const [selecteNodeID, setSelectedNode] = useState<string>("null_user_id");
      
      const downloadGraph = (graphId: string, graphType: GraphType) => {
        backend.downloadGraph(graphId)
          .then((res) => {
            // represents the order of nodes in JSON format
            let {newNodes, newEdges} = graph.initJson(res.data, graphType);
            setNodes(newNodes);
            setEdges(newEdges);
          })
          .catch(error => {
            console.error("Error fetching graph error: ", error);
            throw error;
          })
      }
  
      const showHideUnattachedChildren = useCallback(
        (childNodes: Node[]) => {
          const showHideNodes = getNodes().map((node) => {
            if (node.type === NodeType.UnattachedNode) {
              // if (unattachedNodes.some((unattached) => unattached.id === node.id )) {
              if (childNodes.some((child) => child.id === node.id)) {
                return {
                  ...node,
                  hidden: !node.hidden,
                };
              }
              return {
                ...node,
                hidden: true,
              };
            } else {
              return node;
            }
          });
  
          const unattachedNodes = getNodes().filter(
            (node) => node.type === NodeType.UnattachedNode
          );
  
          const showHideEdges = getEdges().map((edge) => {
            if (unattachedNodes.some((node) => node.id === edge.target)) {
              if (childNodes.some((child) => child.id === edge.target)) {
                return {
                  ...edge,
                  hidden: edge.hidden ? !edge.hidden : false,
  
                };
              } else
                return {
                  ...edge,
                  hidden: true,
                };
            } else {
              return edge;
            }
          });
  
          setEdges(showHideEdges);
          setNodes(showHideNodes);
        },
        [setNodes, setEdges, getEdges, getNodes]
      );
  
      const globalValue = useMemoObject<ConceptMap>({
        showHideUnattachedChildren,
        setSelectedNode,
        downloadGraph
      });
  
      return (
        <ConceptMapContext.Provider value={globalValue}>
            {children}
        </ConceptMapContext.Provider>
      );
    }
  );
  
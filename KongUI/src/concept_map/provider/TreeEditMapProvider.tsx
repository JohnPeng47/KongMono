import React, { 
    memo, 
    useCallback, 
    useEffect,
    useRef,
    useMemo
  } from "react";
  import { createContext, useContext } from "use-context-selector";
  import { useMemoObject } from "../hooks/useMemo";
  import { 
    useReactFlow, 
    Node,
  } from "reactflow";
  import { GraphUtils } from "../graph/graphUtils";
  import { RFNodeData } from "../common/common-types";
  
  import {
    ChangeCounter,
    nextChangeCount,
    useChangeCounter,
    wrapRefChanges,
  } from '../common/hooks/useChangeCounter';
  
  import { SetState } from "../common/common-types";
  
  import { GraphType } from "../data/processJson";
  import { BackendContext } from "./backendProvider";
  import { AxiosResponse } from "axios";
  
  interface TreeEditMap {
    downloadGraph: (graphID: string, graphType: GraphType) => void;
    genSubGraph: (nodeId: string) => void;
    modifyNodeTitle: (nodeId: string, newTitle: string) => void;
    deleteNode: (nodeId: string) => void;
    saveGraph: (title: string) => void;
    genGraphDesc: (graphId: string) => Promise<AxiosResponse>;
  }
  
  export const TreeEditMapContext = createContext<Readonly<TreeEditMap>>({} as TreeEditMap);
  export const TreeEditMapProvider = memo(
    ({
      children,
    }: React.PropsWithChildren) => {
      const [nodeChanges, addNodeChanges, nodeChangesRef] = useChangeCounter();
      const { backend } = useContext(BackendContext);
      const { 
        setNodes, 
        setEdges, 
        getNodes, 
        getEdges, 
      } = useReactFlow();
  
      const graph = useRef(new GraphUtils(getNodes, getEdges)).current;
      const setNodesRef = useRef<SetState<Node<any>[]>>(setNodes);
  
      const changeNodes = useMemo(
        () => wrapRefChanges(setNodesRef, addNodeChanges),
        [addNodeChanges]
      );
  
      
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
    
      const modifyNode = useCallback(
        (id: string, mapFn: (oldNode: Node<RFNodeData>) => Node<RFNodeData>) => {
            setNodes((nodes) => {
                const newNodes: Node<RFNodeData>[] = [];
                for (const n of nodes) {
                    if (n.id === id) {
                        const newNode = mapFn(n);
                        if (newNode === n) return nodes;
                        newNodes.push(newNode);
                    } else {
                        newNodes.push(n);
                    }
                }
                return newNodes;
            });
        },
        [setNodes]
      );
  
      const modifyNodeTitle = useCallback(
        (id: string, newTitle: string): void => {
          modifyNode(id, (old) => {
            return {
              ...old,
              data : {
                ...old.data,
                title: newTitle
              }
            }
          })
        }, [modifyNode]
      )
  
      /**
       * Deletes node and all its children as well as repositioning
       */
      const deleteNode = useCallback(
        (id: string) : void => {
          const node = graph.findNodeRF(id);
          const children = graph.getAllChildren(id);
          const deleteNodes = [children, node].flat();
  
          const newNodes = getNodes().filter((node) => 
            !deleteNodes.some((delNode) => delNode.id === node.id)
          )
          .map((node, index) => {
            return {
              ...node,
              position: {
                x : node.position.x,
                y : index * 70
              }
            }
          })
  
          changeNodes(newNodes);
        }, [changeNodes]
      )
  
      /**
       * Can use this to trigger syncs with the backend
       */
      useEffect(() => {
        if (nodeChanges === 0) 
          return
  
        const rootNode = getNodes()[0];
        const updateRoot = graph.RFtoJSON(rootNode);
        backend.updateGraph(updateRoot);
      }, [nodeChanges])
  
      /**
       * Syncs graph with updated node 
       */
      const genSubGraph = (nodeId: string): void => {
        const subgraph = graph.RFtoJSON(nodeId);
  
        backend.genSubGraph(subgraph).then((res) => {
          const {
            updateNodes, 
            updateEdges
          } = graph.updateJson(res.data);
  
          setNodes(updateNodes);
          setEdges(updateEdges);
        })
      } 
  
      /**
       * Generate graph description
       */
      const genGraphDesc = (graphId: string): Promise<AxiosResponse> => {
        console.log("Generating graph: ", graphId);
        return backend.genGraphDesc(graphId);
      } 
      
      const saveGraph = (title: string): void => {
        const rootNode = getNodes()[0];
        console.log("Saving graph: ", rootNode);
  
        const updateRoot = graph.RFtoJSON(rootNode);
        backend.saveGraph(updateRoot, title);
      }
   
      const globalValue = useMemoObject<TreeEditMap>({
        downloadGraph,
        genSubGraph,
        deleteNode,
        modifyNodeTitle,
        saveGraph,
        genGraphDesc
      });
    
      return (
        <TreeEditMapContext.Provider value={globalValue}>
            {children}
        </TreeEditMapContext.Provider>
      );
    }
  );
  
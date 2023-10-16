import React, { 
  memo, 
  useCallback, 
  useState, 
  useEffect,
  useRef,
  useMemo
} from "react";
import { createContext, useContext } from "use-context-selector";
import { useMemoObject } from "../hooks/useMemo";
import { 
  useReactFlow, 
  Node,
  Edge
} from "reactflow";
import { NodeType } from "../common/common-types";
import { GraphUtils } from "../graph/graphUtils";
import { RFNodeData } from "../common/common-types";

import {
  ChangeCounter,
  nextChangeCount,
  useChangeCounter,
  wrapRefChanges,
} from '../common/hooks/useChangeCounter';

import { SetState } from "../common/common-types";
import { generateUUID } from "../common/utils";

import { GraphType } from "../data/processJson";
import { BackendContext } from "./backendProvider";

interface Global {
  //TODO: figure out what this does
  reactFlowWrapper: string;
  showHideUnattachedChildren: (childNodes: Node[]) => void;
  setSelectedNode: (any) => any;
  downloadGraph: (graphID: string, graphType: GraphType) => void;
  genSubGraph: (nodeId: string) => void;
  modifyNodeTitle: (nodeId: string, newTitle: string) => void;
  deleteNode: (nodeId: string) => void;
  saveGraph: (title: string) => void;
}

interface GlobalVolatile {
  // TODO: change this SetState proper def
  selecteNodeID: string;
  // unattachedNodeIDRef: React.MutableRefObject<string>
}

interface GlobalProviderProps {
  reactFlowWrapper: string;
  // reactFlowWrapper: React.RefObject<HTMLDivElement>;
}

export const GlobalVolatileContext = createContext<Readonly<GlobalVolatile>>(
  {} as GlobalVolatile
);
export const GlobalContext = createContext<Readonly<Global>>({} as Global);
export const GlobalProvider = memo(
  ({
    children,
    reactFlowWrapper,
  }: React.PropsWithChildren<GlobalProviderProps>) => {
    const [nodeChanges, addNodeChanges, nodeChangesRef] = useChangeCounter();

    const { backend } = useContext(BackendContext);
    
    const { 
      setNodes, 
      setEdges, 
      getNodes, 
      getEdges, 
    } = useReactFlow();

    const setNodesRef = useRef<SetState<Node<any>[]>>(setNodes);

    const changeNodes = useMemo(
      () => wrapRefChanges(setNodesRef, addNodeChanges),
      [addNodeChanges]
    );

    const graph = new GraphUtils(getNodes, getEdges);
    const [selecteNodeID, setSelectedNode] = useState<string>("null_user_id");
    
    const downloadGraph = (graphId: string, graphType: GraphType) => {
      async function fetchData() {
        backend.downloadGraph(graphId)
          .then((res) => {
            // represents the order of nodes in JSON format
            let {newNodes, newEdges} = graph.processJson(res.data);
            newNodes = newNodes.map((node, index) => (
              {
                ...node,
                position: {
                  x : graph.findNodeDepth(node.id) * 50,
                  y : index * 74
                }
              }
            ))

            setNodes(newNodes);
            setEdges(newEdges);
          })
      }
      fetchData();
    }

    // TODO: fix this node repositioning
    // also has to keep track of old position
    // useEffect(() => {
    //   let position = 0;
    //   const newNodes = getNodes().map((node) => {
    //     const newPos = {
    //       ...node,
    //       position: {
    //         x : node.position.x,
    //         y : position * 50
    //       }
    //     }
    //     position += 1;
    //     return newPos;
    //   })
    //   setNodes(newNodes);
    // }, [getNodes, setNodes])

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

    const addNode = useCallback(
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
              y : index * 50
            }
          }
        })

        changeNodes(newNodes);
      }, [changeNodes]
    )

    /**
     * Add nodes as well as repositioning
     */
    // const addNodes = useCallback(
    //   (nodes: [{child: Node<RFNodeData>, parent: Node<RFNodeData>}]) : void => {
    //     const newNodes = [];
    //     for (let node of nodes) {
    //       const parentNode = 
          
    //     }
    //   }, [changeNodes]
    // )



    /**
     * Can use this to trigger syncs with the backend
     */
    useEffect(() => {
      if (nodeChanges === 0) 
        return

      const rootNode = getNodes()[0];
      console.log("Children: ", graph.children(rootNode.id));
      console.log("ROOT NODE: ", rootNode);

      const updateRoot = graph.RFtoJSON(rootNode);
      backend.updateGraph(updateRoot);
    }, [nodeChanges])

    /**
     * Syncs graph with updated node 
     */
    const genSubGraph = (nodeId: string): void => {
      const subgraph = graph.RFtoJSON(nodeId);

      backend.genSubGraph(subgraph).then((res) => {
        const {newNodes, newEdges} = graph.processJson(res.data);

        setNodes(newNodes);
        setEdges(newEdges);
      })
    } 

    const saveGraph = (title: string): void => {
      const rootNode = getNodes()[0];
      console.log("Saving graph: ", rootNode);

      const updateRoot = graph.RFtoJSON(rootNode);
      backend.saveGraph(updateRoot, title);

    }
 
    const globalValue = useMemoObject<Global>({
      reactFlowWrapper,
      showHideUnattachedChildren,
      setSelectedNode,
      downloadGraph,
      genSubGraph,
      deleteNode,
      modifyNodeTitle,
      saveGraph
    });

    const globalVolatileValue = useMemoObject({
      selecteNodeID,
    });

    return (
      <GlobalVolatileContext.Provider value={globalVolatileValue}>
        <GlobalContext.Provider value={globalValue}>
          {children}
        </GlobalContext.Provider>
      </GlobalVolatileContext.Provider>
    );
  }
);

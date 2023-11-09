import React, { 
    memo, 
    useCallback, 
    useEffect,
    useRef,
    useMemo
  } from "react";
import { createContext, useContext } from "use-context-selector";
import { useMemoObject } from "../../common/hooks/useMemo";
import { 
  useReactFlow, 
  Node,
  Edge
} from "reactflow";
import { TreeUtils } from "../graph/tree/treeUtils";
import { 
  RFNodeData,
  NodeType
} from "../../common/common-types";

import {
  ChangeCounter,
  nextChangeCount,
  useChangeCounter,
  wrapRefChanges,
} from '../../common/hooks/useChangeCounter';

import { SetState } from "../../common/common-types";

import { GraphType } from "../data/processNodes";
import { BackendContext } from "./backendProvider";
import { AxiosResponse } from "axios";

// Should just get rid of processNodes
// import { CreateTreeNode, CreateTreeEdge } from "../data/processNodes";
import { CreateNode, CreateEdge } from "../data/processTree";
interface TreeEditMap {
  downloadGraph: (graphID: string, graphType: GraphType) => void;
  genSubGraph: (nodeId: string) => Promise<AxiosResponse>;
  modifyNodeTitle: (nodeId: string, newTitle: string) => void;
  deleteNode: (nodeId: string) => void;
  saveGraph: (title: string) => void;
  genGraphDesc: (graphId: string) => Promise<AxiosResponse>;
  collapseNodes: (parentId: string, expand: boolean) => void;
  addNode: (parentId: string) => void;
  nodesWithoutDescr: number;
}

export const TreeEditMapContext = createContext<Readonly<TreeEditMap>>({} as TreeEditMap);
export const TreeEditMapProvider = memo(
({
  children,
}: React.PropsWithChildren) => {
  const [nodeChanges, addNodeChanges, nodeChangesRef] = useChangeCounter();
  const [edgeChanges, addEdgeChanges, edgeChangeRef] = useChangeCounter();

  const { backend } = useContext(BackendContext);
  const { 
    setNodes, 
    setEdges, 
    getNodes, 
    getEdges, 
  } = useReactFlow();

  let nodesWithoutDescr = useRef<number>(0);

  const graph = useRef(new TreeUtils(getNodes, getEdges)).current;
  const setNodesRef = useRef<SetState<Node<any>[]>>(setNodes);
  const setEdgeRef = useRef<SetState<Edge<any>[]>>(setEdges);

  const changeNodes = useMemo(
    () => wrapRefChanges(setNodesRef, addNodeChanges),
    [addNodeChanges]
  );
  const changeEdges = useMemo(
    () => wrapRefChanges(setEdgeRef, addEdgeChanges),
    [addEdgeChanges]
  )
  
  const downloadGraph = (graphId: string, graphType: GraphType) => {
    backend.downloadGraph(graphId)
      .then((res) => {
        // represents the order of nodes in JSON format
        let {newNodes, newEdges} = graph.initJson(res.data, graphType);
        
        changeNodes(newNodes);
        changeEdges(newEdges);
      })
      .catch(error => {
        console.error("Error fetching graph error: ", error);
        throw error;
      })
  }

  // maybe this should go into graph utils, since this generic to all nodes
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
  
  // const modifyNodes = useCallback((modNodes: Node<RFNodeData>[]) => {
  //   const newNodes: Node<RFNodeData>[] = [];
  //   for (const oldNode of getNodes()) {
  //     const modify = modNodes
  //       .map(node => node.id)
  //       .includes(oldNode.id)
  //     newNodes.push(
  //       modify
  //       // double loop here not ideal but looks nicer 
  //       ? modNodes.find(node => node.id === oldNode.id)
  //       : oldNode
  //     )
  //   }
  //   return newNodes;
  // }, [getNodes])

  /**
   * Modifies the node title
   */
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
      const { childNodes: children } = graph.getAllChildren(id);
      const deleteNodes = [children, node].flat();
      const newNodes = getNodes()
        .filter((node) => 
          !deleteNodes
            .map(node => node.id)
            .includes(node.id)
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
      
      const newEdges = getEdges()
        .filter((edge) => 
          !deleteNodes
            .map(node => node.id)
            .includes(edge.target)
        )

      changeEdges(newEdges);
      changeNodes(newNodes);
    }, [changeNodes]
  )

  /**
   * Add blank node before current node
   */
  const addNode = useCallback(
    (currId: string): void => {
      const currNode = graph.findNodeRF(currId);
      const currEdge = graph.findEdge(currId);
      const { 
        beforeNodes,
        beforeEdges,
        afterNodes,
        afterEdges
      } = graph.getNodesBeforeAfter(currId, 0);
      
      const insertNode = CreateNode({
        data: {
          title: ""
        },
        type: NodeType.TreeNode,
        hidden: false,
        position: {
          x : currNode.position.x,
          y: currNode.position.y
        }
      });

      const insertEdge = CreateEdge({
        target: insertNode.id,
        source: graph.parent(currId).id
      });

      const newNodes = beforeNodes
        // we want to swap the order of the nodes
        .concat(insertNode)
        .concat(currNode)
        // .concat(currNode)
        .concat(afterNodes)
        .map((node, index) => ({
          ...node,
          position: {
            x : node.position.x,
            y : index * 70
          }
        })
      );

      const newEdges = beforeEdges
        .concat(insertEdge)
        .concat(currEdge)
        .concat(afterEdges);
    
      changeNodes(newNodes);
      changeEdges(newEdges);
  }, [changeNodes, changeEdges]);
  
  /**
   * Hides all children nodes
   */
  const collapseNodes = useCallback(
    (parentId: string, collapsed: boolean): void => {
      const parentNode = graph.findNodeRF(parentId);
      const parentEdge = graph.findEdge(parentId);

      let newNodes = [];
      let newEdges = [];
      if (!collapsed) {
        const { childNodes, childEdges } = graph.getAllChildren(parentId);

        graph.saveCollapsedNodes(parentId, childNodes, childEdges);

        console.log("Expanding nodes: ", childNodes.length);
        const {
          beforeNodes,
          beforeEdges,
          afterNodes,
          afterEdges
        } = graph.getNodesBeforeAfter(parentId, childNodes.length);
        
        newNodes = beforeNodes
          .concat(parentNode)
          .concat(afterNodes)
          .map((node, index) => ({
            ...node,
            position: {
              x : node.position.x,
              y : index * 70
            }
          }));

        newEdges = beforeEdges
            .concat(parentEdge)
            .concat(afterEdges);

      } else {
        const { savedNodes, savedEdges } = graph.getCollapsedNodes(parentId);
        const {
          beforeNodes,
          beforeEdges,
          afterNodes,
          afterEdges
        } = graph.getNodesBeforeAfter(parentId, 0);

        console.log("Expanding nodes: ", savedNodes.length);
        
        newNodes = beforeNodes
          .concat(parentNode)
          .concat(savedNodes)
          .concat(afterNodes)
          .map((node, index) => ({
            ...node,
            position: {
              x : node.position.x,
              y : index * 70
            }
          }));
  
        newEdges = beforeEdges
            .concat(parentEdge)
            .concat(savedEdges)
            .concat(afterEdges);
      }

      changeNodes(newNodes);
      changeEdges(newEdges);
  }, [changeNodes, changeEdges]);


  // const collapseNodes = useCallback(
  //   (parentId: string, collapsed: boolean): void => {
  //     const direction = collapsed ? 1 : -1;

  //     const parentNode = graph.findNodeRF(parentId);
  //     const parentEdge = graph.findEdge(parentId);
  //     const { childNodes: nodesCollapsed, childEdges } = graph.getAllChildren(parentId);
  //     const collapsedNodeIds = nodesCollapsed.map(node => node.id);

  //     const {
  //       beforeNodes,
  //       beforeEdges,
  //       afterNodes,
  //       afterEdges
  //     } = graph.getNodesBeforeAfter(parentId, nodesCollapsed.length);
      
  //     const newNodes = beforeNodes
  //       .concat(parentNode)
  //       .concat(nodesCollapsed.map(node => (
  //         {
  //           ...node,
  //           hidden: !collapsed
  //         }
  //       )))
  //       .concat(afterNodes.map(node => (
  //         {
  //           ...node,
  //           position: {
  //             x: node.position.x,
  //             y: node.position.y + nodesCollapsed.length * 70 * direction
  //           }
  //         }
  //       )));
      
  //     const newEdges = beforeEdges
  //         .concat(parentEdge)
  //         .concat(
  //           getEdges()
  //             .filter(edge => collapsedNodeIds.includes(edge.target))
  //             .map(edge => (
  //               {
  //                 ...edge,
  //                 hidden: !collapsed
  //               }
  //             ))
  //         )
  //         .concat(afterEdges);

  //     changeNodes(newNodes);
  //     changeEdges(newEdges);
  // }, [changeNodes, changeEdges]);

  /**
   * Sync backend
   */
  useEffect(() => {
    if (nodeChanges === 0) 
      return

    const rootNode = getNodes()[0];
    const updateRoot = graph.RFtoJSON(rootNode);
    backend.updateGraph(updateRoot);
  }, [nodeChanges, edgeChanges])

  /**
   * Update nodes without description
   */
  useEffect(() => {
    nodesWithoutDescr.current = getNodes().filter(node => node.data.description === "").length
  }, [nodeChanges])

  /**
   * Syncs graph with updated node 
   */
  const genSubGraph = (nodeId: string): Promise<AxiosResponse> => {
    return new Promise((resolve, reject) => {
      const subgraph = graph.RFtoJSON(nodeId);
      const rootId = getNodes()[0].id;
      console.log("Subgraph: ", subgraph);
  
      backend.genSubGraph(subgraph, rootId)
        .then((res) => {
          const {
            updateNodes, 
            updateEdges
          } = graph.updateSubtreeJson(res.data);
  
          changeNodes(updateNodes);
          changeEdges(updateEdges);
          resolve(res.data);
        })
        .catch((err) => {
          console.error("Error from server: ", err);
          reject(err);
        });
    });
  };
  
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
    genGraphDesc,
    collapseNodes,
    addNode,
    nodesWithoutDescr: nodesWithoutDescr.current
  });
  
  return (
    <TreeEditMapContext.Provider value={globalValue}>
        {children}
    </TreeEditMapContext.Provider>
  );
}
);

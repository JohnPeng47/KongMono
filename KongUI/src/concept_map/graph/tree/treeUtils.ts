import { Node, Edge } from "reactflow";
import {
  RFNodeData,
  BackendNode,
  Position,
  NodeID,
  RFNode
} from "../../../common/common-types"
import {
  GraphType,
  ConvertNode,
  ConvertEdge
} from "../../data/processNodes";
import { NumberLiteralType } from "typescript";

type DFSNode = {
  node: BackendNode | Node<RFNodeData>
  depth: number
  nodeIndex: number
  parentId: NodeID
}
type NumChildren = number;

/**
 * Utility functions for read-only graph level functions
 * Does not support modification of RF node state
 */
export class TreeUtils {
  private getNodes: () => Node<any>[];
  private getEdges: () => Edge<any>[];
  private X_INTERVAL = 50;
  private Y_INTERVAL = 70;

  // Is this consistent with RF getNodes()??
  private nodeDepth: { [NodeID: NodeID]: number };
  
  private savedCollapsedNodes: { 
    [parentID: NodeID]: {
      savedNodes: Node<RFNodeData>[],
      savedEdges: Edge[]
   }
  };

  public constructor(
    getNodes: () => Node<any>[],
    getEdges: () => Edge<any>[]) {

    this.getNodes = getNodes;
    this.getEdges = getEdges;
    this.nodeDepth = {};
    this.savedCollapsedNodes = {};
  }

  /**
   * DFS implementation
   */
  private DFS(root: any): DFSNode[] {
    let nodeIndex = this.getNodeIndex(root.id);

    let traversalOrder: DFSNode[] = [];
    let stack = [[root, 0, root.id]]; // Assuming root is the starting node, at depth 0 with no parent.

    while (stack.length > 0) {
      const [currNode, depth, parentId] = stack.pop();

      // Add the current node to the traversal order
      traversalOrder.push({
        node: currNode,
        depth: depth,
        parentId: parentId,
        nodeIndex: nodeIndex
      });

      // Assuming that children are stored in currNode.data.children
      this.children(currNode).forEach((child) => {
        stack.push([child, depth + 1, currNode.id]);
      });
    }

    return traversalOrder;
  }

  /**
   * Initializes RFNodes attr such as positions from
   * initial server JSON and keeps track of position and depth
   */
  public initJson = (
    json: BackendNode,
    graphType: GraphType
  ): {
    newNodes: Node<RFNodeData>[];
    newEdges: any[]
  } => {
    const newNodes = [];
    const newEdges = [];
    let [depth, parentId, nodeIndex] = [0, json.id, 0];

    const stack: Array<[BackendNode, number, string]> = [[json, depth, parentId]];

    // return empty nodes and edges
    if (!json) {
      return { newNodes, newEdges };
    }

    while (stack.length > 0) {
      const [currNode, depth, parentId] = stack.pop();
      const rfNode = ConvertNode(currNode, graphType);
      const rfEdge = ConvertEdge(currNode, parentId, graphType);

      // determine initial node position
      const position = this.nodePosInit(depth, nodeIndex);
      rfNode.position = position;

      //node has not been seen by us before
      newNodes.push(rfNode);

      // save node positions/depths/order
      this.updateNodeState(currNode.id, depth, nodeIndex);

      // all nodes not root
      if (parentId !== currNode.id)
        newEdges.push(rfEdge);

      this.children(currNode).forEach((child) => {
        stack.push([child, depth + 1, currNode.id]);
      })

      nodeIndex += 1;
    }

    return { newNodes, newEdges };
  };

  /**
   * Takes an update to the existing RFNode state initialized by
   * initJson, and updates position while keeping all the pre-existing
   * nodes in the same fixed position
   * 
   * In the future, support add node with this interface
   */
  public updateSubtreeJson = (
    parentNode: BackendNode,
  ): {
    updateNodes: Node<RFNodeData>[];
    updateEdges: any[];
  } => {
    // return empty nodes and edges
    if (!parentNode) {
      return {
        updateNodes: [],
        updateEdges: []
      };
    }
    const { childNodes } = this.getAllChildren(parentNode.id);
    const numChildrenBefore = childNodes.length
    console.log("New nodes: ", this.numNewNodes(parentNode));

    let numChildren = 0;
    let nodeIndex = this.getNodeIndex(parentNode.id);

    if (nodeIndex < 0)
      throw Error("Missing sibling or parent node");

    // let depth = this.nodeDepth[parentNode.id];
    let depth = this.getNodeDepth(parentNode.id);
    const stack: Array<[BackendNode, number, string]> = [[parentNode, depth, parentNode.id]];

    // nodes that came before, not including the parent
    const oldNodes = this.getNodes().slice(0, nodeIndex);
    const oldEdges = this.getEdges().slice(0, nodeIndex - 1);

    // these are new nodes added from the update
    const updateNodes = [];
    const updateEdges = [];

    // nodes that comes after the last children of the parent node
    let repoNodes = this.getNodes().slice(nodeIndex + numChildrenBefore + 1);
    let repoEdges = this.getEdges().slice(nodeIndex + numChildrenBefore - 1 + 1);

    while (stack.length > 0) {
      const [currNode, depth, parentId] = stack.pop();

      const rfNode = this.getNodeIndex(currNode.id) < 0
        ? ConvertNode(currNode, "Tree")
        : this.findNodeRF(currNode.id)
      const rfEdge = this.getNodeIndex(currNode.id) < 0
        ? ConvertEdge(currNode, parentId, "Tree")
        : this.findEdge(currNode.id)

      // determine initial node position
      const position = this.nodePosInit(depth, nodeIndex);
      rfNode.position = position;

      // save node positions/depths/order
      this.updateNodeState(currNode.id, depth, nodeIndex);

      updateNodes.push(rfNode);
      updateEdges.push(rfEdge);

      this.children(currNode).forEach((child) => {
        stack.push([child, depth + 1, currNode.id]);
      })

      nodeIndex += 1;
      numChildren += 1;
    }

    // shift position
    repoNodes = repoNodes.map((node) => ({
      ...node,
      position: {
        x: node.position.x,
        y: node.position.y + (numChildren - numChildrenBefore - 1) * this.Y_INTERVAL
      }
    }))

    // that the order of setNodes does not matter
    return {
      updateNodes: oldNodes.concat(updateNodes).concat(repoNodes),
      updateEdges: oldEdges.concat(updateEdges).concat(repoEdges)
    };
  };

  /**
   * Finds the new nodes being added recursively
   */
  private numNewNodes(newNode: BackendNode): number {
    let newNodes = 0;
    for (let dfs of this.DFS(newNode)) {
      if (!this.findNodeRF(dfs.node.id))
        newNodes += 1;
    }

    return newNodes;
  }

  /**
   * We break up the updating the internal RF state
   * since individually calling setNode/edge would 
   * be very expensive (actually not sure if true, but
   * either way, its implementation is not much different).
   * Also this gives us the benefit of keeping the setNode/Edge
   * calls in the provider impl
   */
  // private insertNode(
  //   node: Node<RFNodeData>
  // ): {
  //   updatedNodes: Node<RFNodeData>[]
  // } {
  //   return null;
  // }

  // /**
  //  * Recalculates the positions of old nodes based on a single node deletion
  //  */
  // private deleteNodeUpdate (
  //   nodeId: NodeID
  // ): {
  //   nodeUpdates: nodeUpdate[],
  // } {
  //   const nodeUpdates: nodeUpdate[] = [];
  //   const edgeUpdates: postUpdate[] = [];

  //   const {
  //     beforeNodes, 
  //     afterNodes, 
  //     beforeEdges, 
  //     afterEdges
  //   } = this.getNodesBeforeAfter(nodeId);

  //   for (const node of beforeNodes) {
  //     nodeUpdates.push({
  //       nodeId: node.id,
  //       yOffsetUpdate: 0
  //     })
  //   }

  //   for (const node of afterNodes) {
  //     nodeUpdates.push({
  //       nodeId: node.id,
  //       yOffsetUpdate: this.Y_INTERVAL
  //     })
  //   }

  //   return {
  //     nodeUpdates
  //   }
  // }

  // private updatePos(
  //   updateNodes: Node<RFNodeData>,
  //   yOffset: number
  // ):{
  //   updateNodes: Node<RFNodeData>
  // } {
  //   return null;
  // }

  /**
   * Returns nodes and edges that came before the current node
   */
  public getNodesBeforeAfter(nodeId: NodeID, numNodes: number)
    : {
      beforeNodes: any,
      beforeEdges: any,
      afterNodes: any,
      afterEdges: any
    } {
    const nodeIndex = this.getNodeIndex(nodeId);
    // nodes that came before, not including the parent
    const beforeNodes = this.getNodes().slice(0, nodeIndex);
    const beforeEdges = this.getEdges().slice(0, nodeIndex - 1);

    // nodes that comes after the last children of the parent node
    let afterNodes = this.getNodes().slice(nodeIndex + numNodes + 1);
    let afterEdges = this.getEdges().slice(nodeIndex + numNodes + 1 - 1);

    return {
      beforeNodes,
      beforeEdges,
      afterNodes,
      afterEdges
    }
  }

  /**
   * Adds node at the same level, before the current node
   * Todo: add it at specific index
   */
  // private addNode(
  //   nodeId: string,
  //   node: RFNode
  // ): { updateNodes, updateEdges } {
  //   const nodeAdded = 1;

  //   const nodeIndex = this.getNodeIndex(nodeId);
  //   const parentNode = this.parent(nodeId);

  //   const rfEdge = CreateEdge(node, parentNode.id, "Tree");

  //   if (nodeIndex < 0)
  //     throw Error("Missing sibling or parent node");


  //   // nodes that comes after the last children of the parent node
  //   let afterNodes = this.getNodes().slice(nodeIndex + 1 + nodeAdded);
  //   let afterEdges = this.getEdges().slice(nodeIndex - 1 + 1 + nodeAdded);

  //   return {
  //     beforeNodes,
  //     beforeEdges,
  //     afterNodes,
  //     afterEdges
  //   }
  // }

  /**
   * Save collapse nodes and edges
   */
  public saveCollapsedNodes(parentId: NodeID, nodes: Node<RFNodeData>[], edges: Edge[]): void {
    this.savedCollapsedNodes[parentId] = {
      savedNodes: nodes,
      savedEdges: edges
    }
  }

  /**
   * Restore collapsed nodes and edges
   */
  public getCollapsedNodes(parentId: NodeID):
  {
    savedNodes: Node<RFNodeData>[],
    savedEdges: Edge[]
  } {
    const savedNodes = this.savedCollapsedNodes[parentId];
    delete this.savedCollapsedNodes[parentId];

    return savedNodes;
  }


  /**
   * Calculates the position of a node during initJson
   */
  private nodePosInit(depth: number, nodeIndex: number): Position {
    const position = {
      x: this.X_INTERVAL * depth,
      y: this.Y_INTERVAL * nodeIndex
    }
    return position;
  }

  /**
   * Updates internal node depth and node index
   * TODO: handle case when update is root node
   */
  private updateNodeState(
    nodeId: NodeID,
    depth: number,
    nodeIndex: number
  ): void {
    this.nodeDepth[nodeId] = depth;
    // this actually 
    // this.nodeIndices[nodeId] = nodeIndex;
  }

  /**
   * Find depth
   */
  public getNodeDepth(nodeId: NodeID): number {
    const rootNode = this.root();
    const traverseNodes = this.DFS(rootNode);

    // console.log(traverseNodes);
    for (let dfs of traverseNodes) {
      console.log("t node: ", dfs.node.data.title);
      if (dfs.node.id === nodeId)
        return dfs.depth
    }

    // TODO: figure out why this code below yields an error for below
    // const depth = traverseNodes
    //   .find(dfs => dfs.node.id === nodeId)?.depth;
    // if (depth)
    //   return depth;

    throw Error(`Depth for node: ${nodeId} not found`);
  }

  /**
   * Returns all the nodes that come after the currNode
   * TODO: change this to support collapsed nodes
   */
  private getNodeIndex(nodeId: NodeID): number {
    return this.getNodes().findIndex(node => node.id === nodeId);
  }

  /**
   * Gets the immediate children
   */
  public children(node: NodeID): Node<RFNodeData>[];
  public children(node: BackendNode): BackendNode[];
  public children(node: any): any {
    // BackendNode
    if (typeof node !== "string")
      return node.data.children

    // RFNode
    const nodeId = node;
    const childIds = this.getEdges()
      .filter(edge => edge.source === nodeId)
      .map(edge => edge.target)

    return this.getNodes().filter(node => childIds.includes(node.id));
  }

  /**
   * Recursively retrieves all the child nodes
   */
  public getAllChildren(nodeId: string): {
    childNodes: Node<RFNodeData>[],
    childEdges: Edge[] 
  } {    
    return {
      childNodes: this.children(nodeId).flatMap(child => {
        return [child, ...this.getAllChildren(child.id).childNodes];
      }),
      childEdges: this.children(nodeId).flatMap(child => {
        return [this.findEdge(child.id), ...this.getAllChildren(child.id).childEdges]
      })
    }

  }

  /**
   * Finds and returns the edge leading to the target node
   */
  public findEdge(nodeId: string): Edge | undefined {
    return this.getEdges()
      .find((edge) => edge.target === nodeId)
  }

  /**
   * Returns node by ID using GetNodes
   * Theoretically, both method should be consistent but still
   */
  public findNodeRF(nodeId: string): Node<RFNodeData> | undefined {
    return this.getNodes()
      .find((node) => node.id === nodeId)
  }

  /**
   * Returns the root node
   */
  public root(): Node<RFNodeData> | undefined {
    if (this.getNodes().length === 0)
      throw Error("Get nodes returned zero, no nodes in graph")

    return this.getNodes()[0]
  }

  /**
  * Returns JSON reprentation of node
  */
  public RFtoJSON(node: string): any;
  public RFtoJSON(node: Node<RFNodeData>): any;
  public RFtoJSON(node: any): any {
    if (typeof node === 'string') {
      node = this.findNodeRF(node);
      if (!node) {
        throw Error(`Node id: {node} does not exist`)
      }
    }

    // console.log("RF NODE: ", node.data.title);
    const nodeId = node.id;
    const children = this.children(nodeId);
    node.data.children = [];

    children.forEach((child) => {
      const childNode = this.RFtoJSON(child);
      if (node) {
        node.data.children.push(childNode);
      }
    });

    return node;
  }

  /**
  * Returns siblings
  */
  public siblings(nodeId: string): Node<RFNodeData>[] {
    const parentId = this.parent(nodeId).id;

    return this.getNodes()
      .filter((node) =>
        this.getEdges()
          .filter((edge) => edge.source === parentId)
          .map((edge) => edge.target)
          .some((id) => id === node.id) && node.id !== nodeId
      )
  }

  /**
  * Returns the parent node
  */
  public parent(nodeId: string): Node<RFNodeData> {
    const edgeFromParent = this.getEdges()
      // TODO: there issue around deleting root
      .find((edge) => edge.target === nodeId);

    if (!edgeFromParent) {
      // only way this should fail if nodeId is rootId
      return this.root();
    }

    return this.findNodeRF(edgeFromParent.source);
  }
}


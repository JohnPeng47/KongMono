import { Node, Edge } from "reactflow";
import {
  RFNodeData,
  BackendNode,
  Position,
  NodeID
} from "../common/common-types"
import {
  GraphType,
  CreateEdge,
  CreateNode
} from "../data/processJson";

/**
 * Utility functions for read-only graph level functions
 * Does not support modification of RF node state
 */
export class GraphUtils {
  private getNodes: () => Node<any>[];
  private getEdges: () => Edge<any>[];
  private X_INTERVAL = 50;
  private Y_INTERVAL = 70;

  // Is this consistent with RF getNodes()??
  private nodeDepth: { [NodeID: NodeID]: number };

  public constructor(
    getNodes: () => Node<any>[],
    getEdges: () => Edge<any>[]) {

    this.getNodes = getNodes;
    this.getEdges = getEdges;
    this.nodeDepth = {};
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
      const rfNode = CreateNode(currNode, graphType);
      const rfEdge = CreateEdge(currNode, parentId, graphType);

      // determine initial node position
      const position = this.nodePosInit(depth, nodeIndex);
      rfNode.position = position;

      //node has not been seen by us before
      newNodes.push(rfNode);

      // save node positions/depths/order
      this.nodeDepth[currNode.id] = depth;

      // all nodes not root
      if (parentId !== currNode.id)
        newEdges.push(rfEdge);

      currNode.data.children.forEach((child) => {
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
  public updateJson = (
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

    const numChildrenBefore = this.getAllChildren(parentNode.id).length

    let numChildren = 0;
    let nodeIndex = this.getNodeIndex(parentNode.id);
    // let nodeIndex = lastSibling
    //   // either last sibling or parent if no sibling
    //   ? this.getNodeIndex(lastSibling.id)
    //   : this.getNodeIndex(parentNode.id);

    console.log("Parent Node: ", parentNode);
    console.log("Num children: ", numChildrenBefore);
    console.log("Children: ", this.getAllChildren(parentNode.id));

    if (nodeIndex < 0)
      throw Error("Missing sibling or parent node");

    let depth = this.nodeDepth[parentNode.id];
    // need to change this if 
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

    // source of error when repo nodes length is zero
    // console.log("RepoNodes: ", "Nodeid: ", repoNodes[0], ", Title: ", repoNodes[0].data.title,
    //   "NodeIndex: ", nodeIndex + numChildrenBefore + 1, "End Index: ", nodeIndex + numChildrenBefore + 1 + repoNodes.length);

    while (stack.length > 0) {
      const [currNode, depth, parentId] = stack.pop();

      const rfNode = this.getNodeIndex(currNode.id) < 0
        ? CreateNode(currNode, "Tree")
        : this.findNodeRF(currNode.id)
      const rfEdge = this.getNodeIndex(currNode.id) < 0
        ? CreateEdge(currNode, parentId, "Tree")
        : this.findEdge(currNode.id)

      // determine initial node position
      const position = this.nodePosInit(depth, nodeIndex);
      rfNode.position = position;

      // save node positions/depths/order
      this.nodeDepth[currNode.id] = depth;

      updateNodes.push(rfNode);
      updateEdges.push(rfEdge);

      currNode.data.children.forEach((child) => {
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
   * Calculates the position of a node during updateJson
   * TODO: handle case when update is root node
   */
  private updateNodeStats(nodeId: NodeID): Position {
    const parent = this.parent(nodeId);
    if (!parent) {
      throw Error("This node should have a parent");
    }

    return null;
  }

  /**
   * Returns all the nodes that come after the currNode
   */
  private nodesAfter(nodeId: NodeID): [NodeID] {
    return null;
  }

  /**
   * Returns all the nodes that come after the currNode
   */
  private getNodeIndex(nodeId: NodeID): number {
    return this.getNodes().findIndex(node => node.id === nodeId);
  }

  /**
   * Gets the immediate children
   */
  public children(nodeId: string): Node<RFNodeData>[] {
    const childIds = this.getEdges()
      .filter(edge => edge.source === nodeId)
      .map(edge => edge.target)

    return this.getNodes().filter(node => childIds.includes(node.id));
  }

  /**
   * Recursively retrieves all the child nodes
   */
  public getAllChildren = (nodeId: string): Node<RFNodeData>[] => {
    return this.children(nodeId).flatMap(child => {
      return [child, ...this.getAllChildren(child.id)];
    })
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
      return this.getNodes()[0];
    }

    return this.findNodeRF(edgeFromParent.source);
  }
}


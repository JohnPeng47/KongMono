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
  private Y_INTERVAL = 50;

  // Is this consistent with RF getNodes()??
  private depthNodes: NodeID[][];
  private rootNode: Node<RFNodeData>;

  public constructor(
    getNodes: () => Node<any>[],
    getEdges: () => Edge<any>[]) {

    this.getNodes = getNodes;
    this.getEdges = getEdges;
    this.rootNode = this.getNodes()[0];
    this.depthNodes = [];
  }

  /**
   * Takes JSON response from the server and converts it
   * into RFNode format. 
   * - initialNodes/initialEdges are pre-existing nodes that have 
   * attr updated but dont' need to be repositioned
   * - newNodes/newEdges are new nodes/edges that need to have their
   * positions updated
   */
  public processJson = (
    json: BackendNode,
  ): {
    updateNodes: Node<RFNodeData>[];
    updateEdges: any[];
    newNodes: Node<RFNodeData>[];
    newEdges: any[]
  } => {

    const updateNodes = [];
    const updateEdges = [];
    const newNodes = [];
    const newEdges = [];
    let [depth, parentId] = [0, json.id]

    const stack: Array<[BackendNode, number, string]> = [[json, depth, parentId]];

    // return empty nodes and edges
    if (!json) {
      return { updateNodes, updateEdges, newNodes, newEdges };
    }

    while (stack.length > 0) {
      const [currNode, depth, parentId] = stack.pop();
      const rfNode = CreateNode(currNode, "Tree");
      const rfEdge = CreateEdge(currNode, parentId, "Tree");

      // node has not been seen by us before
      if (!this.findNodeDepth(currNode.id)) {
        newNodes.push(rfNode);

        // create a new depth index to hold nodes
        if (this.depthNodes.length < depth + 1) {
          this.depthNodes.push([currNode.id])
        }
        else {
          this.depthNodes[depth].push(currNode.id)
        }

        // all nodes not root
        if (parentId !== currNode.id)
          newEdges.push(rfEdge);
      } else {
        updateNodes.push(rfNode);
        updateEdges.push(rfEdge);
      }

      currNode.data.children.forEach((child) => {
        stack.push([child, depth + 1, currNode.id]);
      })
    }

    return { updateNodes, updateEdges, newNodes, newEdges };
  };

  // public processJson = (
  //   json: BackendNode,
  //   opType: GraphType = "ConceptMap"
  // ): { initialNodes: any[]; initialEdges: any[] } => {
  //   const initialNodes = [];
  //   const initialEdges = [];
  //   const newNodes = [];
  //   const removedNodes = [];

  //   // only populate nodesPos on initial render
  //   const initialRender = this.nodesPos.length === 0 ? true : false;

  //   let [depth, count, parentId] = [0, 0, json.id]

  //   const stack: Array<[BackendNode, number, string]> = [[json, depth, parentId]];

  //   // return empty nodes and edges
  //   if (!json) {
  //     return { initialNodes, initialEdges };
  //   }

  //   while (stack.length > 0) {
  //     const [currNode, depth, parentId] = stack.pop();
  //     let node = CreateNode(currNode, opType);

  //     node.position = this.nodePosition(depth, count);

  //     // save list of node ids indexed by depth 
  //     if (initialRender) {
  //       if (this.nodesPos.length < depth + 1) {
  //         this.nodesPos.push([currNode.id])
  //       }
  //       else {
  //         this.nodesPos[depth].push(currNode.id)
  //       }
  //     } else {

  //     }

  //     initialNodes.push(CreateNode(currNode, opType));

  //     // all nodes not root
  //     if (parentId !== currNode.id)
  //       initialEdges.push(CreateEdge(currNode, parentId, opType));

  //     currNode.data.children.forEach((child) => {
  //       stack.push([child, depth + 1, currNode.id]);
  //     })

  //     count += 1;
  //   }

  //   this.nodesPos.forEach((level, index) => console.log(`Depth {index}: `, level))

  //   return { initialNodes, initialEdges };
  // };


  /**
   * Calculates the position of a node
   */
  private nodePosition(depth: number, nodeIndex: number): Position {
    return {
      x: this.X_INTERVAL * depth,
      y: this.Y_INTERVAL * nodeIndex
    }
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
   * Returns node by ID using GetNodes
   * Theoretically, both method should be consistent but still
   */
  public findNodeRF(nodeId: string): Node<RFNodeData> | undefined {
    return this.getNodes()
      .find((node) => node.id === nodeId)
  }

  /**
   * Returns node by ID using 
   * Theoretically, both method should be consistent but still
   */
  public findNodeDepth(nodeId: string): number | undefined {
    return this.depthNodes[nodeId];
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

  // private mergeUpdateNodePositions(newNodes: Node<RFNodeData>)

  // public siblings(nodeId: string): Node<RFNodeData>[] {
  //   const parentId = this.parent(nodeId).id;
  //   return this.getNodes()
  //     .filter((node) =>
  //       this.getEdges()
  //         .filter((edge) => edge.source === parentId)
  //         .map((edge) => edge.target)
  //         .some((id) => id === node.id) && node.id !== nodeId
  //     )
  // }

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


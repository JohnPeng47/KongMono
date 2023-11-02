import axios, { AxiosResponse } from "axios";
import {
  RFEdge,
  RFNodeData,
  BackendNode,
} from "./common-types";
import { Node } from "reactflow";
// import { mergeOverwite } from "./utils";

const backendCache = new Map<string, Backend>();

/**
 * Returns a cached backend instance.
 *
 * Given the same URL, this function guarantees that the same instance is returned.
 */
export const getBackend = (url: string): Backend => {
  let instance = backendCache.get(url);
  if (instance === undefined) {
    instance = new Backend(url);
    backendCache.set(url, instance);
  }
  return instance;
};

export class Backend {
  readonly url: string
  // stores nodes with only child ids
  private nodes: BackendNode;
  private readonly mergeFields: string[] = [
    "title"
  ]

  constructor(url: string) {
    this.url = url;
  }

  /**
   * Syncs with nodes state from globalProvider and pushes update to 
   * server, a single node at a time
   */
  genSubGraph(
    subgraph: Node<RFNodeData>): Promise<AxiosResponse> {
    // this.syncGraph(rfNode);
    // this should have the latest sync'd data from the rf node
    const endpoint = this.url + "/gen/subgraph";

    // return null;
    return axios.post(endpoint, subgraph);
  }

  /**
   * Updates the entire graph viaootNode
   */
  updateGraph(
    rootNode: Node<RFNodeData>): void {
    const endpoint = this.url + "/graph/update"

    axios.post(endpoint, rootNode);
  }

  /**
   * Delete graph 
   */
  deleteGraph(
    graphId: string): void {
    const endpoint = this.url + "/graph/delete/" + graphId

    axios.get(endpoint);
  }

  /**
   * Delete graph 
   */
  saveGraph(
    rootNode: Node<RFNodeData>,
    title: string): void {
    const endpoint = this.url + "/graph/save"
    const data = {
      "title": title,
      "graph": rootNode
    }

    axios.post(endpoint, data);
  }

  /**
   * Downloads graph from server
   */
  async downloadGraph(
    graphId: string): Promise<AxiosResponse> {
    const endpoint = this.url + "/graph/" + graphId;

    return axios.get(endpoint);
  }

  /**
   * Downloads graph from server
   */
    async genGraphDesc(graphId: string): Promise<AxiosResponse> {
      const endpoint = this.url + "/graph/generate/" + graphId;
  
      return axios.get(endpoint);
    }
}


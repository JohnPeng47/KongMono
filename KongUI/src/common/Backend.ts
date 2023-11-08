import axios, { AxiosResponse, AxiosRequestConfig } from "axios";
import {
  RFEdge,
  RFNodeData,
  BackendNode,
} from "./common-types";
import { Node } from "reactflow";
import { useNavigate } from "react-router-dom";

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
  private token: string | null = null;
  private nodes: BackendNode;
  private authConf: AxiosRequestConfig = { headers: {}};

  constructor(url: string) {
    this.url = url;
    const token = localStorage.getItem("token");
    if (token) {
      this.authConf = this.addBearerToConf(token);
    }
  }

  /**
    * Adds Bearer token to conf
  */
  private addBearerToConf(token: string): AxiosRequestConfig {
    return {
      ...this.authConf,
      headers: {
        ...this.authConf.headers,
        Authorization : `Bearer ${token}`
      }
    }
  }

  /**
   * Syncs with nodes state from globalProvider and pushes update to 
   * server, a single node at a time
   */
  genSubGraph(
    subgraph: Node<RFNodeData>,
    graphId: string): Promise<AxiosResponse> {
    // this.syncGraph(rfNode);
    // this should have the latest sync'd data from the rf node
    const endpoint = this.url + `/gen/subgraph/${graphId}`;
    const data = {
      subgraph: subgraph
    }

    return axios.post(endpoint, data);
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

  /**
   * Downloads graph from server
   */
  async login(email: string, password: string): Promise<string | Boolean> {
    const endpoint = this.url + "/authenticate";
    const data = {
      email: email,
      password: password
    }

    return new Promise<Boolean>((resolve, reject) => {
      axios.post(endpoint, data)
        .then((res) => {
          this.authConf = this.addBearerToConf(res.data.token);
          localStorage.setItem("token", res.data.token);
          resolve(true);
        })
        .catch(err => reject(err))
    })
  }

  /**
   * Gets list of metadata
   */
  async getMetadaList(user: string): Promise<AxiosResponse> {
    const endpoint = this.url + "/metadata";

    return axios.get(endpoint, this.authConf);
  }
  
  /**
   * Downloads graph from server
   */
  async createGraph(curriculum: string, title: string): Promise<AxiosResponse> {
    const endpoint = this.url + "/graph/create";
    const data = {
      curriculum: curriculum,
      title: title
    }

    console.log(data);
    return axios.post(endpoint, data);
  }
}


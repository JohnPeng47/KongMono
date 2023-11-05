import { BaseHTTPRequest, ENDPOINT } from "./common";

export const METADATA_ENDPOINT = ENDPOINT + "/metadata";
export const AUTHTENICATE_ENDPOINT = ENDPOINT + "/authenticate";

export const GRAPH_ENDPOINT = (graph_id: string) => {
  return ENDPOINT + "/graph/" + graph_id;
};

export class GETMetadataRequest extends BaseHTTPRequest {
  public static getMetadata() {
    return BaseHTTPRequest.get(METADATA_ENDPOINT);
  }
}
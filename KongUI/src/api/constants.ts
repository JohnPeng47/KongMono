const ENDPOINT = "http://localhost:8000";

export const METADATA_ENDPOINT = ENDPOINT + "/metadata";
export const AUTHTENICATE_ENDPOINT = ENDPOINT + "/authenticate";
export const GRAPH_ENDPOINT = (graph_id: string) => {
  return ENDPOINT + "/graph/" + graph_id;
};

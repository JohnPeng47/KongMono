import { BaseHTTPRequest, ENDPOINT } from "./common";

const TRACKING_ENDPOINT = ENDPOINT + "/events";

type ExpandDescriptionEvent = {
  eventType: "expand_description";
  data: {
    node_id: string;
  };
};

type ReadDescriptionEvent = {
  eventType: "read_description";
  data: {
    node_id: string;
  };
};

type SelectNodeEvent = {
  eventType: "select_node";
  data: {
    selected_node_id: string;
    sibling_nodes: {
      previously_selected: string[];
      not_seelcted: string[];
    };
  };
};

type TrackingData = {
  event: ExpandDescriptionEvent | SelectNodeEvent | ReadDescriptionEvent;
};

export class POSTTrackingDataRequest extends BaseHTTPRequest {
  public static postTrackingData(data: TrackingData) {
    return BaseHTTPRequest.post(TRACKING_ENDPOINT, data);
  }
}

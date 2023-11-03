import React, { useCallback } from "react";
import { useState, useMemo } from "react";
import { useContext } from "use-context-selector";
import { Handle, Position, useReactFlow } from "reactflow";
import { ConceptMapContext } from "../../provider/ConceptMapProvider";
import { RFNodeData } from "../../../common/common-types";
import ToggleOnceCheckbox from "./ToggleOnceCheckbox";
import { POSTTrackingDataRequest } from "../../../api/tracking";

import Box from "@mui/material/Box";

type AttachedNodeProps = {
  data: RFNodeData;
  isConnectable: boolean;
};

function AttachedNode({ data, isConnectable }: AttachedNodeProps) {
  const { getEdges, getNodes } = useReactFlow();
  const [isChecked, setIsChecked] = useState(false); // state to keep track of checkbox

  const { id: nodeID } = data;
  const nodes = getNodes();
  // const color = data.color ? data.color

  const [dropdown, setDropdown] = useState(false);

  // think the reason we put this in global context was because calling setNodes
  // right here within a ReactNode component triggered an infinite loop since
  // this component gets re-rendered whenever setNodes is called
  const { showHideUnattachedChildren } = useContext(ConceptMapContext);

  const outEdges = useMemo(() => {
    return getEdges().filter((edge) => edge.source === nodeID);
  }, [getEdges, nodeID]);

  // this call should be resolved by the global KnowledgeGraph provider
  const children = nodes.filter((node) => {
    return outEdges.some((edge) => edge.target === node.id);
  });

  const readDescriptionCallback = useCallback(
    (check: boolean) => {
      setIsChecked(check);

      const req = POSTTrackingDataRequest.postTrackingData({
        event: {
          eventType: "read_description",
          data: {
            node_id: nodeID,
          },
        },
      });
      req();
    },
    [isChecked]
  );

  return (
    <Box
      sx={{
        display: "flex",
        bgcolor: "background.paper",
        boxShadow: 4,
        borderRadius: 2,
        p: 2,
        border: 3,
        borderColor: data.color,
        maxWidth: 300,
        // TODO: add a transition here
        // transition: 'maxHeight 0.8s ease-in-out', // Transitioning maxHeight
        // overflow: 'hidden',  // To hide content during transition
        // maxHeight: dropdown ? '1000px' : '200px' // Assuming 200px is the height without dropdown. Adjust as needed.
      }}
    >
      <Handle type="target" position={Position.Top} isConnectable={true} />
      <Handle type="source" position={Position.Bottom} isConnectable={true} />
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          width: "100%",
        }}
      >
        <div>
          <div><strong>{data.title}</strong></div>
          <button onClick={() => {
            console.log(data.id);
            setDropdown(!dropdown);
          }}>Description</button>
          <button onClick={() => showHideUnattachedChildren(children)}>
            {" "}
            Open connections
          </button>
          {dropdown && (
            <Box>
              <p>{data.description}</p>
            </Box>
          )}
        </div>
        {/* Child not expanding to 100% height of parent when parent is expanded, help me */}
        {/* <Box sx={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            height: "100%",
            justifyContent: "space-between"
          }}> */}
        {dropdown && (
          <Box
            sx={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              height: "100%",
              justifyContent: "space-between",
            }}
          >
            <ToggleOnceCheckbox
              isChecked={isChecked}
              onChange={readDescriptionCallback}
            ></ToggleOnceCheckbox>
            {isChecked && (
              <Box
                sx={{
                  color: "green",
                }}
              >
                <p>Read!</p>
              </Box>
            )}
          </Box>
        )}
      </Box>
    </Box>
  );
}

export default AttachedNode;

import { useRef, useState } from 'react';
import { Handle, Position } from 'reactflow';
import { RFNodeData } from "../../../common/common-types";
import { 
  Box, 
  TextField, 
  Button,
  CircularProgress
} from '@mui/material';
import { TreeEditMapContext } from '../../provider/TreeEditMapProvider';
import { useContext } from 'use-context-selector';

import '../../../index.css'
import { AlertBoxContext } from '../../../common/provider/AlertBoxProvider';

const handleStyle = { left: 10 };

type TreeNodeProps = {
    data: RFNodeData;
    isConnectable: boolean;
    selected: boolean;
    xPos: number,
    yPos: number 
  };

function SaveGraphButton({ onClick }) {
  return (
    <Button 
      sx={{ width: 300, marginLeft: 1 }}
      variant="contained" 
      color="error" 
      onClick={onClick}
    >
      SAVE GRAPH
    </Button>
  );
}

function GraphTitlePopup({ title, setTitle, onSave, onCancel }) {
  return (
    <div style ={{width: 300}} >
      <input 
        type="text" 
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter graph title"
      />
      <button onClick={onSave}>
        Confirm
      </button>
      <button onClick={onCancel}>
        Cancel
      </button>
    </div>
  );
}

function TreeNode({ data, isConnectable, xPos, yPos }: TreeNodeProps) {
  const [showPopup, setShowPopup] = useState(false);
  const [title, setTitle] = useState(data.title);  

  const [loading, setLoading] = useState<boolean>(false);
  const titleRef = useRef<string>(data.title);

  const { 
    modifyNodeTitle, 
    genSubGraph, 
    deleteNode, 
    saveGraph,
    genGraphDesc,
    collapseNodes,
    addNode
  } = useContext( TreeEditMapContext );

  const {
    sendToast
  } = useContext( AlertBoxContext );

  const { id: currID } = data;

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    titleRef.current = event.target.value;
    modifyNodeTitle(currID, titleRef.current);
  };

  const openPopup = () => {
    setShowPopup(x => !x);
    console.log(showPopup);
  }

  function GenGraphDescBtn({graphId}) { 
    return (
      <Button 
        sx={{ width: 300, marginLeft: 1 }}
        variant="contained" 
        color="success" 
        onClick={() => {
          sendToast("Started generating graph descriptions, please wait..", "info");
          genGraphDesc(graphId).then(res => {
            if (res)
              sendToast("Finished updating graph!", "success")
          }).catch(err => {
            sendToast("Something went wrong..", "error");
          })
        }}
      >
        Generate Graph
      </Button>
    );
  }
  
  return (
    <div style={{ display: 'flex', alignItems: 'center' }}>
        <Handle type="target" position={Position.Left} isConnectable={isConnectable} />


      <Box sx={{
        display: 'flex', // Horizontal layout
        flexDirection: 'row',
        width: '100%', // Take full width of the parent container
      }}>
        <Box sx={{
          display: 'flex',             // Turn this box into a flex container
          alignItems: 'center',        // Align items vertically in the center
          width: 1500,
          maxWidth: '100%',
          border: "black"
        }}>
          <TextField
            id="text"
            name="text"
            label="Text"
            variant="outlined"
            onChange={handleInputChange}
            fullWidth                  // This will ensure it takes up the available space
            defaultValue={data.title}
            sx={{ width: 500 }}       // Allow the text field to grow as needed
          />
          <Button sx={{
            width: 100,            // Set a specific width for the button
            marginLeft: 1            // Optional: add a little spacing between the TextField and Button
          }} variant="contained" color="primary" onClick={() =>  {
              setLoading(true);
              genSubGraph(currID).then((_) => {
                sendToast("Finished generating!", "success");
              }).catch((err) => {
                sendToast(`Server error: ${err}`, "success");
                // Success
              }).finally(() => {
                setLoading(false);
              })
            }
          }>
            Re-generate
          </Button>

          <Button sx={{
            width: 50,            // Set a specific width for the button
            marginLeft: 1            // Optional: add a little spacing between the TextField and Button
          }} variant="contained" color="primary" onClick={() =>  {
              console.log("Deleting node: ", data.title);
              deleteNode(currID);
            }
          }>
            DELETE
          </Button>

          <Button sx={{
            width: 40,            // Set a specific width for the button
            marginLeft: 1            // Optional: add a little spacing between the TextField and Button
          }} variant="contained" color="primary" onClick={() =>  {
              console.log("collapsing node: ", data.title);
              collapseNodes(currID);
            }
          }>
            Collapse
          </Button>
          <Button sx={{
            width: 50,            // Set a specific width for the button
            marginLeft: 1            // Optional: add a little spacing between the TextField and Button
          }} variant="contained" color="primary" onClick={() =>  {
              console.log("Adding node: ", data.title);
              addNode(data.id);
            }
          }>
            Add
          </Button>

          {
            data.node_type === "ROOT" && (
              <>
                <SaveGraphButton onClick={() => openPopup()} />
                {showPopup && (
                  <GraphTitlePopup 
                    title={title}
                    setTitle={setTitle}
                    onSave={() => {
                      saveGraph(title);
                      setShowPopup(false);
                    }}
                    onCancel={() => setShowPopup(false)}
                  />
                )}
                <GenGraphDescBtn graphId={data.id} />
              </>
            )
          }
          <Box sx={{
            paddingLeft: 5,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '50', // This Box will take 20% of the parent Box's width
          }}>
            {
              loading &&
              <CircularProgress /> // This will be rendered when loading is true
            }
          </Box>

        </Box>
      </Box>
      {/* Cant actually remove this because RF expects it*/}
      {/* <div style={{display: "none"}}> */}
        <Handle
          type="source"
          position={Position.Bottom}
          id="a"
          style={handleStyle}
          isConnectable={isConnectable}
        />
      {/* </div> */}
    </div>

    );
  }

export default TreeNode;
  
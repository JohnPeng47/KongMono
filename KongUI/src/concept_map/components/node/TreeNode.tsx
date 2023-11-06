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
import { useNavigate } from 'react-router-dom';
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

function TreeNode({ data, isConnectable, xPos, yPos }: TreeNodeProps) {
  const [showPopup, setShowPopup] = useState(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [navToMap, setNavToMap] = useState(false);
  const titleRef = useRef<string>(data.title);

  const { 
    modifyNodeTitle, 
    genSubGraph, 
    deleteNode, 
    genGraphDesc,
    collapseNodes,
    addNode,
    nodesWithoutDescr
  } = useContext( TreeEditMapContext );

  const navigate = useNavigate();
  const {
    sendToast
  } = useContext( AlertBoxContext );

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    titleRef.current = event.target.value;
    modifyNodeTitle(data.id, titleRef.current);
  };

  function GenDescrBtn() { 
    return (
      <Button 
        sx={{ width: 300, marginLeft: 1 }}
        variant="contained" 
        color="success" 
        onClick={() => {
          sendToast("Started generating graph descriptions, please wait..", "info");
          genGraphDesc(data.id).then(res => {
            sendToast("Finished updating graph!", "success");
            setNavToMap(true);
          }).catch(err => {
            sendToast("Something went wrong..", "error");
          })
        }}
      >
        Generate Graph
      </Button>
    );
  }

  function NavToMapBtn() { 
    return (
      <Button 
        sx={{ width: 300, marginLeft: 1 }}
        variant="contained" 
        color="secondary" 
        onClick={() => navigate(`/map/${data.id}`)}
      >
        See Updated Map
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
              genSubGraph(data.id).then((_) => {
                sendToast("Finished generating!", "success");
                setNavToMap(false);
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
              deleteNode(data.id);
            }
          }>
            DELETE
          </Button>

          <Button sx={{
            width: 40,            // Set a specific width for the button
            marginLeft: 1            // Optional: add a little spacing between the TextField and Button
          }} variant="contained" color="primary" onClick={() =>  {
              collapseNodes(data.id);
            }
          }>
            Collapse
          </Button>
          <Button sx={{
            width: 50,            // Set a specific width for the button
            marginLeft: 1            // Optional: add a little spacing between the TextField and Button
          }} variant="contained" color="primary" onClick={() =>  {
              addNode(data.id);
              // setNavToMap(false);
            }
          }>
            Add
          </Button>

          {
            data.node_type === "ROOT" && (
                !navToMap ? <GenDescrBtn /> : <NavToMapBtn />
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
  
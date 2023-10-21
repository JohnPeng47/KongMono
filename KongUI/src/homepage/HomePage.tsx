import React, { useEffect, useState } from "react";

// import axios from "axios";
import { GETMetadataRequest } from "../api/api";
import {
  Grid,
  Card,
  CardContent,
  Typography,
  CardActions,
  IconButton,
  Collapse,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { useContext } from "use-context-selector";
import { BackendContext } from "../concept_map/provider/backendProvider";

function HomePage() {
  const navigate = useNavigate();
  // modify this to use an array of booleans
  // right now all cards are toggled on/off at once
  const [expanded, setExpanded] = useState(false);
  const [metadataList, setMetadataList] = useState([]);
  const { backend } = useContext(BackendContext);

  async function fetchData() {
    try {
      const req = GETMetadataRequest.getMetadata();
      const res = await req();
      setMetadataList(res.data);
    } catch (error) {
      console.error("Error fetching metadata:", error);
    }
  }
  
  // console.log(getLayout());

  useEffect(() => {
    fetchData();
  }, []);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const navToGraph = (graphId: string) => {
    navigate("/map/" + graphId);
  };

  const navToTree = (graphId: string) => {
    navigate("/tree/" + graphId);
  };
  
  return (
    <>
    {/* <MyCytoscapeComponent></MyCytoscapeComponent> */}
    <Grid container spacing={3}>
      {metadataList.map((item, index) => (
        <Grid item xs={4} key={index}>
          <Card>
            <CardContent onClick={() => navToGraph(item.id)}>
              <Typography variant="h5" component="div">
                {item.metadata.title}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Curriculum: {item.metadata.curriculum}
              </Typography>
            </CardContent>
            <CardActions disableSpacing>
              <IconButton
                onClick={handleExpandClick}
                aria-expanded={expanded}
                aria-label="show more"
              >
                <ExpandMoreIcon />
              </IconButton>
            </CardActions>

            <button onClick={() => navToTree(item.id)}>Tree View</button>
            <button onClick={() => {
              backend.deleteGraph(item.id);
              fetchData();
            }}>Delete</button>

          </Card>
        </Grid>
      ))}
    </Grid>
    </>

  );
}

export default HomePage;

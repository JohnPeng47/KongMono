import React, { useState, useEffect } from "react";
import "./App.css";
import { Routes, Route } from "react-router-dom";
import { CircularProgress } from "@mui/material";

import { BaseHTTPRequest } from "./api/common";
import HomePage from "./homepage/HomePage";
import ConceptMapPage from "./concept_map/ConceptMapPage";
import LoginPage from "./authentication/Login";
import TreeEditMapPage from "./concept_map/TreeEditMapPage";

import { ReactFlowProvider } from "reactflow";
import { GlobalProvider } from "./concept_map/provider/globalProvider";
import { BackendProvider } from "./concept_map/provider/backendProvider";

import { ENDPOINT } from "./api/common";

function App() {
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    async function initializeApp() {
      // TODO: fold this into the backend provider class
      await BaseHTTPRequest.initializeToken();

      setIsInitialized(true);
    }

    initializeApp();
  }, []);

  // If not initialized, render the loading icon
  if (!isInitialized) {
    return <CircularProgress />;
  }

  return (
    <BackendProvider url={ENDPOINT}>
      <ReactFlowProvider>
        <GlobalProvider reactFlowWrapper={"hello"}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/map/:mapId" element={<ConceptMapPage />} />
            <Route path="/tree/:mapId" element={<TreeEditMapPage />} />
            <Route path="/login" element={<LoginPage />} />
          </Routes>
        </GlobalProvider>
      </ReactFlowProvider>
    </BackendProvider>
  );
}

export default App;

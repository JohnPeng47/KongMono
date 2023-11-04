import "./App.css";
import { Routes, Route } from "react-router-dom";
import HomePage from "./homepage/HomePage";
import ConceptMapPage from "./pages/ConceptMapPage";
import LoginPage from "./authentication/Login";
import TreeEditMapPage from "./pages/TreeEditMapPage";
import RegisterationPage from "./authentication/Register";

import { ReactFlowProvider } from "reactflow";
import { BackendProvider } from "./concept_map/provider/backendProvider";
import { AlertBoxProvider } from "./common/provider/AlertBoxProvider";

import { ENDPOINT } from "./api/common";
import { AlertBoxProvider } from "./common/provider/AlertBoxProvider";

function App() {  
  return (
    <BackendProvider url={ENDPOINT}>
      <ReactFlowProvider>
        <AlertBoxProvider>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/map/:mapId" element={<ConceptMapPage />} />
            <Route path="/tree/:mapId" element={<TreeEditMapPage />} />
            <Route path="/login" element={<LoginPage />} />
<<<<<<< HEAD
=======
            <Route path="/register" element={<RegisterationPage />} />
>>>>>>> f702ce2 (Integrated login with backend)
          </Routes>
        </AlertBoxProvider>
      </ReactFlowProvider>
    </BackendProvider>
  );
}

export default App;

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';

import ReactFlowProvider from 'reactflow';

import HomePage from './homepage/HomePage';
import App from './App';
import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <div style={{ backgroundColor: '#404040', height: '100vh'}}>
    {/* <React.StrictMode> */}
      <BrowserRouter>
        <App></App>
      </BrowserRouter>
        {/* <LayoutFlow/> */}
      {/* <HomePage></HomePage> */}
  </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

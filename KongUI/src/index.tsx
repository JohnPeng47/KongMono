import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';

import App from './App';
import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <div style={{ backgroundColor: '#d4e6b5', height: '100vh'}}>
    <BrowserRouter>
      <App></App>
    </BrowserRouter>
  </div>
);
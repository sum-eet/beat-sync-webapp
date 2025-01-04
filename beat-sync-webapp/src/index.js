import React from "react";
import ReactDOM from "react-dom/client"; // Import createRoot from 'react-dom/client'
import "./index.css"; // Optional global styles
import HomePage from "./pages/HomePage"; // Import your HomePage component

// Create a root and render the app
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <HomePage />
  </React.StrictMode>
);

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { FiltersProvider } from "../context/filters.jsx";
import { AuthProvider } from "../context/auth.jsx";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <AuthProvider>
    <FiltersProvider>
      <App />
    </FiltersProvider>
  </AuthProvider>
);

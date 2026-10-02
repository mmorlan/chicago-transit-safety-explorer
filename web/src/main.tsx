import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import esriConfig from "@arcgis/core/config.js";
import "@esri/calcite-components/main.css";
import "@arcgis/core/assets/esri/themes/light/main.css";
import "./index.css";
import App from "./App";

const apiKey = import.meta.env.VITE_ARCGIS_API_KEY;
if (apiKey) {
  esriConfig.apiKey = apiKey;
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

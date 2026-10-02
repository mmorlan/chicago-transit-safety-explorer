import "@arcgis/map-components/components/arcgis-map";
import "@arcgis/map-components/components/arcgis-zoom";
import "@arcgis/map-components/components/arcgis-home";
import "@arcgis/map-components/components/arcgis-legend";

import type { ArcgisMap } from "@arcgis/map-components/components/arcgis-map";
import { createStationsLayer } from "../layers/stationsLayer";

// Esri basemap styles need an API key. Without one, fall back to OpenStreetMap so the app still runs locally.
const BASEMAP = import.meta.env.VITE_ARCGIS_API_KEY ? "arcgis/light-gray" : "osm";
const STATIONS_URL = `${import.meta.env.BASE_URL}data/stations.geojson`;

export function StationMap() {
  const handleViewReady = (event: CustomEvent<void> & { target: ArcgisMap }) => {
    const map = event.target.map;
    if (map && map.layers.length === 0) {
      map.add(createStationsLayer(STATIONS_URL));
    }
  };

  return (
    <arcgis-map basemap={BASEMAP} center="-87.68, 41.86" zoom={11} onarcgisViewReadyChange={handleViewReady}>
      <arcgis-zoom slot="top-left" />
      <arcgis-home slot="top-left" />
      <arcgis-legend slot="bottom-left" />
    </arcgis-map>
  );
}

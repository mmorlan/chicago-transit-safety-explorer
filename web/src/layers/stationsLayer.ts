import GeoJSONLayer from "@arcgis/core/layers/GeoJSONLayer.js";
import SimpleRenderer from "@arcgis/core/renderers/SimpleRenderer.js";
import SimpleMarkerSymbol from "@arcgis/core/symbols/SimpleMarkerSymbol.js";

/** Stage 1 layer: CTA 'L' stations straight from the pipeline's GeoJSON output. */
export function createStationsLayer(url: string): GeoJSONLayer {
  return new GeoJSONLayer({
    url,
    title: "CTA 'L' stations",
    outFields: ["*"],
    renderer: new SimpleRenderer({
      label: "Station",
      symbol: new SimpleMarkerSymbol({
        style: "circle",
        size: 8,
        color: [32, 72, 120, 0.9],
        outline: { color: [255, 255, 255, 1], width: 1.25 },
      }),
    }),
    popupTemplate: {
      title: "{station_name}",
      content: [
        {
          type: "fields",
          fieldInfos: [
            { fieldName: "lines", label: "Lines" },
            { fieldName: "ada", label: "ADA accessible" },
            { fieldName: "station_id", label: "Station ID (map_id)" },
          ],
        },
      ],
    },
  });
}

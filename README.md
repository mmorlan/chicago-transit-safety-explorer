# Chicago Transit Safety Explorer

Finds CTA stops with a disproportionate concentration of nearby traffic crashes, in the spirit of a Vision Zero high injury network analysis. A Python pipeline does the geoprocessing; a React + ArcGIS Maps SDK for JavaScript front end displays the precomputed results.

**Status: stage 1 (thin slice).** CTA 'L' stations go from the Chicago Data Portal API through a Pandas pipeline into GeoJSON, displayed as one map layer.

## Layout

| Path | What it is |
|---|---|
| `pipeline/` | Python ETL (uv, Pandas). Writes `web/public/data/stations.geojson`. |
| `web/` | Vite + React 19 + TypeScript + `@arcgis/map-components` 5.1. |

## Run it

Requires [uv](https://docs.astral.sh/uv/) and Node 22+.

```sh
# 1. Pipeline: extract, clean, write GeoJSON
cd pipeline
uv run pytest
uv run python -m pipeline

# 2. Front end
cd ../web
npm install
cp .env.example .env.local   # optional: add an ArcGIS API key for Esri basemaps
npm run dev
```

Without an API key the map uses the OpenStreetMap basemap. With one it uses the Esri light gray canvas.

## Data

- [CTA - System Information - List of 'L' Stops](https://data.cityofchicago.org/Transportation/CTA-System-Information-List-of-L-Stops/8pix-ypme) (`8pix-ypme`). The source has one row per platform direction (302 rows). The pipeline collapses these to one row per station by `map_id` (144 stations). A station serves a line if any platform does, and is ADA accessible only if every platform is.

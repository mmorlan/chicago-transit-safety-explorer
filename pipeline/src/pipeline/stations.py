"""Extract, clean, and export CTA 'L' stations from the Chicago Data Portal."""

import json
from pathlib import Path

import pandas as pd
import requests

# CTA - System Information - List of 'L' Stops (one row per platform direction)
STOPS_URL = "https://data.cityofchicago.org/resource/8pix-ypme.json"

# Dataset column -> readable line name
LINE_COLUMNS = {
    "red": "Red",
    "blue": "Blue",
    "g": "Green",
    "brn": "Brown",
    "p": "Purple",
    "y": "Yellow",
    "pnk": "Pink",
    "o": "Orange",
}


def extract(url: str = STOPS_URL, timeout: int = 30) -> list[dict]:
    """Request every stop record from the Socrata API."""
    response = requests.get(url, params={"$limit": 50000}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def transform(records: list[dict]) -> pd.DataFrame:
    """Collapse platform-level stops to one row per station.

    The source lists each platform direction separately, so a station like
    Clark/Lake appears several times. Stations are keyed by map_id. A station
    serves a line if any of its platforms does, and is ADA accessible only if
    every platform is.
    """
    df = pd.DataFrame.from_records(records)
    df["latitude"] = pd.to_numeric(df["location"].str["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["location"].str["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])

    flag_columns = ["ada", *LINE_COLUMNS]
    for column in flag_columns:
        df[column] = df[column].astype(str).str.lower().eq("true")

    stations = df.groupby("map_id", as_index=False).agg(
        station_name=("station_name", "first"),
        descriptive_name=("station_descriptive_name", "first"),
        latitude=("latitude", "mean"),
        longitude=("longitude", "mean"),
        ada=("ada", "all"),
        **{column: (column, "any") for column in LINE_COLUMNS},
    )
    stations["lines"] = stations[list(LINE_COLUMNS)].apply(
        lambda row: ", ".join(name for column, name in LINE_COLUMNS.items() if row[column]),
        axis=1,
    )
    stations["line_count"] = stations[list(LINE_COLUMNS)].sum(axis=1).astype(int)
    stations = stations.rename(columns={"map_id": "station_id"})
    return stations[
        ["station_id", "station_name", "descriptive_name", "lines", "line_count", "ada", "latitude", "longitude"]
    ].sort_values("station_name", ignore_index=True)


def to_geojson(stations: pd.DataFrame) -> dict:
    """Build a GeoJSON FeatureCollection of points in WGS84 (EPSG:4326)."""
    features = []
    for row in stations.itertuples(index=False):
        properties = row._asdict()
        longitude = properties.pop("longitude")
        latitude = properties.pop("latitude")
        # GeoJSONLayer has no boolean field type and drops boolean properties, so write text
        properties["ada"] = "Yes" if properties["ada"] else "No"
        properties["line_count"] = int(properties["line_count"])
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(longitude, 6), round(latitude, 6)]},
                "properties": properties,
            }
        )
    return {"type": "FeatureCollection", "features": features}


def load(geojson: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(geojson, indent=1))

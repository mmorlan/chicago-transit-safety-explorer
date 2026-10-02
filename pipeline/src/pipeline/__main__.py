"""Run the pipeline: python -m pipeline [output_path]"""

import sys
from pathlib import Path

from pipeline import stations

DEFAULT_OUTPUT = Path(__file__).resolve().parents[3] / "web" / "public" / "data" / "stations.geojson"


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    records = stations.extract()
    cleaned = stations.transform(records)
    stations.load(stations.to_geojson(cleaned), output)
    print(f"{len(records)} stop records -> {len(cleaned)} stations -> {output}")


if __name__ == "__main__":
    main()

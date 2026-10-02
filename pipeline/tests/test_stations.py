from pipeline.stations import to_geojson, transform


def stop(map_id, name, lat, lon, ada=True, **lines):
    record = {
        "map_id": map_id,
        "station_name": name,
        "station_descriptive_name": f"{name} (test)",
        "ada": ada,
        "location": {"latitude": str(lat), "longitude": str(lon)},
    }
    for column in ["red", "blue", "g", "brn", "p", "y", "pnk", "o"]:
        record[column] = lines.get(column, False)
    return record


def test_platforms_collapse_to_one_station():
    records = [
        stop("40380", "Clark/Lake", 41.8857, -87.6309, blue=True),
        stop("40380", "Clark/Lake", 41.8859, -87.6311, ada=False, brn=True, g=True),
        stop("40830", "18th", 41.8579, -87.6691, pnk=True),
    ]
    stations = transform(records)

    assert len(stations) == 2
    clark = stations.set_index("station_id").loc["40380"]
    assert clark["lines"] == "Blue, Green, Brown"
    assert clark["line_count"] == 3
    assert clark["ada"] == False  # noqa: E712 - one inaccessible platform makes the station inaccessible
    assert abs(clark["latitude"] - 41.8858) < 1e-9


def test_string_flags_and_missing_location_are_handled():
    records = [
        stop("1", "A", 41.9, -87.6, ada="true", red="true"),
        {**stop("2", "B", 0, 0), "location": {}},
    ]
    stations = transform(records)

    assert list(stations["station_id"]) == ["1"]
    assert stations.loc[0, "ada"] == True  # noqa: E712
    assert stations.loc[0, "lines"] == "Red"


def test_geojson_uses_lon_lat_order():
    geojson = to_geojson(transform([stop("1", "A", 41.9, -87.6, red=True)]))
    feature = geojson["features"][0]

    assert geojson["type"] == "FeatureCollection"
    assert feature["geometry"]["coordinates"] == [-87.6, 41.9]
    assert "latitude" not in feature["properties"]
    assert feature["properties"]["ada"] == "Yes"

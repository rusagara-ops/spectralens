"""Vector GIS exports — GeoJSON FeatureCollections for QGIS."""

import json

import numpy as np

from analysis import compute_zone_statistics
from geospatial import pixel_to_wgs84

# Zone definitions mirror those in analysis.compute_zone_statistics so QGIS
# attribute tables line up 1:1 with the AI report.
ZONE_DEFS = [
    {"id": "A", "name": "Zone A (NW)", "rows": (0, 40), "cols": (0, 40)},
    {"id": "B", "name": "Zone B (NE)", "rows": (0, 40), "cols": (60, 100)},
    {"id": "C", "name": "Zone C (SW)", "rows": (60, 100), "cols": (0, 40)},
    {"id": "D", "name": "Zone D (SE)", "rows": (60, 100), "cols": (60, 100)},
]


def _ring_for_zone(rows, cols):
    """Return a closed GeoJSON polygon ring (lon, lat) for a zone bounding box."""
    r0, r1 = rows
    c0, c1 = cols

    # Walk the four corners. pixel_to_wgs84 returns (lat, lon); GeoJSON wants (lon, lat).
    corners_pix = [(c0, r0), (c1, r0), (c1, r1), (c0, r1), (c0, r0)]
    return [list(reversed(pixel_to_wgs84(c, r))) for c, r in corners_pix]


def zones_to_geojson(cube: np.ndarray, ndvi: np.ndarray) -> dict:
    """Build a GeoJSON FeatureCollection of the four health zones with stats attached."""
    stats = compute_zone_statistics(cube, ndvi)["zones"]

    features = []
    for zd in ZONE_DEFS:
        zone_key = zd["name"].replace("(NW)", "(NW quadrant)") \
                              .replace("(NE)", "(NE quadrant)") \
                              .replace("(SW)", "(SW quadrant)") \
                              .replace("(SE)", "(SE quadrant)")
        zone_stats = stats.get(zone_key, {})

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [_ring_for_zone(zd["rows"], zd["cols"])],
            },
            "properties": {
                "zone_id": zd["id"],
                "zone_name": zd["name"],
                "classification": zone_stats.get("health_classification", "Unknown"),
                "mean_ndvi": zone_stats.get("mean_ndvi"),
                "min_ndvi": zone_stats.get("min_ndvi"),
                "max_ndvi": zone_stats.get("max_ndvi"),
                "std_ndvi": zone_stats.get("std_ndvi"),
                "pixel_count": zone_stats.get("pixel_count"),
            },
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "name": "spectralens_zones",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"},
        },
        "features": features,
    }


def zones_to_geojson_bytes(cube: np.ndarray, ndvi: np.ndarray) -> bytes:
    return json.dumps(zones_to_geojson(cube, ndvi), indent=2).encode("utf-8")

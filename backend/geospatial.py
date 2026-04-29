"""Geospatial reference for SpectraLens demo data.

Anchors the synthetic 100x100 hyperspectral cube to a real-world location
so outputs (GeoTIFF, GeoJSON, KML) can be loaded directly into QGIS, ArcGIS,
or any GIS tool with proper georeferencing.

Demo plot: a 50m x 50m research field near Ames, Iowa (USDA corn belt).
Projection: UTM Zone 15N (EPSG:32615) — meter-based, suitable for agriculture.
"""

import math

# Pixel grid
PIXEL_SIZE_M = 0.5  # meters per pixel — 0.5 m matches typical drone hyperspectral GSD
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Coordinate reference systems
CRS_UTM = "EPSG:32615"  # UTM Zone 15N — Iowa, USA
CRS_WGS84 = "EPSG:4326"  # lat/lon

# Plot anchor (top-left corner) in UTM Zone 15N
# Approximate location: research plot near Ames, IA
ORIGIN_UTM_E = 447500.0  # easting (m)
ORIGIN_UTM_N = 4654000.0  # northing (m)

# Approximate WGS84 anchor for the same point (used for Leaflet / web maps)
ORIGIN_LAT = 42.0308
ORIGIN_LON = -93.6319


def get_geotransform():
    """GDAL-style affine geotransform: (origin_x, px_width, 0, origin_y, 0, -px_height).

    The negative pixel height encodes the standard north-up image convention
    (row 0 at top, increasing y means moving south).
    """
    return (
        ORIGIN_UTM_E,
        PIXEL_SIZE_M,
        0.0,
        ORIGIN_UTM_N,
        0.0,
        -PIXEL_SIZE_M,
    )


def get_bounds_utm():
    """Bounding box in UTM as (min_x, min_y, max_x, max_y)."""
    width_m = GRID_WIDTH * PIXEL_SIZE_M
    height_m = GRID_HEIGHT * PIXEL_SIZE_M
    return (
        ORIGIN_UTM_E,
        ORIGIN_UTM_N - height_m,
        ORIGIN_UTM_E + width_m,
        ORIGIN_UTM_N,
    )


def get_bounds_wgs84():
    """Approximate WGS84 bounds (south, west, north, east) — Leaflet ordering."""
    width_m = GRID_WIDTH * PIXEL_SIZE_M
    height_m = GRID_HEIGHT * PIXEL_SIZE_M

    # Local flat-earth approximation (good enough for a 50m plot)
    meters_per_deg_lat = 111_320.0
    meters_per_deg_lon = 111_320.0 * math.cos(math.radians(ORIGIN_LAT))

    south = ORIGIN_LAT - height_m / meters_per_deg_lat
    north = ORIGIN_LAT
    west = ORIGIN_LON
    east = ORIGIN_LON + width_m / meters_per_deg_lon

    return (south, west, north, east)


def pixel_to_utm(col: int, row: int):
    """Pixel (col, row) -> UTM (easting, northing) at pixel center."""
    x = ORIGIN_UTM_E + (col + 0.5) * PIXEL_SIZE_M
    y = ORIGIN_UTM_N - (row + 0.5) * PIXEL_SIZE_M
    return (x, y)


def pixel_to_wgs84(col: int, row: int):
    """Pixel (col, row) -> WGS84 (lat, lon) at pixel center, flat-earth approx."""
    width_m = (col + 0.5) * PIXEL_SIZE_M
    height_m = (row + 0.5) * PIXEL_SIZE_M

    meters_per_deg_lat = 111_320.0
    meters_per_deg_lon = 111_320.0 * math.cos(math.radians(ORIGIN_LAT))

    lat = ORIGIN_LAT - height_m / meters_per_deg_lat
    lon = ORIGIN_LON + width_m / meters_per_deg_lon
    return (lat, lon)


def get_metadata():
    """Bundle every geospatial fact about the demo plot — surfaced via /api."""
    s, w, n, e = get_bounds_wgs84()
    min_x, min_y, max_x, max_y = get_bounds_utm()
    return {
        "crs_projected": CRS_UTM,
        "crs_geographic": CRS_WGS84,
        "pixel_size_m": PIXEL_SIZE_M,
        "grid_width": GRID_WIDTH,
        "grid_height": GRID_HEIGHT,
        "origin_utm": {"easting": ORIGIN_UTM_E, "northing": ORIGIN_UTM_N},
        "origin_wgs84": {"lat": ORIGIN_LAT, "lon": ORIGIN_LON},
        "bounds_utm": {"min_x": min_x, "min_y": min_y, "max_x": max_x, "max_y": max_y},
        "bounds_wgs84": {"south": s, "west": w, "north": n, "east": e},
        "geotransform": list(get_geotransform()),
        "location_name": "Ames, IA research plot (synthetic)",
    }

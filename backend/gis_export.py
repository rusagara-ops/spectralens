"""GIS export helpers — write GeoTIFFs, world files, and projection sidecars.

The GeoTIFFs are written with proper GeoKeyDirectory tags so QGIS and ArcGIS
recognize the projection without a sidecar. We additionally emit a .tfw world
file and a .prj WKT file, which is the canonical ESRI fallback and ensures
compatibility with tools that don't read embedded GeoTIFF tags.
"""

import io
import zipfile

import numpy as np
from PIL import Image
from PIL.TiffImagePlugin import ImageFileDirectory_v2

from geospatial import (
    CRS_UTM,
    ORIGIN_UTM_E,
    ORIGIN_UTM_N,
    PIXEL_SIZE_M,
)

# Well-known text for UTM Zone 15N (NAD83 datum used by USDA / Iowa surveys).
# Hardcoded so the export is dependency-free — no pyproj required.
UTM15N_WKT = (
    'PROJCS["NAD83 / UTM zone 15N",'
    'GEOGCS["NAD83",'
    'DATUM["North_American_Datum_1983",'
    'SPHEROID["GRS 1980",6378137,298.257222101]],'
    'PRIMEM["Greenwich",0],'
    'UNIT["degree",0.0174532925199433]],'
    'PROJECTION["Transverse_Mercator"],'
    'PARAMETER["latitude_of_origin",0],'
    'PARAMETER["central_meridian",-93],'
    'PARAMETER["scale_factor",0.9996],'
    'PARAMETER["false_easting",500000],'
    'PARAMETER["false_northing",0],'
    'UNIT["metre",1],'
    'AUTHORITY["EPSG","32615"]]'
)


def _build_geo_ifd():
    """Build the GeoTIFF tag directory pinning the raster to UTM Zone 15N."""
    ifd = ImageFileDirectory_v2()

    # ModelPixelScaleTag — pixel size in projected units
    ifd.tagtype[33550] = 12  # DOUBLE
    ifd[33550] = (PIXEL_SIZE_M, PIXEL_SIZE_M, 0.0)

    # ModelTiepointTag — anchor pixel (0,0) to projected origin
    ifd.tagtype[33922] = 12  # DOUBLE
    ifd[33922] = (0.0, 0.0, 0.0, ORIGIN_UTM_E, ORIGIN_UTM_N, 0.0)

    # GeoKeyDirectoryTag — encodes the CRS as a key/value table
    # Layout: header (4 shorts) + N key entries (4 shorts each)
    # Keys we set:
    #   1024 GTModelTypeGeoKey      = 1 (projected)
    #   1025 GTRasterTypeGeoKey     = 1 (PixelIsArea)
    #   3072 ProjectedCSTypeGeoKey  = 32615 (UTM 15N WGS84)
    ifd.tagtype[34735] = 3  # SHORT
    ifd[34735] = (
        1, 1, 0, 3,             # version=1, key_rev=1, minor=0, num_keys=3
        1024, 0, 1, 1,          # GTModelTypeGeoKey -> projected
        1025, 0, 1, 1,          # GTRasterTypeGeoKey -> PixelIsArea
        3072, 0, 1, 32615,      # ProjectedCSTypeGeoKey -> EPSG:32615
    )

    return ifd


def _write_world_file(pixel_size_m: float, origin_x: float, origin_y: float) -> str:
    """Generate the contents of a .tfw world file (6 lines)."""
    return (
        f"{pixel_size_m}\n"
        f"0.0\n"
        f"0.0\n"
        f"-{pixel_size_m}\n"
        f"{origin_x}\n"
        f"{origin_y}\n"
    )


def _array_to_uint8(arr: np.ndarray, vmin: float, vmax: float) -> np.ndarray:
    """Stretch a float array to 0-255 uint8 for image storage."""
    span = vmax - vmin
    if span <= 0:
        return np.zeros_like(arr, dtype=np.uint8)
    scaled = np.clip((arr - vmin) / span, 0.0, 1.0)
    return (scaled * 255).astype(np.uint8)


def write_geotiff_float32(arr: np.ndarray) -> bytes:
    """Write a single-band float32 GeoTIFF — preserves real NDVI / reflectance values."""
    if arr.ndim != 2:
        raise ValueError("write_geotiff_float32 expects a 2D array")
    img = Image.fromarray(arr.astype(np.float32), mode="F")
    buf = io.BytesIO()
    img.save(buf, format="TIFF", tiffinfo=_build_geo_ifd(), compression="tiff_deflate")
    return buf.getvalue()


def write_geotiff_uint8(arr: np.ndarray) -> bytes:
    """Write a single-band uint8 GeoTIFF — for visualization layers."""
    if arr.ndim != 2:
        raise ValueError("write_geotiff_uint8 expects a 2D array")
    img = Image.fromarray(arr.astype(np.uint8), mode="L")
    buf = io.BytesIO()
    img.save(buf, format="TIFF", tiffinfo=_build_geo_ifd(), compression="tiff_deflate")
    return buf.getvalue()


def write_geotiff_rgb(arr: np.ndarray) -> bytes:
    """Write a 3-band RGB GeoTIFF — for false-color and styled NDVI maps."""
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise ValueError("write_geotiff_rgb expects a (H, W, 3) array")
    img = Image.fromarray(arr.astype(np.uint8), mode="RGB")
    buf = io.BytesIO()
    img.save(buf, format="TIFF", tiffinfo=_build_geo_ifd(), compression="tiff_deflate")
    return buf.getvalue()


def bundle_zip(tif_bytes: bytes, basename: str) -> bytes:
    """Bundle .tif + .tfw + .prj into a single ZIP for one-click QGIS load."""
    tfw = _write_world_file(PIXEL_SIZE_M, ORIGIN_UTM_E, ORIGIN_UTM_N)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{basename}.tif", tif_bytes)
        zf.writestr(f"{basename}.tfw", tfw)
        zf.writestr(f"{basename}.prj", UTM15N_WKT)
        zf.writestr(
            "README.txt",
            (
                f"SpectraLens GIS export — {basename}\n"
                f"CRS: {CRS_UTM} (UTM Zone 15N)\n"
                f"Pixel size: {PIXEL_SIZE_M} m\n"
                f"Origin (top-left): {ORIGIN_UTM_E} E, {ORIGIN_UTM_N} N\n"
                "\n"
                "Load in QGIS: Layer > Add Layer > Add Raster Layer > select the .tif.\n"
                "The .tfw and .prj sidecars are read automatically alongside.\n"
            ),
        )
    return buf.getvalue()

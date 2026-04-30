"""PyQGIS loader for SpectraLens outputs.

Run from inside QGIS:
  Python Console > Open Script > select this file > Run.

The script:
  1. Pulls NDVI, the full hyperspectral cube, and the four vegetation indices
     from a running SpectraLens backend (default http://localhost:8000).
  2. Pulls the zone vector layer as GeoJSON.
  3. Loads each layer into the active QGIS project with the matching .qml style.
  4. Frames the canvas to the field bounds and saves the project.

This is the "one-click" workflow for an agronomist or QGIS analyst — no
manual download, drag, or styling required.
"""

import json
import os
import tempfile
import urllib.request
import zipfile

# PyQGIS imports — only resolve when running inside QGIS
from qgis.core import (  # type: ignore
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsRectangle,
)
from qgis.utils import iface  # type: ignore


SPECTRALENS_API = os.environ.get("SPECTRALENS_API", "http://localhost:8000")
QML_DIR = os.path.dirname(os.path.abspath(__file__))


def _download(url: str, dest: str) -> str:
    """Fetch a URL to a local path; return that path."""
    print(f"  -> {url}")
    urllib.request.urlretrieve(url, dest)
    return dest


def _extract_tif(zip_path: str, work_dir: str) -> str:
    """Extract a SpectraLens .tif/.tfw/.prj bundle and return the .tif path."""
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(work_dir)
        for name in zf.namelist():
            if name.endswith(".tif"):
                return os.path.join(work_dir, name)
    raise RuntimeError(f"No .tif found in bundle: {zip_path}")


def _load_raster(path: str, name: str, qml: str | None = None):
    layer = QgsRasterLayer(path, name)
    if not layer.isValid():
        print(f"  !! failed to load {name}")
        return None
    if qml and os.path.exists(qml):
        layer.loadNamedStyle(qml)
        layer.triggerRepaint()
    QgsProject.instance().addMapLayer(layer)
    print(f"  + raster: {name}")
    return layer


def _load_vector(path: str, name: str, qml: str | None = None):
    layer = QgsVectorLayer(path, name, "ogr")
    if not layer.isValid():
        print(f"  !! failed to load {name}")
        return None
    if qml and os.path.exists(qml):
        layer.loadNamedStyle(qml)
        layer.triggerRepaint()
    QgsProject.instance().addMapLayer(layer)
    print(f"  + vector: {name}")
    return layer


def main():
    work_dir = tempfile.mkdtemp(prefix="spectralens_")
    print(f"SpectraLens loader — work dir: {work_dir}")
    print(f"API: {SPECTRALENS_API}")

    # 1) Field metadata — used to set the project CRS and canvas extent
    meta_path = _download(
        f"{SPECTRALENS_API}/api/demo/geospatial",
        os.path.join(work_dir, "geospatial.json"),
    )
    with open(meta_path) as f:
        meta = json.load(f)

    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem(meta["crs_projected"]))

    # 2) NDVI raster
    ndvi_zip = _download(
        f"{SPECTRALENS_API}/api/demo/ndvi.tif",
        os.path.join(work_dir, "ndvi.zip"),
    )
    ndvi_tif = _extract_tif(ndvi_zip, work_dir)
    _load_raster(ndvi_tif, "SpectraLens NDVI", os.path.join(QML_DIR, "spectralens_ndvi.qml"))

    # 3) Vegetation indices
    for index_name in ("ndre", "gndvi", "savi", "evi", "msavi"):
        zip_path = _download(
            f"{SPECTRALENS_API}/api/demo/index/{index_name}.tif",
            os.path.join(work_dir, f"{index_name}.zip"),
        )
        tif_path = _extract_tif(zip_path, work_dir)
        # Reuse the NDVI style for visual consistency across indices
        _load_raster(
            tif_path,
            f"SpectraLens {index_name.upper()}",
            os.path.join(QML_DIR, "spectralens_ndvi.qml"),
        )

    # 4) Full hyperspectral cube (60-band multipage TIFF)
    cube_zip = _download(
        f"{SPECTRALENS_API}/api/demo/cube.tif",
        os.path.join(work_dir, "cube.zip"),
    )
    cube_tif = _extract_tif(cube_zip, work_dir)
    _load_raster(cube_tif, "SpectraLens Cube (60 bands)")

    # 5) Zones vector
    geojson_path = _download(
        f"{SPECTRALENS_API}/api/demo/zones.geojson",
        os.path.join(work_dir, "zones.geojson"),
    )
    _load_vector(
        geojson_path,
        "SpectraLens Zones",
        os.path.join(QML_DIR, "spectralens_zones.qml"),
    )

    # 6) Frame the canvas to the field
    b = meta["bounds_utm"]
    extent = QgsRectangle(b["min_x"], b["min_y"], b["max_x"], b["max_y"])
    iface.mapCanvas().setExtent(extent)
    iface.mapCanvas().refresh()

    print("Done. SpectraLens layers loaded with styles applied.")


if __name__ == "__main__" or __name__ == "console":
    main()

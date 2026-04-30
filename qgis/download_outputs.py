"""Standalone downloader for SpectraLens outputs (no QGIS required).

Useful for users who want to grab all GIS layers in one shot for use in any
GIS tool (QGIS, ArcGIS Pro, GDAL command line, etc.). Run with plain Python:

  python qgis/download_outputs.py [--api http://localhost:8000] [--out ./gis_out]
"""

import argparse
import os
import sys
import urllib.request
import zipfile


DEFAULT_API = "http://localhost:8000"
INDICES = ["ndvi", "ndre", "gndvi", "savi", "evi", "msavi"]


def _fetch(url: str, dest: str):
    print(f"  -> {url}")
    urllib.request.urlretrieve(url, dest)


def _extract_zip(zip_path: str, dest_dir: str):
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", default=DEFAULT_API, help="SpectraLens API base URL")
    parser.add_argument("--out", default="./gis_out", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # NDVI + indices
    for name in INDICES:
        if name == "ndvi":
            url = f"{args.api}/api/demo/ndvi.tif"
        else:
            url = f"{args.api}/api/demo/index/{name}.tif"
        zip_path = os.path.join(args.out, f"{name}.zip")
        _fetch(url, zip_path)
        _extract_zip(zip_path, args.out)
        os.remove(zip_path)

    # Full cube
    cube_zip = os.path.join(args.out, "cube.zip")
    _fetch(f"{args.api}/api/demo/cube.tif", cube_zip)
    _extract_zip(cube_zip, args.out)
    os.remove(cube_zip)

    # Zones
    _fetch(f"{args.api}/api/demo/zones.geojson", os.path.join(args.out, "spectralens_zones.geojson"))

    # Geospatial metadata
    _fetch(f"{args.api}/api/demo/geospatial", os.path.join(args.out, "geospatial.json"))

    print(f"\nDone. Outputs written to {os.path.abspath(args.out)}")
    print("Open the .tif files and zones.geojson in QGIS to visualize.")


if __name__ == "__main__":
    sys.exit(main())

# SpectraLens

**Spectral Intelligence Platform** — turning hyperspectral drone imagery into plain-English crop health reports. No PhD, no specialist, no waiting.

SpectraLens analyzes hundreds of spectral bands captured by drone-mounted hyperspectral sensors and delivers actionable agronomic insights in seconds. Built for farmers, agri-tech companies, and agricultural researchers who need to act fast during the growing season.

## The Problem

Hyperspectral imagery captures what the human eye cannot — but interpreting 100-500 spectral bands per pixel requires PhD-level remote sensing expertise. Analysis takes weeks. By the time insights arrive, the growing window has passed.

## How SpectraLens Works

1. **Upload** — Drag and drop hyperspectral drone imagery in any standard format (.hdr, .bil, .bip, .img, .tif)
2. **Analyze** — AI reads every spectral band, computes vegetation indices, and identifies health anomalies automatically
3. **Act** — Get a plain-English field health report with zone-by-zone findings and immediate action items

## Features

- **NDVI Mapping** — Interactive normalized difference vegetation index visualization with click-to-inspect pixel analysis
- **Spectral Band Explorer** — Browse all 60 spectral bands (400-1000nm) with real-time rendering and false color composites
- **Pixel-Level Spectral Signatures** — Click any point on the field to see its full spectral fingerprint with reference markers for chlorophyll absorption and NIR plateau
- **AI Field Health Reports** — Claude-powered analysis that interprets spectral data into executive summaries, zone classifications, severity ratings, and recommended actions
- **Zone Analysis** — Automatic detection and classification of healthy crops, nitrogen deficiency, water stress, and pest damage
- **Export** — Download reports or copy summaries to clipboard

## Demo

SpectraLens ships with a synthetic 100x100 pixel hyperspectral demo field (60 bands, 400-1000nm) simulating a corn crop with four distinct health zones:

| Zone | Location | Condition | NDVI |
|------|----------|-----------|------|
| A | NW quadrant | Healthy | ~0.83 |
| B | NE quadrant | Nitrogen deficient | ~0.50 |
| C | SW quadrant | Water stressed | ~0.34 |
| D | SE quadrant | Pest damage | ~0.17 |

## Quick Start

1. Clone the repo:
   ```bash
   git clone https://github.com/rusagara-ops/spectralens.git
   cd spectralens
   ```

2. Add your Anthropic API key to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. Launch:
   ```bash
   bash start.sh
   ```

4. Open http://localhost:5173

The NDVI map, band explorer, and spectral charts work immediately. AI analysis requires a valid Anthropic API key.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS, Recharts |
| Backend | Python, FastAPI, Uvicorn |
| AI | Anthropic Claude API (claude-sonnet-4-20250514) |
| Data Processing | NumPy, SciPy, Pillow |

## Project Structure

```
spectralens/
├── backend/
│   ├── main.py               # FastAPI routes and server config
│   ├── demo_data.py          # Synthetic hyperspectral data generator
│   ├── analysis.py           # NDVI, spectral analysis, image rendering
│   ├── indices.py            # Vegetation index library (NDRE, GNDVI, SAVI, EVI, MSAVI)
│   ├── geospatial.py         # CRS, bounds, pixel <-> world transforms
│   ├── gis_export.py         # GeoTIFF / TFW / PRJ writers
│   ├── vector_export.py      # GeoJSON FeatureCollection builder
│   ├── ai_interpreter.py     # Claude / Gemini API integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main app with dashboard layout
│   │   └── components/
│   │       ├── LandingHero.jsx
│   │       ├── NDVIMap.jsx
│   │       ├── GeoMapView.jsx  # Leaflet map with NDVI overlay + zone polygons
│   │       ├── SpectrumChart.jsx
│   │       ├── BandSlider.jsx
│   │       ├── AIReport.jsx
│   │       ├── ImageViewer.jsx
│   │       ├── UploadZone.jsx
│   │       └── ExportButton.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── qgis/
│   ├── spectralens_ndvi.qml      # Raster pseudocolor style
│   ├── spectralens_zones.qml     # Vector categorized style
│   ├── load_in_qgis.py           # PyQGIS one-click loader
│   └── download_outputs.py       # Standalone bulk downloader
├── start.sh                  # Single command to run everything
└── .env                      # API keys (not committed)
```

## QGIS Integration

SpectraLens is **GIS-native** — every analysis output is georeferenced and exportable to QGIS, ArcGIS, or any tool that reads GeoTIFF / GeoJSON.

The demo plot is anchored to a real-world location near Ames, Iowa, projected in **UTM Zone 15N (EPSG:32615)** with a 0.5 m pixel size. This means everything you produce drops onto a satellite basemap at the right scale.

### What you can pull into QGIS

| Output | Endpoint | Format |
|--------|----------|--------|
| NDVI raster | `/api/demo/ndvi.tif` | Float32 GeoTIFF (.zip with .tif/.tfw/.prj) |
| Single spectral band | `/api/demo/band/{i}.tif` | Float32 GeoTIFF |
| Full hyperspectral cube | `/api/demo/cube.tif` | 60-band GeoTIFF |
| Vegetation index (NDRE/GNDVI/SAVI/EVI/MSAVI) | `/api/demo/index/{name}.tif` | Float32 GeoTIFF |
| Health zones | `/api/demo/zones.geojson` | GeoJSON FeatureCollection |
| Geospatial metadata | `/api/demo/geospatial` | JSON (CRS, bounds, geotransform) |

### One-click load (PyQGIS)

With the backend running, open QGIS, then `Plugins > Python Console > Show Editor`, open `qgis/load_in_qgis.py`, and run. The script:

1. Sets the project CRS to UTM Zone 15N.
2. Downloads NDVI, the full hyperspectral cube, and all five vegetation indices as GeoTIFFs.
3. Loads them as raster layers with the `qgis/spectralens_ndvi.qml` pseudocolor style applied.
4. Loads the zones GeoJSON as a vector layer with a categorized renderer (`qgis/spectralens_zones.qml`).
5. Frames the map canvas to the field bounds.

### Standalone download (no QGIS dependency)

```bash
python qgis/download_outputs.py --api http://localhost:8000 --out ./gis_out
```

Drops every layer as `.tif` / `.geojson` / `.tfw` / `.prj` into `./gis_out`. Open them in QGIS, ArcGIS Pro, GDAL, or any GIS tool.

### Layer styles

- `qgis/spectralens_ndvi.qml` — Red-Yellow-Green pseudocolor for NDVI / index rasters (-0.2 to 0.9).
- `qgis/spectralens_zones.qml` — Categorized fill by `classification` attribute (Healthy → Pest Damage), with auto labels showing `Zone X — NDVI 0.83`.

QGIS auto-loads a `.qml` placed alongside the data file with the same basename. Otherwise: `Layer Properties > Symbology > Style > Load Style`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health check |
| GET | `/api/demo/cube-info` | Hyperspectral cube metadata (incl. geospatial block) |
| GET | `/api/demo/geospatial` | CRS, bounds, geotransform |
| GET | `/api/demo/band/{index}` | Single band PNG preview |
| GET | `/api/demo/band/{index}.tif` | Single band GeoTIFF (zipped with sidecars) |
| GET | `/api/demo/cube.tif` | Multi-band GeoTIFF (60 bands) |
| GET | `/api/demo/false-color` | False color composite |
| GET | `/api/demo/ndvi` | NDVI map PNG with statistics |
| GET | `/api/demo/ndvi.tif` | NDVI as float32 GeoTIFF |
| GET | `/api/demo/indices` | List supported vegetation indices |
| GET | `/api/demo/index/{name}.tif` | NDRE/GNDVI/SAVI/EVI/MSAVI GeoTIFF |
| GET | `/api/demo/index/{name}/stats` | Mean/min/max/std for an index |
| GET | `/api/demo/zones.geojson` | Health zones as GeoJSON |
| GET | `/api/demo/pixel-spectrum?x=&y=` | Pixel spectral signature |
| POST | `/api/demo/analyze` | AI-powered field analysis |
| POST | `/api/upload` | File upload (future feature) |

## License

MIT

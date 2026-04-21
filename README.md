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
│   ├── ai_interpreter.py     # Claude API integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main app with dashboard layout
│   │   └── components/
│   │       ├── LandingHero.jsx
│   │       ├── NDVIMap.jsx
│   │       ├── SpectrumChart.jsx
│   │       ├── BandSlider.jsx
│   │       ├── AIReport.jsx
│   │       ├── ImageViewer.jsx
│   │       ├── UploadZone.jsx
│   │       └── ExportButton.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── start.sh                  # Single command to run everything
└── .env                      # API keys (not committed)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health check |
| GET | `/api/demo/cube-info` | Hyperspectral cube metadata |
| GET | `/api/demo/band/{index}` | Single band image (0-59) |
| GET | `/api/demo/false-color` | False color composite |
| GET | `/api/demo/ndvi` | NDVI map with statistics |
| GET | `/api/demo/pixel-spectrum?x=&y=` | Pixel spectral signature |
| POST | `/api/demo/analyze` | AI-powered field analysis |
| POST | `/api/upload` | File upload (future feature) |

## License

MIT

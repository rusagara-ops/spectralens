"""FastAPI app entry point for SpectraLens."""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware

from demo_data import generate_demo_cube, get_wavelengths, get_zone_labels
from analysis import (
    compute_ndvi,
    get_pixel_spectrum,
    render_band_image,
    render_false_color,
    render_ndvi_map,
    compute_zone_statistics,
)
from ai_interpreter import interpret_field

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

if not os.getenv("ANTHROPIC_API_KEY"):
    print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set. AI analysis will fail.")
    print("   Add your key to spectralens/.env\n")

app = FastAPI(title="SpectraLens API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generate demo data once at startup
print("Generating synthetic hyperspectral data...")
DEMO_CUBE = generate_demo_cube()
WAVELENGTHS = get_wavelengths()
DEMO_NDVI = compute_ndvi(DEMO_CUBE, WAVELENGTHS)
print(f"Demo cube ready: {DEMO_CUBE.shape}, NDVI range: {DEMO_NDVI.min():.2f} to {DEMO_NDVI.max():.2f}")

# Cache for AI analysis result
_analysis_cache = None


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/demo/cube-info")
def cube_info():
    return {
        "shape": list(DEMO_CUBE.shape),
        "wavelengths": WAVELENGTHS,
        "band_count": 60,
        "spatial_resolution": "0.1m per pixel (simulated)",
        "sensor": "Demo VNIR Sensor (400-1000nm)",
    }


@app.get("/api/demo/band/{band_index}")
def get_band(band_index: int):
    if band_index < 0 or band_index > 59:
        raise HTTPException(status_code=400, detail="band_index must be 0-59")
    image_b64 = render_band_image(DEMO_CUBE, band_index)
    return {
        "image_base64": image_b64,
        "wavelength_nm": WAVELENGTHS[band_index],
        "band_index": band_index,
    }


@app.get("/api/demo/false-color")
def false_color(
    r_band: int = Query(default=45),
    g_band: int = Query(default=25),
    b_band: int = Query(default=10),
):
    for b in [r_band, g_band, b_band]:
        if b < 0 or b > 59:
            raise HTTPException(status_code=400, detail="Band indices must be 0-59")
    image_b64 = render_false_color(DEMO_CUBE, r_band, g_band, b_band)
    return {
        "image_base64": image_b64,
        "r_nm": WAVELENGTHS[r_band],
        "g_nm": WAVELENGTHS[g_band],
        "b_nm": WAVELENGTHS[b_band],
    }


@app.get("/api/demo/ndvi")
def ndvi_map():
    image_b64 = render_ndvi_map(DEMO_NDVI)
    return {
        "image_base64": image_b64,
        "mean_ndvi": round(float(DEMO_NDVI.mean()), 4),
        "min_ndvi": round(float(DEMO_NDVI.min()), 4),
        "max_ndvi": round(float(DEMO_NDVI.max()), 4),
    }


@app.get("/api/demo/pixel-spectrum")
def pixel_spectrum(
    x: int = Query(ge=0, le=99),
    y: int = Query(ge=0, le=99),
):
    data = get_pixel_spectrum(DEMO_CUBE, x, y, WAVELENGTHS)
    data["x"] = x
    data["y"] = y
    return data


@app.post("/api/demo/analyze")
async def analyze_field():
    global _analysis_cache
    if _analysis_cache is not None:
        return _analysis_cache

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY not set. Add it to spectralens/.env",
        )

    zone_stats = compute_zone_statistics(DEMO_CUBE, DEMO_NDVI)
    ndvi_stats = {
        "overall_mean_ndvi": zone_stats["overall_mean_ndvi"],
        "overall_min_ndvi": zone_stats["overall_min_ndvi"],
        "overall_max_ndvi": zone_stats["overall_max_ndvi"],
    }

    result = await interpret_field(zone_stats, WAVELENGTHS, ndvi_stats)
    _analysis_cache = result
    return result


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "message": "File received. Full upload support coming soon.",
        "filename": file.filename,
        "redirect": "demo",
    }

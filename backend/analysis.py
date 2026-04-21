"""Spectral analysis functions for SpectraLens."""

import io
import base64
import numpy as np
from PIL import Image


def compute_ndvi(cube: np.ndarray, wavelengths: list) -> np.ndarray:
    """
    NDVI = (NIR - Red) / (NIR + Red)
    Find band closest to 670nm (red) and 800nm (NIR).
    Returns 2D array (100, 100) with NDVI values -1 to 1.
    """
    wl = np.array(wavelengths)
    red_idx = int(np.argmin(np.abs(wl - 670)))
    nir_idx = int(np.argmin(np.abs(wl - 800)))

    red = cube[:, :, red_idx].astype(np.float64)
    nir = cube[:, :, nir_idx].astype(np.float64)

    denominator = nir + red
    with np.errstate(divide='ignore', invalid='ignore'):
        ndvi = np.where(denominator == 0, 0.0, (nir - red) / denominator)
    return ndvi.astype(np.float32)


def get_pixel_spectrum(cube: np.ndarray, x: int, y: int, wavelengths: list) -> dict:
    """
    Return spectral signature for a single pixel.
    Returns: {wavelengths: [...], reflectance: [...], ndvi: float}
    """
    spectrum = cube[y, x, :].tolist()
    wl = np.array(wavelengths)
    red_idx = int(np.argmin(np.abs(wl - 670)))
    nir_idx = int(np.argmin(np.abs(wl - 800)))

    red = float(cube[y, x, red_idx])
    nir = float(cube[y, x, nir_idx])
    ndvi = (nir - red) / (nir + red) if (nir + red) != 0 else 0.0

    return {
        "wavelengths": wavelengths,
        "reflectance": spectrum,
        "ndvi": round(ndvi, 4),
    }


def render_band_image(cube: np.ndarray, band_index: int) -> str:
    """Render a single band as a grayscale PNG, return as base64 string."""
    band = cube[:, :, band_index]
    normalized = (band / band.max() * 255).astype(np.uint8) if band.max() > 0 else np.zeros_like(band, dtype=np.uint8)
    img = Image.fromarray(normalized, mode="L")
    # Scale up for better visibility
    img = img.resize((400, 400), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def render_false_color(cube: np.ndarray, r_band: int, g_band: int, b_band: int) -> str:
    """Render false color composite as PNG, return as base64 string."""
    def normalize_band(band):
        mn, mx = band.min(), band.max()
        if mx - mn == 0:
            return np.zeros_like(band, dtype=np.uint8)
        return ((band - mn) / (mx - mn) * 255).astype(np.uint8)

    r = normalize_band(cube[:, :, r_band])
    g = normalize_band(cube[:, :, g_band])
    b = normalize_band(cube[:, :, b_band])

    rgb = np.stack([r, g, b], axis=-1)
    img = Image.fromarray(rgb, mode="RGB")
    img = img.resize((400, 400), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def render_ndvi_map(ndvi: np.ndarray) -> str:
    """
    Render NDVI map as colored PNG.
    Color scale: red (low <0.2) -> yellow (0.2-0.4) -> light green (0.4-0.6) -> dark green (>0.6)
    Return as base64 string.
    """
    h, w = ndvi.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)

    for y in range(h):
        for x in range(w):
            v = ndvi[y, x]
            if v < 0.2:
                # Red
                rgb[y, x] = [220, 50, 50]
            elif v < 0.4:
                # Yellow (interpolate from red to yellow)
                t = (v - 0.2) / 0.2
                rgb[y, x] = [220, int(50 + 170 * t), 50]
            elif v < 0.6:
                # Light green (interpolate from yellow to light green)
                t = (v - 0.4) / 0.2
                rgb[y, x] = [int(220 - 140 * t), 220, int(50 + 50 * t)]
            else:
                # Dark green (interpolate from light green to dark green)
                t = min((v - 0.6) / 0.3, 1.0)
                rgb[y, x] = [int(80 - 55 * t), int(220 - 60 * t), int(100 - 60 * t)]

    img = Image.fromarray(rgb, mode="RGB")
    img = img.resize((400, 400), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def compute_zone_statistics(cube: np.ndarray, ndvi: np.ndarray) -> dict:
    """
    Compute statistics for each 40x40 zone.
    Returns structured dict for AI prompt injection.
    """
    wavelengths = [400.0 + i * 10.0 for i in range(60)]

    zones = {
        "Zone A (NW quadrant)": {"rows": slice(0, 40), "cols": slice(0, 40)},
        "Zone B (NE quadrant)": {"rows": slice(0, 40), "cols": slice(60, 100)},
        "Zone C (SW quadrant)": {"rows": slice(60, 100), "cols": slice(0, 40)},
        "Zone D (SE quadrant)": {"rows": slice(60, 100), "cols": slice(60, 100)},
    }

    health_thresholds = [
        (0.6, 2.0, "Healthy"),
        (0.4, 0.6, "Nitrogen Deficient"),
        (0.25, 0.4, "Water Stressed"),
        (-2.0, 0.25, "Pest Damage"),
    ]

    results = {}
    for zone_name, slices in zones.items():
        zone_cube = cube[slices["rows"], slices["cols"], :]
        zone_ndvi = ndvi[slices["rows"], slices["cols"]]

        mean_ndvi = float(np.mean(zone_ndvi))
        mean_reflectance = [float(np.mean(zone_cube[:, :, b])) for b in range(60)]

        # Classify health
        health = "Unknown"
        for low, high, label in health_thresholds:
            if low <= mean_ndvi < high:
                health = label
                break

        results[zone_name] = {
            "mean_ndvi": round(mean_ndvi, 4),
            "min_ndvi": round(float(np.min(zone_ndvi)), 4),
            "max_ndvi": round(float(np.max(zone_ndvi)), 4),
            "std_ndvi": round(float(np.std(zone_ndvi)), 4),
            "mean_reflectance_per_band": [round(v, 4) for v in mean_reflectance],
            "health_classification": health,
            "pixel_count": int(zone_cube.shape[0] * zone_cube.shape[1]),
        }

    return {
        "zones": results,
        "wavelengths": wavelengths,
        "overall_mean_ndvi": round(float(np.mean(ndvi)), 4),
        "overall_min_ndvi": round(float(np.min(ndvi)), 4),
        "overall_max_ndvi": round(float(np.max(ndvi)), 4),
    }

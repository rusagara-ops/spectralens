"""Synthetic hyperspectral data generator for SpectraLens demo."""

import numpy as np


def get_wavelengths() -> list:
    """Returns list of 60 wavelengths in nm: [400, 410, ..., 990]."""
    return [400.0 + i * 10.0 for i in range(60)]


def get_zone_labels() -> dict:
    """Returns {zone_name: description} for the 4 zones."""
    return {
        "Zone A (NW)": "Healthy crops — high NIR reflectance, normal red absorption",
        "Zone B (NE)": "Nitrogen deficiency — elevated red, reduced NIR",
        "Zone C (SW)": "Water stress — reduced overall reflectance, water absorption dips",
        "Zone D (SE)": "Pest damage — irregular spectral pattern, low NIR, elevated red",
    }


def _spectral_profile(wavelengths: np.ndarray, zone: str) -> np.ndarray:
    """Generate a realistic spectral reflectance profile for a given zone type."""
    wl = wavelengths
    profile = np.zeros_like(wl, dtype=np.float32)

    if zone == "healthy":
        # Strong chlorophyll absorption at ~670nm, high NIR plateau at ~800nm+
        for i, w in enumerate(wl):
            if w < 500:
                profile[i] = 0.05 + 0.02 * (w - 400) / 100
            elif w < 550:
                profile[i] = 0.12 + 0.08 * (w - 500) / 50  # green peak
            elif w < 680:
                profile[i] = 0.20 - 0.15 * (w - 550) / 130  # red absorption
            elif w < 720:
                profile[i] = 0.05 + 0.55 * (w - 680) / 40  # red edge
            else:
                profile[i] = 0.60 + 0.10 * np.sin((w - 720) / 100)  # NIR plateau

    elif zone == "nitrogen_deficient":
        # Target NDVI ~0.45: Red ~0.15, NIR ~0.40
        for i, w in enumerate(wl):
            if w < 500:
                profile[i] = 0.06 + 0.03 * (w - 400) / 100
            elif w < 550:
                profile[i] = 0.10 + 0.05 * (w - 500) / 50
            elif w < 680:
                profile[i] = 0.15 - 0.01 * (w - 550) / 130  # slightly elevated red
            elif w < 720:
                profile[i] = 0.14 + 0.26 * (w - 680) / 40
            else:
                profile[i] = 0.40 + 0.03 * np.sin((w - 720) / 100)  # moderately reduced NIR

    elif zone == "water_stress":
        # Target NDVI ~0.35: Red ~0.16, NIR ~0.30
        for i, w in enumerate(wl):
            if w < 500:
                profile[i] = 0.04 + 0.02 * (w - 400) / 100
            elif w < 550:
                profile[i] = 0.08 + 0.04 * (w - 500) / 50
            elif w < 680:
                profile[i] = 0.12 + 0.04 * (w - 550) / 130  # elevated red reflectance
            elif w < 720:
                profile[i] = 0.16 + 0.14 * (w - 680) / 40
            elif w < 930:
                profile[i] = 0.30 + 0.02 * np.sin((w - 720) / 100)  # low NIR
            else:
                profile[i] = 0.22 - 0.08 * (w - 930) / 70  # water absorption dip

    elif zone == "pest_damage":
        # Target NDVI ~0.20: Red ~0.18, NIR ~0.27
        for i, w in enumerate(wl):
            if w < 500:
                profile[i] = 0.07 + 0.02 * (w - 400) / 100
            elif w < 550:
                profile[i] = 0.08 + 0.02 * (w - 500) / 50
            elif w < 680:
                profile[i] = 0.10 + 0.08 * (w - 550) / 130  # elevated red
            elif w < 720:
                profile[i] = 0.18 + 0.05 * (w - 680) / 40
            else:
                profile[i] = 0.23 + 0.02 * np.sin((w - 720) / 80)  # very low NIR

    return np.clip(profile, 0.0, 1.0)


def generate_demo_cube() -> np.ndarray:
    """Returns shape (100, 100, 60) float32 array, values 0.0-1.0."""
    rng = np.random.RandomState(42)
    wavelengths = np.array(get_wavelengths())
    cube = np.zeros((100, 100, 60), dtype=np.float32)

    # Generate base profiles for each zone
    healthy = _spectral_profile(wavelengths, "healthy")
    nitrogen = _spectral_profile(wavelengths, "nitrogen_deficient")
    water = _spectral_profile(wavelengths, "water_stress")
    pest = _spectral_profile(wavelengths, "pest_damage")

    # Fill zones with per-pixel noise
    for y in range(100):
        for x in range(100):
            noise = rng.normal(0, 0.015, 60).astype(np.float32)

            if y < 40 and x < 40:
                # Zone A — NW — Healthy
                cube[y, x, :] = healthy + noise
            elif y < 40 and x >= 60:
                # Zone B — NE — Nitrogen deficient
                cube[y, x, :] = nitrogen + noise
            elif y >= 60 and x < 40:
                # Zone C — SW — Water stress
                cube[y, x, :] = water + noise
            elif y >= 60 and x >= 60:
                # Zone D — SE — Pest damage
                cube[y, x, :] = pest + noise
            else:
                # Border/transition zone — blend neighbors
                weights = []
                profiles = []

                # Distance-based blending to nearby zone centers
                dA = np.sqrt((y - 20) ** 2 + (x - 20) ** 2) / 40
                dB = np.sqrt((y - 20) ** 2 + (x - 80) ** 2) / 40
                dC = np.sqrt((y - 80) ** 2 + (x - 20) ** 2) / 40
                dD = np.sqrt((y - 80) ** 2 + (x - 80) ** 2) / 40

                wA = max(0, 1 - dA)
                wB = max(0, 1 - dB)
                wC = max(0, 1 - dC)
                wD = max(0, 1 - dD)

                total = wA + wB + wC + wD + 1e-8
                blended = (
                    wA / total * healthy
                    + wB / total * nitrogen
                    + wC / total * water
                    + wD / total * pest
                )
                cube[y, x, :] = blended + noise * 1.5  # more noise in borders

    return np.clip(cube, 0.0, 1.0)

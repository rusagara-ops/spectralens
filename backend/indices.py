"""Vegetation indices library — NDVI, NDRE, GNDVI, SAVI, EVI, MSAVI.

Each index returns a 2D float32 array aligned with the input cube. Wavelengths
are matched to the closest available band so the same code works for any
sensor (60-band demo, 224-band AVIRIS, 5-band MicaSense, etc.).
"""

import numpy as np

# Canonical wavelengths (nm) for each spectral region
BLUE_NM = 470
GREEN_NM = 550
RED_NM = 670
RED_EDGE_NM = 720
NIR_NM = 800


def _band_at(cube: np.ndarray, wavelengths, target_nm: float) -> np.ndarray:
    """Return the band closest to target_nm as a float64 2D array."""
    wl = np.asarray(wavelengths)
    idx = int(np.argmin(np.abs(wl - target_nm)))
    return cube[:, :, idx].astype(np.float64)


def _safe_divide(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(den == 0, 0.0, num / den).astype(np.float32)


def ndvi(cube, wavelengths):
    """Normalized Difference Vegetation Index — general crop vigor."""
    red = _band_at(cube, wavelengths, RED_NM)
    nir = _band_at(cube, wavelengths, NIR_NM)
    return _safe_divide(nir - red, nir + red)


def ndre(cube, wavelengths):
    """Normalized Difference Red Edge — sensitive to nitrogen / chlorophyll content."""
    re = _band_at(cube, wavelengths, RED_EDGE_NM)
    nir = _band_at(cube, wavelengths, NIR_NM)
    return _safe_divide(nir - re, nir + re)


def gndvi(cube, wavelengths):
    """Green NDVI — uses green band; less saturation in dense canopy than NDVI."""
    green = _band_at(cube, wavelengths, GREEN_NM)
    nir = _band_at(cube, wavelengths, NIR_NM)
    return _safe_divide(nir - green, nir + green)


def savi(cube, wavelengths, L: float = 0.5):
    """Soil-Adjusted Vegetation Index — corrects for bare-soil background."""
    red = _band_at(cube, wavelengths, RED_NM)
    nir = _band_at(cube, wavelengths, NIR_NM)
    return _safe_divide((nir - red) * (1 + L), nir + red + L)


def evi(cube, wavelengths):
    """Enhanced Vegetation Index — atmospherically resistant, high biomass sensitivity."""
    blue = _band_at(cube, wavelengths, BLUE_NM)
    red = _band_at(cube, wavelengths, RED_NM)
    nir = _band_at(cube, wavelengths, NIR_NM)
    G = 2.5
    C1, C2, L = 6.0, 7.5, 1.0
    return _safe_divide(G * (nir - red), nir + C1 * red - C2 * blue + L)


def msavi(cube, wavelengths):
    """Modified SAVI — self-adjusting soil correction, no L parameter needed."""
    red = _band_at(cube, wavelengths, RED_NM)
    nir = _band_at(cube, wavelengths, NIR_NM)
    inner = (2 * nir + 1) ** 2 - 8 * (nir - red)
    inner = np.clip(inner, 0, None)
    return ((2 * nir + 1 - np.sqrt(inner)) / 2).astype(np.float32)


INDEX_FUNCS = {
    "ndvi": ndvi,
    "ndre": ndre,
    "gndvi": gndvi,
    "savi": savi,
    "evi": evi,
    "msavi": msavi,
}


INDEX_DESCRIPTIONS = {
    "ndvi": "Normalized Difference Vegetation Index — general crop vigor (-1 to 1).",
    "ndre": "Normalized Difference Red Edge — nitrogen / chlorophyll status.",
    "gndvi": "Green NDVI — better than NDVI for dense canopy.",
    "savi": "Soil-Adjusted Vegetation Index — corrects for soil background.",
    "evi": "Enhanced Vegetation Index — atmospheric correction, high biomass.",
    "msavi": "Modified SAVI — self-adjusting soil correction.",
}


def compute(name: str, cube, wavelengths):
    """Dispatch to the requested index by name."""
    fn = INDEX_FUNCS.get(name.lower())
    if fn is None:
        raise ValueError(f"Unknown index: {name}. Options: {list(INDEX_FUNCS)}")
    return fn(cube, wavelengths)

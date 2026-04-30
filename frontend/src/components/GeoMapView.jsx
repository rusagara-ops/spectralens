import React, { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const ZONE_COLORS = {
  Healthy: '#268c43',
  'Nitrogen Deficient': '#f1c40f',
  'Water Stressed': '#e67e22',
  'Pest Damage': '#c0392b',
}

export default function GeoMapView({ ndviData, onPixelClick }) {
  const mapEl = useRef(null)
  const mapRef = useRef(null)
  const ndviLayerRef = useRef(null)
  const zonesLayerRef = useRef(null)
  const [meta, setMeta] = useState(null)
  const [zones, setZones] = useState(null)
  const [showNdvi, setShowNdvi] = useState(true)
  const [showZones, setShowZones] = useState(true)

  // Pull geospatial bounds + zones once
  useEffect(() => {
    fetch('/api/demo/geospatial')
      .then((r) => r.json())
      .then(setMeta)
      .catch((err) => console.error('geospatial fetch failed:', err))

    fetch('/api/demo/zones.geojson')
      .then((r) => r.json())
      .then(setZones)
      .catch((err) => console.error('zones fetch failed:', err))
  }, [])

  // Initialize Leaflet map once meta is available
  useEffect(() => {
    if (!meta || !mapEl.current || mapRef.current) return

    const { south, west, north, east } = meta.bounds_wgs84
    const bounds = L.latLngBounds([south, west], [north, east])

    const map = L.map(mapEl.current, {
      zoomControl: true,
      attributionControl: true,
    }).fitBounds(bounds, { padding: [20, 20] })

    // Esri World Imagery — high-res satellite, free for non-commercial demos
    L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      {
        maxZoom: 22,
        attribution: 'Imagery © Esri, Maxar, Earthstar Geographics',
      }
    ).addTo(map)

    // Click handler — translate map click back to pixel coordinates
    map.on('click', (e) => {
      const { south, west, north, east } = meta.bounds_wgs84
      const fracX = (e.latlng.lng - west) / (east - west)
      const fracY = (north - e.latlng.lat) / (north - south)
      const px = Math.round(fracX * (meta.grid_width - 1))
      const py = Math.round(fracY * (meta.grid_height - 1))
      if (px >= 0 && px < meta.grid_width && py >= 0 && py < meta.grid_height) {
        onPixelClick?.(px, py)
      }
    })

    mapRef.current = map
    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [meta, onPixelClick])

  // NDVI raster overlay (uses the existing PNG endpoint, georeferenced via bounds)
  useEffect(() => {
    if (!mapRef.current || !meta || !ndviData?.image_base64) return

    if (ndviLayerRef.current) {
      mapRef.current.removeLayer(ndviLayerRef.current)
      ndviLayerRef.current = null
    }

    if (!showNdvi) return

    const { south, west, north, east } = meta.bounds_wgs84
    const url = `data:image/png;base64,${ndviData.image_base64}`
    const overlay = L.imageOverlay(url, [[south, west], [north, east]], {
      opacity: 0.7,
    }).addTo(mapRef.current)

    ndviLayerRef.current = overlay
  }, [meta, ndviData, showNdvi])

  // Zone polygons
  useEffect(() => {
    if (!mapRef.current || !zones) return

    if (zonesLayerRef.current) {
      mapRef.current.removeLayer(zonesLayerRef.current)
      zonesLayerRef.current = null
    }

    if (!showZones) return

    const layer = L.geoJSON(zones, {
      style: (feature) => ({
        color: '#0f172a',
        weight: 1.5,
        fillColor: ZONE_COLORS[feature.properties.classification] || '#94a3b8',
        fillOpacity: 0.25,
      }),
      onEachFeature: (feature, lyr) => {
        const p = feature.properties
        lyr.bindPopup(
          `<strong>${p.zone_name}</strong><br/>` +
            `<span style="color:#475569">Classification:</span> ${p.classification}<br/>` +
            `<span style="color:#475569">Mean NDVI:</span> ${p.mean_ndvi}<br/>` +
            `<span style="color:#475569">NDVI range:</span> ${p.min_ndvi} – ${p.max_ndvi}<br/>` +
            `<span style="color:#475569">Pixels:</span> ${p.pixel_count}`
        )
      },
    }).addTo(mapRef.current)

    zonesLayerRef.current = layer
  }, [zones, showZones])

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-4 text-xs">
        <label className="flex items-center gap-1.5 cursor-pointer">
          <input
            type="checkbox"
            checked={showNdvi}
            onChange={(e) => setShowNdvi(e.target.checked)}
          />
          NDVI overlay
        </label>
        <label className="flex items-center gap-1.5 cursor-pointer">
          <input
            type="checkbox"
            checked={showZones}
            onChange={(e) => setShowZones(e.target.checked)}
          />
          Zone polygons
        </label>
        {meta && (
          <span className="ml-auto text-slate-500">
            CRS: {meta.crs_projected} · {meta.location_name}
          </span>
        )}
      </div>
      <div
        ref={mapEl}
        className="w-full rounded-lg border border-slate-200 shadow-sm"
        style={{ height: '500px' }}
      />
      <p className="text-xs text-slate-500">
        Click anywhere on the field to inspect that pixel's spectral signature. Same
        georeferenced layers (NDVI, zones, indices) are downloadable for QGIS via{' '}
        <code className="bg-slate-100 px-1 rounded">/api/demo/ndvi.tif</code>.
      </p>
    </div>
  )
}

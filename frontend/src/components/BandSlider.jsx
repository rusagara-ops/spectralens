import React from 'react'

const BAND_LABELS = {
  0: '400nm — Violet',
  5: '450nm — Blue',
  10: '500nm — Cyan',
  15: '550nm — Green',
  20: '600nm — Orange',
  25: '650nm — Red',
  27: '670nm — Red (Chlorophyll absorption)',
  30: '700nm — Red edge',
  35: '750nm — NIR onset',
  40: '800nm — NIR',
  45: '850nm — NIR plateau',
  50: '900nm — NIR',
  55: '950nm — Water absorption',
  59: '990nm — SWIR onset',
}

function getWavelengthLabel(band) {
  if (BAND_LABELS[band]) return BAND_LABELS[band]
  const nm = 400 + band * 10
  let region = 'Visible'
  if (nm >= 700) region = 'NIR'
  if (nm >= 950) region = 'SWIR onset'
  return `${nm}nm — ${region}`
}

export default function BandSlider({ selectedBand, onChange, onPreset }) {
  const nm = 400 + selectedBand * 10

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-slate-700">Spectral Band Explorer</span>
        <span className="text-xs font-mono text-brand bg-brand/10 px-2 py-0.5 rounded">
          Band {selectedBand} — {nm}nm
        </span>
      </div>
      <input
        type="range"
        min={0}
        max={59}
        value={selectedBand}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="w-full h-2 rounded-lg appearance-none cursor-pointer accent-brand bg-gradient-to-r from-violet-400 via-green-400 via-60% to-red-900"
      />
      <div className="flex justify-between text-xs text-slate-400 mt-1">
        <span>400nm</span>
        <span>700nm</span>
        <span>990nm</span>
      </div>
      <p className="text-xs text-slate-500 mt-2">{getWavelengthLabel(selectedBand)}</p>

      <div className="flex gap-2 mt-3">
        <button
          onClick={() => onPreset('natural')}
          className="text-xs px-3 py-1.5 rounded-md border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors"
        >
          Natural Color
        </button>
        <button
          onClick={() => onPreset('vegetation')}
          className="text-xs px-3 py-1.5 rounded-md border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors"
        >
          Vegetation (NIR)
        </button>
        <button
          onClick={() => onPreset('mineral')}
          className="text-xs px-3 py-1.5 rounded-md border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors"
        >
          False Color
        </button>
      </div>
    </div>
  )
}

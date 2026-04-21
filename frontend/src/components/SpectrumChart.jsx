import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
} from 'recharts'

export default function SpectrumChart({ pixelSpectrum }) {
  if (!pixelSpectrum) {
    return (
      <div className="h-full flex items-center justify-center text-slate-400 text-sm">
        <div className="text-center">
          <svg className="w-12 h-12 mx-auto mb-3 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.042 21.672L13.684 16.6m0 0l-2.51 2.225.569-9.47 5.227 7.917-3.286-.672zM12 2.25V4.5m5.834.166l-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243l-1.59-1.591" />
          </svg>
          <p className="font-medium text-slate-500">Click any pixel on the NDVI map</p>
          <p className="text-xs text-slate-400 mt-1">to see its spectral signature</p>
        </div>
      </div>
    )
  }

  const data = pixelSpectrum.wavelengths.map((wl, i) => ({
    wavelength: wl,
    reflectance: parseFloat(pixelSpectrum.reflectance[i].toFixed(4)),
  }))

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-3">
        <div>
          <span className="text-sm font-medium text-slate-700">
            Pixel ({pixelSpectrum.x}, {pixelSpectrum.y})
          </span>
          <span className={`ml-3 text-xs font-mono px-2 py-0.5 rounded ${
            pixelSpectrum.ndvi > 0.6
              ? 'bg-green-100 text-green-700'
              : pixelSpectrum.ndvi > 0.4
              ? 'bg-yellow-100 text-yellow-700'
              : 'bg-red-100 text-red-700'
          }`}>
            NDVI: {pixelSpectrum.ndvi.toFixed(3)}
          </span>
        </div>
      </div>

      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height={340}>
          <LineChart data={data} margin={{ top: 10, right: 20, bottom: 30, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis
              dataKey="wavelength"
              label={{ value: 'Wavelength (nm)', position: 'bottom', offset: 10, style: { fontSize: 12, fill: '#64748b' } }}
              tick={{ fontSize: 11, fill: '#94a3b8' }}
            />
            <YAxis
              domain={[0, 'auto']}
              allowDataOverflow={false}
              label={{ value: 'Reflectance', angle: -90, position: 'insideLeft', offset: -5, style: { fontSize: 12, fill: '#64748b' } }}
              tick={{ fontSize: 11, fill: '#94a3b8' }}
            />
            <Tooltip
              contentStyle={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', fontSize: '12px' }}
              formatter={(value) => [value.toFixed(4), 'Reflectance']}
              labelFormatter={(label) => `${label} nm`}
            />
            <ReferenceLine
              x={670}
              stroke="#dc2626"
              strokeDasharray="4 4"
              label={{ value: '670nm Chlorophyll', position: 'top', fill: '#dc2626', fontSize: 10 }}
            />
            <ReferenceLine
              x={800}
              stroke="#1a5c38"
              strokeDasharray="4 4"
              label={{ value: '800nm NIR plateau', position: 'top', fill: '#1a5c38', fontSize: 10 }}
            />
            <Line
              type="monotone"
              dataKey="reflectance"
              stroke="#1a5c38"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#1a5c38' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

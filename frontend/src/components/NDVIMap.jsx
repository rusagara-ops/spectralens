import React from 'react'
import ImageViewer from './ImageViewer'

export default function NDVIMap({ ndviData, onPixelClick }) {
  return (
    <div className="h-full flex flex-col">
      <ImageViewer
        imageBase64={ndviData?.image_base64}
        label={ndviData ? `NDVI \u2014 Mean: ${ndviData.mean_ndvi.toFixed(3)}` : null}
        onClick={onPixelClick}
        crosshair
      />

      {/* Legend */}
      <div className="mt-3">
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500">NDVI</span>
          <div className="flex-1 h-3 rounded-full bg-gradient-to-r from-red-500 via-yellow-400 via-50% to-green-700"></div>
        </div>
        <div className="flex justify-between text-xs text-slate-400 mt-1">
          <span>0.0</span>
          <span>0.2</span>
          <span>0.4</span>
          <span>0.6</span>
          <span>0.8+</span>
        </div>
      </div>
      <p className="text-xs text-slate-400 mt-3 text-center">Click any pixel to view its spectral signature</p>
    </div>
  )
}

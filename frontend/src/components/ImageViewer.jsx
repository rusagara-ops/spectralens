import React from 'react'

export default function ImageViewer({ imageBase64, label, onClick, crosshair = false }) {
  const handleClick = (e) => {
    if (!onClick) return
    const rect = e.target.getBoundingClientRect()
    // Map click position to 0-99 pixel coordinates
    const x = Math.floor(((e.clientX - rect.left) / rect.width) * 100)
    const y = Math.floor(((e.clientY - rect.top) / rect.height) * 100)
    onClick(Math.min(99, Math.max(0, x)), Math.min(99, Math.max(0, y)))
  }

  if (!imageBase64) {
    return (
      <div className="w-full aspect-square bg-slate-100 rounded-lg flex items-center justify-center text-slate-400 text-sm">
        Loading image...
      </div>
    )
  }

  return (
    <div className="relative">
      <img
        src={`data:image/png;base64,${imageBase64}`}
        alt={label || 'Spectral image'}
        className={`w-full aspect-square rounded-lg object-contain bg-slate-900 ${
          crosshair ? 'cursor-crosshair' : ''
        }`}
        onClick={handleClick}
      />
      {label && (
        <div className="absolute bottom-2 left-2 bg-black/60 text-white text-xs px-2 py-1 rounded">
          {label}
        </div>
      )}
    </div>
  )
}

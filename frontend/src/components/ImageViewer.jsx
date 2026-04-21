import React, { useRef } from 'react'

export default function ImageViewer({ imageBase64, label, onClick, crosshair = false }) {
  const imgRef = useRef(null)

  const handleClick = (e) => {
    if (!onClick || !imgRef.current) return
    const img = imgRef.current
    const rect = img.getBoundingClientRect()

    // Account for object-fit by using the actual rendered image area
    const naturalW = img.naturalWidth || rect.width
    const naturalH = img.naturalHeight || rect.height

    // For object-cover/contain, the image may not fill the entire element
    // Calculate the actual displayed image bounds
    const containerRatio = rect.width / rect.height
    const imageRatio = naturalW / naturalH

    let renderW, renderH, offsetX, offsetY

    if (containerRatio > imageRatio) {
      // Container is wider — image is height-constrained
      renderH = rect.height
      renderW = rect.height * imageRatio
      offsetX = (rect.width - renderW) / 2
      offsetY = 0
    } else {
      // Container is taller — image is width-constrained
      renderW = rect.width
      renderH = rect.width / imageRatio
      offsetX = 0
      offsetY = (rect.height - renderH) / 2
    }

    const clickX = e.clientX - rect.left - offsetX
    const clickY = e.clientY - rect.top - offsetY

    // Click outside image area
    if (clickX < 0 || clickY < 0 || clickX > renderW || clickY > renderH) return

    const x = Math.floor((clickX / renderW) * 100)
    const y = Math.floor((clickY / renderH) * 100)
    onClick(Math.min(99, Math.max(0, x)), Math.min(99, Math.max(0, y)))
  }

  if (!imageBase64) {
    return (
      <div className="w-full aspect-square bg-slate-100 rounded-lg flex items-center justify-center text-slate-400 text-sm animate-pulse">
        Loading image...
      </div>
    )
  }

  return (
    <div className="relative">
      <img
        ref={imgRef}
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

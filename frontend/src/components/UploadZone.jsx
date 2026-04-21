import React, { useState, useCallback } from 'react'

export default function UploadZone() {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  const handleDrop = useCallback(async (e) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer?.files?.[0] || e.target?.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/upload', { method: 'POST', body: formData })
      const data = await res.json()
      setUploadStatus({ success: true, message: data.message, filename: file.name })
    } catch {
      setUploadStatus({ success: false, message: 'Upload failed. Please try again.' })
    }
  }, [])

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
        isDragging ? 'border-brand bg-brand/5' : 'border-slate-300 hover:border-brand/50'
      }`}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
    >
      <svg className="w-10 h-10 mx-auto mb-3 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
      </svg>
      <p className="text-sm font-medium text-slate-700 mb-1">
        Drag & drop your hyperspectral data
      </p>
      <p className="text-xs text-slate-400 mb-3">
        Accepted formats: .hdr, .bil, .bip, .img, .tif
      </p>
      <label className="inline-block px-4 py-2 text-sm font-medium text-brand border border-brand rounded-lg cursor-pointer hover:bg-brand hover:text-white transition-colors">
        Browse Files
        <input type="file" className="hidden" onChange={handleDrop} accept=".hdr,.bil,.bip,.img,.tif,.tiff" />
      </label>

      {uploadStatus && (
        <div className={`mt-4 p-3 rounded-lg text-sm ${
          uploadStatus.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
        }`}>
          {uploadStatus.success && <span className="font-medium">{uploadStatus.filename}: </span>}
          {uploadStatus.message}
          {uploadStatus.success && (
            <p className="mt-1 text-xs">For now, explore our demo field below.</p>
          )}
        </div>
      )}
    </div>
  )
}

import React, { useState, useEffect, useCallback, useRef } from 'react'
import LandingHero from './components/LandingHero'
import UploadZone from './components/UploadZone'
import ImageViewer from './components/ImageViewer'
import BandSlider from './components/BandSlider'
import SpectrumChart from './components/SpectrumChart'
import NDVIMap from './components/NDVIMap'
import GeoMapView from './components/GeoMapView'
import AIReport from './components/AIReport'
import ExportButton from './components/ExportButton'

const LeafIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1a5c38" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1.55-3.67C11.55 20 17 17.5 19.5 12.5 22 7.5 17 8 17 8z" fill="#1a5c38" opacity="0.15" />
    <path d="M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1.55-3.67C11.55 20 17 17.5 19.5 12.5 22 7.5 17 8 17 8z" />
    <path d="M6 15s3-2 6-2" />
  </svg>
)

const ZONE_INFO = [
  { key: 'nw', name: 'Zone A (NW)', label: 'NW Quadrant' },
  { key: 'ne', name: 'Zone B (NE)', label: 'NE Quadrant' },
  { key: 'sw', name: 'Zone C (SW)', label: 'SW Quadrant' },
  { key: 'se', name: 'Zone D (SE)', label: 'SE Quadrant' },
]

export default function App() {
  const [currentView, setCurrentView] = useState('landing')
  const [analysisData, setAnalysisData] = useState(null)
  const [selectedBand, setSelectedBand] = useState(27)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [pixelSpectrum, setPixelSpectrum] = useState(null)
  const [activeTab, setActiveTab] = useState('ndvi')
  const [bandImage, setBandImage] = useState(null)
  const [bandLoading, setBandLoading] = useState(false)
  const [showUpload, setShowUpload] = useState(false)
  const [ndviData, setNdviData] = useState(null)
  const [error, setError] = useState(null)

  // Abort controllers for cancelling stale requests
  const bandAbort = useRef(null)
  const pixelAbort = useRef(null)

  // Fetch NDVI data once when entering demo view
  useEffect(() => {
    if (currentView !== 'demo') return
    fetch('/api/demo/ndvi')
      .then((r) => r.json())
      .then(setNdviData)
      .catch((err) => console.error('Failed to load NDVI:', err))
  }, [currentView])

  // Fetch band image when band changes, cancel previous request
  useEffect(() => {
    if (currentView !== 'demo') return

    if (bandAbort.current) bandAbort.current.abort()
    const controller = new AbortController()
    bandAbort.current = controller

    setBandLoading(true)
    fetch(`/api/demo/band/${selectedBand}`, { signal: controller.signal })
      .then((r) => r.json())
      .then((data) => {
        setBandImage(data)
        setBandLoading(false)
      })
      .catch((err) => {
        if (err.name !== 'AbortError') {
          console.error('Failed to load band:', err)
          setBandLoading(false)
        }
      })

    return () => controller.abort()
  }, [selectedBand, currentView])

  // Handle pixel click on NDVI map
  const handlePixelClick = useCallback(async (x, y) => {
    if (pixelAbort.current) pixelAbort.current.abort()
    const controller = new AbortController()
    pixelAbort.current = controller

    try {
      const res = await fetch(`/api/demo/pixel-spectrum?x=${x}&y=${y}`, { signal: controller.signal })
      const data = await res.json()
      setPixelSpectrum(data)
      setActiveTab('spectrum')
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('Failed to fetch pixel spectrum:', err)
      }
    }
  }, [])

  // Handle band preset
  const handlePreset = useCallback((type) => {
    if (type === 'natural') setSelectedBand(15)
    else if (type === 'vegetation') setSelectedBand(40)
    else if (type === 'mineral') setSelectedBand(10)
    setActiveTab('band')
  }, [])

  // Run AI analysis
  const handleRunAnalysis = useCallback(async () => {
    setIsAnalyzing(true)
    setActiveTab('report')
    setError(null)
    try {
      const res = await fetch('/api/demo/analyze', { method: 'POST' })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Analysis failed')
      }
      const data = await res.json()
      setAnalysisData(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsAnalyzing(false)
    }
  }, [])

  // Landing page
  if (currentView === 'landing') {
    return <LandingHero onStartDemo={() => setCurrentView('demo')} />
  }

  // Get zone cards from analysis data
  const zoneCards = analysisData?.zones || []
  const overallHealth = analysisData?.overall_field_health

  // Demo dashboard
  return (
    <div className="h-screen flex flex-col bg-slate-50">
      {/* Top bar */}
      <header className="flex items-center justify-between px-6 py-3 bg-white border-b border-slate-200 flex-shrink-0">
        <div className="flex items-center gap-3">
          <button onClick={() => setCurrentView('landing')} className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <LeafIcon />
            <span className="text-lg font-bold text-brand">SpectraLens</span>
          </button>
          <span className="text-xs text-slate-400 bg-slate-100 px-2 py-0.5 rounded">Demo</span>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowUpload(!showUpload)}
            className="text-sm px-4 py-1.5 text-slate-600 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
          >
            Upload Your Data
          </button>
          <button
            onClick={handleRunAnalysis}
            disabled={isAnalyzing}
            className="text-sm px-4 py-1.5 bg-brand text-white font-medium rounded-lg hover:bg-brand-light transition-colors disabled:opacity-50"
          >
            {isAnalyzing ? 'Analyzing...' : 'Run AI Analysis'}
          </button>
        </div>
      </header>

      {/* Upload zone dropdown */}
      {showUpload && (
        <div className="px-6 py-4 bg-white border-b border-slate-200">
          <UploadZone />
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex min-h-0">
        {/* Left panel — 40% */}
        <div className="w-2/5 p-5 overflow-y-auto border-r border-slate-200 bg-white space-y-5">
          {/* Field overview */}
          <div>
            <h2 className="text-lg font-bold text-slate-900 mb-1">Demo Field — Corn Crop, Iowa</h2>
            <p className="text-xs text-slate-500">(Simulated)</p>
            <div className="flex flex-wrap gap-2 mt-2">
              {['100x100 pixels', '60 spectral bands', '400-1000nm', '0.1m resolution'].map((tag) => (
                <span key={tag} className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Health score */}
          <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
            <div className="flex items-center gap-4">
              <div className="relative w-20 h-20 flex-shrink-0">
                <svg className="w-20 h-20 transform -rotate-90" viewBox="0 0 80 80">
                  <circle cx="40" cy="40" r="35" fill="none" stroke="#e2e8f0" strokeWidth="6" />
                  <circle
                    cx="40"
                    cy="40"
                    r="35"
                    fill="none"
                    stroke={overallHealth >= 60 ? '#16a34a' : overallHealth >= 40 ? '#eab308' : overallHealth ? '#dc2626' : '#e2e8f0'}
                    strokeWidth="6"
                    strokeLinecap="round"
                    strokeDasharray={`${(overallHealth || 0) * 2.2} 220`}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className={`text-xl font-bold ${
                    overallHealth >= 60 ? 'text-green-600' : overallHealth >= 40 ? 'text-yellow-600' : overallHealth ? 'text-red-600' : 'text-slate-300'
                  }`}>
                    {overallHealth != null ? `${overallHealth}%` : '\u2014'}
                  </span>
                </div>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-slate-700">Overall Field Health</h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  {overallHealth != null ? 'Based on AI analysis' : 'Run AI analysis to compute'}
                </p>
              </div>
            </div>
          </div>

          {/* Band controls */}
          <div className="bg-white rounded-xl p-4 border border-slate-200">
            <BandSlider selectedBand={selectedBand} onChange={setSelectedBand} onPreset={handlePreset} />
          </div>

          {/* Zone summary cards */}
          <div>
            <h3 className="text-sm font-semibold text-slate-700 mb-3">Zone Summary</h3>
            <div className="grid grid-cols-2 gap-2">
              {ZONE_INFO.map((zone, i) => {
                const zoneData = zoneCards[i]
                const ndvi = zoneData?.ndvi
                const status = zoneData?.health_status

                const statusColors = {
                  Healthy: 'border-l-green-500 bg-green-50/50',
                  'Nitrogen Deficient': 'border-l-yellow-500 bg-yellow-50/50',
                  'Water Stressed': 'border-l-orange-500 bg-orange-50/50',
                  'Pest Damage': 'border-l-red-500 bg-red-50/50',
                }

                return (
                  <div
                    key={zone.key}
                    className={`rounded-lg border border-slate-200 border-l-4 p-3 ${statusColors[status] || 'border-l-slate-300 bg-slate-50/50'}`}
                  >
                    <div className="text-xs font-semibold text-slate-700">{zone.name}</div>
                    {zoneData ? (
                      <>
                        <div className="text-xs text-slate-500 mt-1">
                          NDVI: <span className="font-mono font-medium">{ndvi?.toFixed(2)}</span>
                        </div>
                        <div className={`text-xs mt-1 font-medium ${
                          status === 'Healthy' ? 'text-green-600' :
                          status === 'Nitrogen Deficient' ? 'text-yellow-600' :
                          status === 'Water Stressed' ? 'text-orange-600' :
                          'text-red-600'
                        }`}>
                          {status}
                        </div>
                      </>
                    ) : (
                      <div className="text-xs text-slate-400 mt-1">Awaiting analysis</div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        </div>

        {/* Right panel — 60% */}
        <div className="flex-1 flex flex-col min-h-0">
          {/* Tabs */}
          <div className="flex border-b border-slate-200 bg-white px-5 flex-shrink-0" role="tablist">
            {[
              { id: 'ndvi', label: 'NDVI Map' },
              { id: 'geomap', label: 'Geo Map' },
              { id: 'band', label: 'Band View' },
              { id: 'spectrum', label: 'Spectrum' },
              { id: 'report', label: 'AI Report' },
            ].map((tab) => (
              <button
                key={tab.id}
                role="tab"
                aria-selected={activeTab === tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-brand text-brand'
                    : 'border-transparent text-slate-500 hover:text-slate-700'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab content */}
          <div className="flex-1 p-5 overflow-y-auto">
            {activeTab === 'ndvi' && (
              <div className="max-w-lg mx-auto">
                <NDVIMap ndviData={ndviData} onPixelClick={handlePixelClick} />
              </div>
            )}

            {activeTab === 'geomap' && (
              <div className="max-w-3xl mx-auto">
                <GeoMapView ndviData={ndviData} onPixelClick={handlePixelClick} />
              </div>
            )}

            {activeTab === 'band' && (
              <div className="max-w-lg mx-auto">
                {bandLoading && !bandImage ? (
                  <div className="w-full aspect-square bg-slate-100 rounded-lg flex items-center justify-center text-slate-400 text-sm animate-pulse">
                    Loading band...
                  </div>
                ) : (
                  <ImageViewer
                    imageBase64={bandImage?.image_base64}
                    label={bandImage ? `${bandImage.wavelength_nm}nm \u2014 Band ${bandImage.band_index}` : null}
                  />
                )}
              </div>
            )}

            {activeTab === 'spectrum' && (
              <SpectrumChart pixelSpectrum={pixelSpectrum} />
            )}

            {activeTab === 'report' && (
              <div className="max-w-2xl mx-auto">
                {error && (
                  <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
                    <span className="font-medium">Error: </span>{error}
                  </div>
                )}
                <AIReport
                  analysisData={analysisData}
                  isAnalyzing={isAnalyzing}
                  onRunAnalysis={handleRunAnalysis}
                />
                <ExportButton analysisData={analysisData} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

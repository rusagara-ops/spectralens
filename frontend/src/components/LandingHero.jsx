import React from 'react'

const LeafIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1a5c38" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1.55-3.67C11.55 20 17 17.5 19.5 12.5 22 7.5 17 8 17 8z" fill="#1a5c38" opacity="0.15" />
    <path d="M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1.55-3.67C11.55 20 17 17.5 19.5 12.5 22 7.5 17 8 17 8z" />
    <path d="M6 15s3-2 6-2" />
  </svg>
)

export default function LandingHero({ onStartDemo }) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="flex items-center justify-between px-8 py-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <LeafIcon />
          <span className="text-xl font-bold text-brand">SpectraLens</span>
        </div>
        <button
          onClick={onStartDemo}
          className="px-5 py-2 text-sm font-medium text-brand border border-brand rounded-lg hover:bg-brand hover:text-white transition-colors"
        >
          Request Demo
        </button>
      </header>

      {/* Hero */}
      <section className="flex-1 flex items-center justify-center px-8 py-16">
        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-5xl font-bold text-slate-900 leading-tight mb-6">
              Your crops are talking.{' '}
              <span className="text-brand">We translate.</span>
            </h1>
            <p className="text-lg text-slate-600 mb-8 leading-relaxed">
              SpectraLens turns hyperspectral drone imagery into plain-English crop health
              reports — no PhD, no specialist, no waiting.
            </p>
            <div className="flex gap-4">
              <button
                onClick={onStartDemo}
                className="px-8 py-3 bg-brand text-white font-semibold rounded-lg hover:bg-brand-light transition-colors shadow-lg shadow-brand/20"
              >
                See Live Demo &rarr;
              </button>
              <a
                href="#how-it-works"
                className="px-8 py-3 text-slate-600 font-semibold rounded-lg border border-slate-200 hover:border-slate-400 transition-colors"
              >
                How it works &darr;
              </a>
            </div>
          </div>

          {/* Dashboard mockup card */}
          <div className="bg-slate-50 rounded-2xl border border-slate-200 p-6 shadow-xl">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-3 h-3 rounded-full bg-red-400"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
              <div className="w-3 h-3 rounded-full bg-green-400"></div>
              <span className="ml-2 text-xs text-slate-400">SpectraLens Dashboard</span>
            </div>
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="h-32 rounded-lg bg-gradient-to-br from-green-600 via-yellow-400 to-red-500 opacity-80"></div>
              <div className="space-y-2">
                <div className="h-6 bg-slate-200 rounded w-3/4"></div>
                <div className="h-4 bg-slate-200 rounded w-full"></div>
                <div className="h-4 bg-slate-200 rounded w-5/6"></div>
                <div className="h-8 bg-brand/10 rounded flex items-center justify-center">
                  <span className="text-brand font-bold text-sm">Health: 52%</span>
                </div>
                <div className="h-4 bg-slate-200 rounded w-2/3"></div>
              </div>
            </div>
            <div className="h-20 bg-slate-100 rounded-lg flex items-center justify-center">
              <div className="text-xs text-slate-400">AI Analysis Report Preview</div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section id="how-it-works" className="py-20 px-8 bg-slate-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-slate-900 mb-4">The problem with hyperspectral data</h2>
          <p className="text-center text-slate-500 mb-12 max-w-2xl mx-auto">Hyperspectral imagery captures what the human eye cannot — but interpreting it requires expertise that most farms don't have.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                stat: '100-500',
                unit: 'spectral bands per image',
                desc: 'Traditional software requires specialist expertise to interpret',
              },
              {
                stat: 'Weeks',
                unit: 'of analysis time',
                desc: 'PhD-level bottleneck slows decisions that need to happen today',
              },
              {
                stat: 'Missed',
                unit: 'yield opportunities',
                desc: 'By the time insights arrive, the growing window has passed',
              },
            ].map((card, i) => (
              <div key={i} className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm">
                <div className="text-3xl font-bold text-brand mb-1">{card.stat}</div>
                <div className="text-sm font-medium text-slate-500 mb-3">{card.unit}</div>
                <p className="text-slate-600 text-sm">{card.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="py-20 px-8">
        <div className="max-w-5xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-slate-900 mb-4">Upload. Analyze. Act.</h2>
          <p className="text-slate-500 mb-12 max-w-2xl mx-auto">AI interprets in seconds what takes specialists weeks.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: '01', title: 'Upload', desc: 'Drag and drop your hyperspectral drone imagery — any standard format.' },
              { step: '02', title: 'Analyze', desc: 'Our AI reads every spectral band and identifies health issues automatically.' },
              { step: '03', title: 'Act', desc: 'Get plain-English recommendations you can act on immediately.' },
            ].map((s, i) => (
              <div key={i} className="text-center">
                <div className="w-14 h-14 bg-brand/10 text-brand font-bold text-lg rounded-full flex items-center justify-center mx-auto mb-4">
                  {s.step}
                </div>
                <h3 className="font-semibold text-lg text-slate-900 mb-2">{s.title}</h3>
                <p className="text-slate-500 text-sm">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Traction Bar */}
      <section className="py-8 px-8 bg-slate-900 text-white">
        <div className="max-w-5xl mx-auto flex flex-wrap items-center justify-center gap-8 text-sm text-slate-300">
          <span>Built on NSF-Yale research</span>
          <span className="text-slate-600">|</span>
          <span>Validated with research institutions</span>
          <span className="text-slate-600">|</span>
          <span>Agriculture, geology, environmental science</span>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-6 px-8 text-center text-sm text-slate-400 border-t border-slate-100">
        SpectraLens &copy; 2025 — AI-powered hyperspectral analysis
      </footer>
    </div>
  )
}

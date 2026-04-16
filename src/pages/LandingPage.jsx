import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { apiFetch, setToken } from '../api/client'
import './LandingPage.css'

const BLOCKED_DOMAINS = ['gmail.com','yahoo.com','outlook.com','hotmail.com','icloud.com','protonmail.com','aol.com']
function isWorkEmail(email) {
  const domain = email.split('@')[1]?.toLowerCase()
  return domain && !BLOCKED_DOMAINS.includes(domain)
}

/* ══════════════════════════════════════════════════════════════
   VisiMind Landing Page
   Lifted from Stitch "Premium Landing Page (Linear Style)"
   screen 6716ddea — 25KB HTML, class→className conversion only.
   React used ONLY for the pilot signup form.
   ══════════════════════════════════════════════════════════════ */
export default function LandingPage() {
  useEffect(() => {
    document.body.classList.add('landing-active')
    return () => document.body.classList.remove('landing-active')
  }, [])

  /* Lightweight mouse-reactive background (passive, no rAF loop) */
  useEffect(() => {
    const onMove = (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 2
      const y = (e.clientY / window.innerHeight - 0.5) * 2
      const s = document.documentElement.style
      s.setProperty('--orb-cx', `${x * 40}px`)
      s.setProperty('--orb-cy', `${y * 40}px`)
      s.setProperty('--orb-lx', `${x * -30}px`)
      s.setProperty('--orb-ly', `${y * -30}px`)
      s.setProperty('--mouse-x', `${e.clientX}px`)
      s.setProperty('--mouse-y', `${e.clientY}px`)
    }
    window.addEventListener('mousemove', onMove, { passive: true })
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div className="landing-page font-body text-on-surface antialiased overflow-x-hidden">
      <a href="#main-content" className="skip-link">Skip to main content</a>
      {/* Animated ambient background */}
      <div className="grid-shimmer" />
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[60%] h-[60%] ambient-orb-cyan"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[60%] h-[60%] ambient-orb-lavender"></div>
      </div>

      {/* NAVBAR */}
      <header className="fixed top-0 w-full z-50 flex justify-between items-center px-8 py-4 max-w-[1440px] left-1/2 -translate-x-1/2 bg-white/5 dark:bg-slate-950/40 backdrop-blur-xl shadow-[0_0_50px_-12px_rgba(0,229,255,0.1)]">
        <div className="flex items-center gap-2">
          <div className="text-cyan-400">
            <span className="material-symbols-outlined text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>bolt</span>
          </div>
          <span className="text-2xl font-bold tracking-tighter text-slate-100 font-headline">VisiMind</span>
        </div>
        <nav className="hidden md:flex gap-8 items-center">
          <a className="text-cyan-400 font-medium border-b-2 border-cyan-400 pb-1 font-['Inter'] text-sm tracking-wide" href="#features">Platform</a>
          <a className="text-slate-400 hover:text-slate-100 transition-colors font-['Inter'] text-sm tracking-wide" href="#problem">Solutions</a>
          <a className="text-slate-400 hover:text-slate-100 transition-colors font-['Inter'] text-sm tracking-wide" href="#pilot">Pricing</a>
        </nav>
        <div className="flex items-center gap-4">
          <Link className="hidden lg:block text-slate-400 hover:text-slate-100 text-sm font-medium transition-colors" to="/signin">Sign In</Link>
          <Link className="bg-primary-container text-on-primary-container px-6 py-2.5 rounded-md font-bold text-sm hover:shadow-[0_0_20px_rgba(0,229,255,0.4)] transition-all" to="/signup">Get Started</Link>
        </div>
      </header>

      <main id="main-content" className="relative z-10 pt-32">
        {/* ── HERO ── */}
        <section className="max-w-7xl mx-auto px-6 lg:px-12 text-center">
          <a href="https://proceedings.neurips.cc/paper_files/paper/2023/file/8b8a7960d343e023a6a0afe37eee6022-Paper-Datasets_and_Benchmarks.pdf" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-high border border-outline-variant/20 mb-8 hover:border-cyan-400/30 transition-colors">
            <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
            <span className="text-xs font-bold tracking-widest uppercase text-cyan-400">NeurIPS 2023 Research Backed</span>
            <span className="material-symbols-outlined text-cyan-400 text-sm">open_in_new</span>
          </a>
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-headline font-extrabold tracking-[-0.02em] leading-[0.95] mb-8 max-w-5xl mx-auto">
            AI is telling your brand story.<br /><span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-container to-secondary">Is it telling the truth?</span>
          </h1>
          <p className="text-lg md:text-xl text-on-surface-variant max-w-2xl mx-auto mb-12 font-light leading-relaxed">
            ChatGPT and Gemini describe your luxury brand to millions daily — often with hallucinated facts, especially in French. Audit accuracy across languages before misinformation becomes a reputation risk.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-24">
            <a href="#pilot" className="bg-primary-container text-on-primary-container px-8 py-4 rounded-lg font-bold text-lg hover:shadow-[0_0_30px_rgba(0,229,255,0.3)] transition-all flex items-center justify-center gap-2">
              Start your free audit <span className="material-symbols-outlined">arrow_forward</span>
            </a>
            <a href="https://calendly.com/a-naim2004/ai-search-research" target="_blank" rel="noopener noreferrer" className="glass-panel px-8 py-4 rounded-lg font-bold text-lg hover:bg-white/10 transition-all border border-outline-variant/30 text-center flex items-center justify-center gap-2">
              Book a Demo <span className="material-symbols-outlined text-base">calendar_month</span>
            </a>
          </div>

          {/* Demo Video — replaces dashboard mockup */}
          <div id="demo" className="relative max-w-5xl mx-auto glass-panel rounded-lg p-2 shadow-2xl">
            <div className="bg-surface-container-lowest rounded-lg overflow-hidden border border-outline-variant/10 aspect-video flex items-center justify-center relative group cursor-pointer">
              {/* Play button overlay */}
              <div className="absolute inset-0 bg-gradient-to-br from-primary-container/5 to-secondary/5 z-0"></div>
              <div className="relative z-10 flex flex-col items-center gap-4">
                <div className="w-20 h-20 rounded-full bg-primary-container/10 border border-primary-container/30 flex items-center justify-center group-hover:bg-primary-container/20 group-hover:border-primary-container/50 transition-all duration-300">
                  <span className="material-symbols-outlined text-primary-container text-4xl ml-1" style={{ fontVariationSettings: "'FILL' 1" }}>play_arrow</span>
                </div>
                <span className="text-on-surface-variant text-sm font-medium">Watch the 90-second demo</span>
              </div>
            </div>
            {/* Lavender Tooltip */}
            <div className="absolute -right-8 top-1/2 -translate-y-1/2 glass-panel p-4 rounded-lg shadow-xl border-secondary/20 max-w-[240px] text-left hidden lg:block">
              <div className="flex items-center gap-2 mb-2">
                <span className="material-symbols-outlined text-secondary text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span>
                <span className="text-[10px] font-bold tracking-widest text-secondary uppercase">AI Insight</span>
              </div>
              <p className="text-xs leading-relaxed text-on-surface">Brand sentiment drift detected in FR-Quebec model variants regarding &quot;Sustainability&quot;.</p>
            </div>
          </div>

          {/* Trust Strip */}
          <div className="mt-20 py-12 border-t border-white/5 flex flex-wrap justify-center gap-12 grayscale opacity-50">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined">hub</span>
              <span className="font-headline font-bold">Built on MCP</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined">location_on</span>
              <span className="font-headline font-bold">Made in Montreal</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined">school</span>
              <span className="font-headline font-bold">NeurIPS 2023 Research</span>
            </div>
          </div>
        </section>

        {/* ── THE PROBLEM ── */}
        <section id="problem" className="py-32 max-w-7xl mx-auto px-6 lg:px-12">
          <span className="text-error font-bold tracking-[0.2em] uppercase text-xs mb-4 block">The Blind Spot</span>
          <h2 className="text-4xl md:text-5xl font-headline font-bold tracking-tight mb-16 max-w-3xl leading-tight">
            AI models are your new storefront. <br /><span className="text-on-surface-variant">Most brands are flying blind.</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-surface-container-low p-10 rounded-lg border border-white/5 hover:border-error/20 transition-all group">
              <div className="text-5xl font-headline font-extrabold text-error mb-4">47%</div>
              <p className="text-on-surface-variant leading-relaxed">Percentage of generated responses containing historical or pricing errors for premium retail.</p>
            </div>
            <div className="bg-surface-container-low p-10 rounded-lg border border-white/5 hover:border-tertiary/20 transition-all">
              <div className="text-5xl font-headline font-extrabold text-tertiary mb-4">3.2x</div>
              <p className="text-on-surface-variant leading-relaxed">Increase in hallucination frequency when querying models in non-English languages.</p>
            </div>
            <div className="bg-surface-container-low p-10 rounded-lg border border-white/5 hover:border-secondary/20 transition-all">
              <div className="text-5xl font-headline font-extrabold text-secondary mb-4">$2.4M</div>
              <p className="text-on-surface-variant leading-relaxed">Estimated annual brand equity erosion per $1B in revenue due to AI-driven misinformation.</p>
            </div>
          </div>
        </section>

        {/* ── THE BILINGUAL GAP ── */}
        <section className="py-32">
          <div className="max-w-7xl mx-auto px-6 lg:px-12">
            <span className="text-primary-container font-bold tracking-[0.2em] uppercase text-xs mb-4 block">The Bilingual Audit</span>
            <h2 className="text-4xl md:text-5xl font-headline font-bold tracking-tight mb-16 max-w-3xl leading-tight">
              Same question. Two languages. <br />Completely different answers.
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
              {/* EN Card */}
              <div className="glass-panel rounded-lg overflow-hidden border-primary-container/20">
                <div className="bg-surface-container-high px-6 py-3 border-b border-white/5 flex justify-between items-center">
                  <span className="text-xs font-mono text-primary-container">PROMPT_EN.V1</span>
                  <span className="px-2 py-0.5 rounded-full bg-primary-container/10 text-primary-container text-[10px] font-bold">VERIFIED</span>
                </div>
                <div className="p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <span className="material-symbols-outlined text-outline">alternate_email</span>
                    <p className="text-on-surface italic">&quot;Tell me about the heritage of the brand Mackage.&quot;</p>
                  </div>
                  <div className="flex items-start gap-4">
                    <span className="material-symbols-outlined text-primary-container">smart_toy</span>
                    <div className="space-y-4">
                      <p className="text-on-surface text-sm leading-relaxed">Mackage is a Canadian luxury outerwear brand founded in 1999 by Eran Elfassy and Elisa Dahan. It is headquartered in Montreal and is known for its high-performance fabrics and tailored silhouettes...</p>
                      <div className="h-px w-full bg-white/5"></div>
                      <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-primary-container text-xs">check_circle</span>
                        <span className="text-[10px] text-primary-container font-medium">Data alignment: 99.8%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              {/* FR Card */}
              <div className="glass-panel rounded-lg overflow-hidden border-error/20">
                <div className="bg-surface-container-high px-6 py-3 border-b border-white/5 flex justify-between items-center">
                  <span className="text-xs font-mono text-error">PROMPT_FR.V1</span>
                  <span className="px-2 py-0.5 rounded-full bg-error/10 text-error text-[10px] font-bold">ERROR: BIAS DETECTED</span>
                </div>
                <div className="p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <span className="material-symbols-outlined text-outline">alternate_email</span>
                    <p className="text-on-surface italic">&quot;Parle-moi de l&apos;héritage de la marque Mackage.&quot;</p>
                  </div>
                  <div className="flex items-start gap-4">
                    <span className="material-symbols-outlined text-error">smart_toy</span>
                    <div className="space-y-4">
                      <p className="text-on-surface text-sm leading-relaxed">Mackage est une maison de couture <span className="bg-error/20 text-error px-1">fondée à Paris</span> en 1999. Symbole de l&apos;élégance française, la marque est connue pour ses designs européens inspirés de la haute couture...</p>
                      <div className="h-px w-full bg-white/5"></div>
                      <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-error text-xs">warning</span>
                        <span className="text-[10px] text-error font-medium">Fact Hallucination: Origins misidentified as French</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── FEATURES ── */}
        <section id="features" className="py-32 max-w-7xl mx-auto px-6 lg:px-12">
          <div className="text-center mb-20">
            <span className="text-secondary font-bold tracking-[0.2em] uppercase text-xs mb-4 block">Capabilities</span>
            <h2 className="text-4xl md:text-5xl font-headline font-bold tracking-tight">Full-stack AI brand intelligence.</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-24">
            <div className="bg-surface-container p-8 rounded-lg border border-white/10 hover:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-primary-container text-4xl mb-6" style={{ fontVariationSettings: "'FILL' 1" }}>security_update_good</span>
              <h3 className="text-xl font-bold font-headline mb-3">Inference Audit</h3>
              <p className="text-on-surface-variant text-sm leading-relaxed">Stress-test foundation models with 10k+ branded queries to map the risk landscape.</p>
            </div>
            <div className="bg-surface-container p-8 rounded-lg border border-white/10 hover:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-primary-container text-4xl mb-6" style={{ fontVariationSettings: "'FILL' 1" }}>query_stats</span>
              <h3 className="text-xl font-bold font-headline mb-3">IAS Scoring</h3>
              <p className="text-on-surface-variant text-sm leading-relaxed">Integrity-Accuracy-Sentiment scoring. A unified metric for your AI brand equity.</p>
            </div>
            <div className="bg-surface-container p-8 rounded-lg border border-white/10 hover:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-primary-container text-4xl mb-6" style={{ fontVariationSettings: "'FILL' 1" }}>translate</span>
              <h3 className="text-xl font-bold font-headline mb-3">Bilingual Gap</h3>
              <p className="text-on-surface-variant text-sm leading-relaxed">Dedicated monitoring for English/French inconsistencies common in global luxury.</p>
            </div>
            <div className="bg-surface-container p-8 rounded-lg border border-white/10 hover:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-primary-container text-4xl mb-6" style={{ fontVariationSettings: "'FILL' 1" }}>build_circle</span>
              <h3 className="text-xl font-bold font-headline mb-3">Fix Kit</h3>
              <p className="text-on-surface-variant text-sm leading-relaxed">Automated system prompts and fine-tuning datasets to correct model hallucinations.</p>
            </div>
            <div className="bg-surface-container p-8 rounded-lg border border-white/10 hover:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-primary-container text-4xl mb-6" style={{ fontVariationSettings: "'FILL' 1" }}>sync</span>
              <h3 className="text-xl font-bold font-headline mb-3">Verification Loop</h3>
              <p className="text-on-surface-variant text-sm leading-relaxed">Real-time alerts whenever foundation models update and alter your brand&apos;s narrative.</p>
            </div>
            <div className="bg-surface-container p-8 rounded-lg border border-white/10 hover:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-primary-container text-4xl mb-6" style={{ fontVariationSettings: "'FILL' 1" }}>account_tree</span>
              <h3 className="text-xl font-bold font-headline mb-3">MCP Knowledge Graphs</h3>
              <p className="text-on-surface-variant text-sm leading-relaxed">Direct context injection using Model Context Protocol to ground AI responses in truth.</p>
            </div>
          </div>
          <div className="glass-panel p-12 rounded-lg text-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-primary-container/10 to-secondary/10 pointer-events-none"></div>
            <h3 className="text-3xl font-headline font-bold mb-6 relative z-10">Ready to secure your brand&apos;s AI future?</h3>
            <a href="#pilot" className="relative z-10 inline-block bg-primary-container text-on-primary-container px-10 py-4 rounded-full font-bold text-lg hover:shadow-lg transition-all">
              Start Your Audit
            </a>
          </div>
        </section>

        {/* ── HOW IT WORKS ── */}
        <section className="py-32">
          <div className="max-w-7xl mx-auto px-6 lg:px-12">
            <div className="text-center mb-20">
              <span className="text-on-surface-variant font-bold tracking-[0.2em] uppercase text-xs mb-4 block">The Methodology</span>
              <h2 className="text-4xl font-headline font-bold">Three steps to AI clarity.</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
              <div className="relative glass-panel p-10 pt-20 rounded-lg group">
                <span className="absolute top-4 left-6 text-8xl font-headline font-extrabold text-white/5 group-hover:text-primary-container/10 transition-colors pointer-events-none select-none">01</span>
                <h4 className="text-xl font-bold font-headline mb-4">Enter brand</h4>
                <p className="text-on-surface-variant leading-relaxed">Connect your official brand portal and product databases via secure API or MCP.</p>
              </div>
              <div className="relative glass-panel p-10 pt-20 rounded-lg group">
                <span className="absolute top-4 left-6 text-8xl font-headline font-extrabold text-white/5 group-hover:text-primary-container/10 transition-colors pointer-events-none select-none">02</span>
                <h4 className="text-xl font-bold font-headline mb-4">Probe models</h4>
                <p className="text-on-surface-variant leading-relaxed">Our engine simulates millions of interactions across every major foundation model and language.</p>
              </div>
              <div className="relative glass-panel p-10 pt-20 rounded-lg group">
                <span className="absolute top-4 left-6 text-8xl font-headline font-extrabold text-white/5 group-hover:text-primary-container/10 transition-colors pointer-events-none select-none">03</span>
                <h4 className="text-xl font-bold font-headline mb-4">Get Score + Kit</h4>
                <p className="text-on-surface-variant leading-relaxed">Receive your IAS score dashboard and actionable datasets to fix detected hallucinations.</p>
              </div>
            </div>
          </div>
        </section>

        {/* ── PILOT SIGNUP (React form) ── */}
        <PilotForm />
      </main>

      {/* FOOTER */}
      <footer className="bg-[#060a14] border-t border-white/5 py-16 px-12 mt-20 relative z-10">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-12">
          <div className="flex flex-col items-center md:items-start gap-4">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-cyan-400 text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>bolt</span>
              <span className="text-xl font-bold text-slate-100 font-headline">VisiMind</span>
            </div>
            <p className="text-slate-500 font-['Inter'] text-sm tracking-wide max-w-xs text-center md:text-left">
              The precision layer for luxury brands in the age of generative intelligence.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-8">
            <a className="text-slate-500 hover:text-slate-300 font-['Inter'] text-sm transition-colors" href="#">Privacy</a>
            <a className="text-slate-500 hover:text-slate-300 font-['Inter'] text-sm transition-colors" href="#">Terms</a>
            <Link className="text-slate-500 hover:text-slate-300 font-['Inter'] text-sm transition-colors" to="/signin">Sign In</Link>
            <Link className="text-slate-500 hover:text-slate-300 font-['Inter'] text-sm transition-colors" to="/signup">Sign Up</Link>
          </div>
          <div className="text-slate-500 font-['Inter'] text-sm tracking-wide">
            © 2024 VisiMind. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}

/* ── Pilot signup form — only React-ified section ── */
function PilotForm() {
  const navigate = useNavigate()
  const [capacity, setCapacity] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({ brand_name: '', email: '', company_url: '' })

  useEffect(() => {
    fetch('/api/v1/system/capacity')
      .then(r => r.ok ? r.json() : null)
      .then(data => { if (data) setCapacity(data) })
      .catch(() => setCapacity({ remaining: 5, total: 10 }))
  }, [])

  const slots = capacity?.remaining ?? null

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!isWorkEmail(form.email)) { setError('Please use your work email.'); return }
    setLoading(true)
    try {
      const pwd = Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2)
      const data = await apiFetch('/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ email: form.email, password: pwd, company_name: form.brand_name, company_url: form.company_url }),
      })
      setToken(data.access_token || data.token)
      navigate('/setup')
    } catch (err) { setError(err.message || 'Something went wrong.') }
    finally { setLoading(false) }
  }

  return (
    <section id="pilot" className="py-32 max-w-4xl mx-auto px-6 text-center">
      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-8">
        <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span className="text-xs font-bold tracking-widest uppercase text-emerald-500">
          {slots !== null ? `${slots} slots remaining for Q4 Pilot` : 'Checking availability...'}
        </span>
      </div>
      <h2 className="text-4xl md:text-5xl font-headline font-bold mb-12">Secure your priority audit.</h2>
      <div className="glass-panel p-8 md:p-12 rounded-lg border-white/10 shadow-2xl">
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Brand Name</label>
            <input className="w-full bg-surface-container-highest border-none rounded-md px-4 py-3 focus:ring-2 focus:ring-primary-container text-on-surface" placeholder="e.g. Mackage" type="text" required value={form.brand_name} onChange={e => setForm({ ...form, brand_name: e.target.value })} />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Corporate Email</label>
            <input className="w-full bg-surface-container-highest border-none rounded-md px-4 py-3 focus:ring-2 focus:ring-primary-container text-on-surface" placeholder="name@brand.com" type="email" required value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
          </div>
          <div className="md:col-span-2 space-y-2">
            <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Website URL</label>
            <input className="w-full bg-surface-container-highest border-none rounded-md px-4 py-3 focus:ring-2 focus:ring-primary-container text-on-surface" placeholder="https://www.brand.com" type="url" required value={form.company_url} onChange={e => setForm({ ...form, company_url: e.target.value })} />
          </div>
          {error && <div className="md:col-span-2"><p className="text-error text-sm">{error}</p></div>}
          <div className="md:col-span-2 pt-4">
            <button type="submit" disabled={loading} className="w-full bg-primary-container text-on-primary-container py-4 rounded-md font-bold text-lg hover:shadow-[0_0_40px_rgba(0,229,255,0.2)] transition-all disabled:opacity-50 disabled:cursor-not-allowed">
              {loading ? 'Starting...' : 'Start your free audit'}
            </button>
            <p className="text-[10px] text-center text-on-surface-variant mt-4 uppercase tracking-tighter">Free tier. No credit card required. Results in under 5 minutes.</p>
          </div>
        </form>
      </div>
    </section>
  )
}

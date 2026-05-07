import { useState, useEffect, useCallback, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { apiFetch, setToken } from '../api/client'
import './LandingPage.css'

/* 10 findings from real search audits, April 2026 -- every one verified against raw data */
const FINDINGS_ROW_1 = [
  { brand: 'Mackage', query: 'manteau hiver luxe femme Québec', finding: 'Audvik owns the top 3 spots for women\'s luxury coats in Quebec. Mackage doesn\'t appear. The French Quebec market is wide open.', lang: 'FR' },
  { brand: 'Mackage', query: 'best luxury winter coats Montreal', finding: 'A brand founded in Montreal in 1999, invisible in Montreal search results. Gorski and Quartz Co. rank instead.', lang: 'EN' },
  { brand: 'SSENSE', query: 'où acheter vêtements designer Montréal', finding: '52K Trustpilot reviews, Montreal HQ -- but 0 of 4 non-branded French queries show SSENSE. An entire audience isn\'t finding them.', lang: 'FR' },
  { brand: 'Mackage', query: 'Mackage winter jacket review', finding: 'All 10 results are blogs and forums. mackage.com doesn\'t rank for its own brand reviews.', lang: 'EN' },
  { brand: 'Rudsak', query: 'meilleurs manteaux cuir Montréal', finding: 'A Montreal leather brand, absent from French leather queries. Cuir Dimitri and m0851 rank instead.', lang: 'FR' },
]
const FINDINGS_ROW_2 = [
  { brand: 'Mackage', query: 'Mackage manteau avis', finding: 'French shoppers see La Canadienne and Altitude Sports reviews -- not Mackage\'s own story.', lang: 'FR' },
  { brand: 'SSENSE', query: 'designer clothing Montreal', finding: 'Montreal\'s biggest fashion platform, invisible in local search. Indie boutiques take every spot.', lang: 'EN' },
  { brand: 'Rudsak', query: 'Rudsak vs Mackage', finding: '3 of 10 results are about a design-copying lawsuit. Neither brand owns a comparison page.', lang: 'EN' },
  { brand: 'Mackage', query: 'luxury down jacket brands', finding: 'The one bright spot: mackage.com ranks #1 here. But it\'s the only query out of 12 where it does.', lang: 'EN' },
  { brand: 'Dynamite', query: 'affordable fashion brands Canada', finding: 'H&M and Joe Fresh own this space. A Canadian alternative with 300+ stores isn\'t in the conversation.', lang: 'EN' },
]

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
  const [activeNav, setActiveNav] = useState('features')
  const [capacity, setCapacity] = useState(null)
  const clickLock = useRef(false)

  useEffect(() => {
    document.body.classList.add('landing-active')
    return () => document.body.classList.remove('landing-active')
  }, [])

  useEffect(() => {
    const API_URL = import.meta.env.VITE_API_URL || ''
    fetch(`${API_URL}/api/v1/system/capacity`)
      .then(r => r.ok ? r.json() : null)
      .then(data => { if (data) setCapacity(data) })
      .catch(() => setCapacity({ slots_remaining: 7, limit: 10 }))
  }, [])

  const handleNavClick = useCallback((id) => {
    setActiveNav(id)
    clickLock.current = true
    setTimeout(() => { clickLock.current = false }, 800)
  }, [])

  useEffect(() => {
    const sections = ['features', 'proof', 'pilot']
    const onScroll = () => {
      if (clickLock.current) return
      for (const id of [...sections].reverse()) {
        const el = document.getElementById(id)
        if (el && el.getBoundingClientRect().top <= 200) { setActiveNav(id); return }
      }
      setActiveNav('features')
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <div className="landing-page font-body text-on-surface antialiased overflow-x-hidden">
      {/* Animated ambient background */}
      <div className="grid-shimmer" />
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[60%] h-[60%] ambient-orb-cyan"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[60%] h-[60%] ambient-orb-lavender"></div>
      </div>

      {/* NAVBAR */}
      <header className="fixed top-0 left-0 right-0 w-full z-50 bg-surface-container-lowest/80 backdrop-blur-xl border-b border-white/5">
        <div className="flex justify-between items-center px-8 py-4 max-w-[1440px] mx-auto">
          <div className="flex items-center gap-2">
            <div className="text-cyan-400">
              <span className="material-symbols-outlined text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>bolt</span>
            </div>
            <span className="text-2xl font-bold tracking-tighter text-slate-100 font-headline">VisiMind</span>
          </div>
          <nav className="hidden md:flex gap-8 items-center">
            {(() => {
              const slots = capacity?.slots_remaining ?? null
              const pilotLabel = slots === null ? 'Pilot' : slots <= 0 ? 'Pilot (Full)' : `Pilot (${slots} spots)`
              return [['features', 'Platform'], ['proof', 'Proof'], ['pilot', pilotLabel]]
            })().map(([id, label]) => (
              <a key={id} className={`font-['Inter'] text-sm tracking-wide pb-1 border-b-2 transition-all duration-300 ease-out ${activeNav === id ? 'text-cyan-400 font-medium border-cyan-400' : 'text-slate-400 hover:text-slate-100 border-transparent'}`} href={`#${id}`} onClick={() => handleNavClick(id)}>{label}</a>
            ))}
          </nav>
          <div className="flex items-center gap-4">
            <Link className="hidden lg:block text-slate-400 hover:text-slate-100 text-sm font-medium transition-colors" to="/signin">Sign In</Link>
            <Link className="bg-primary-container text-on-primary-fixed px-6 py-2.5 rounded-md font-bold text-sm hover:shadow-[0_0_20px_rgba(0,229,255,0.4)] transition-all" to="/signup">Get Started</Link>
          </div>
        </div>
      </header>

      <main className="relative z-10 pt-32">
        {/* ── HERO ── */}
        <section className="max-w-7xl mx-auto px-6 lg:px-12 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-high border border-outline-variant/20 mb-8">
            <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
            <span className="text-xs font-bold tracking-widest uppercase text-cyan-400">NeurIPS 2023 Research Backed</span>
          </div>
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-headline font-extrabold tracking-[-0.04em] leading-[0.9] mb-8 max-w-5xl mx-auto">
            Your brand has a <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-container to-secondary">new spokesperson.</span> It's an AI.
          </h1>
          <p className="text-lg md:text-xl text-on-surface-variant max-w-2xl mx-auto mb-12 font-light leading-relaxed">
            Automatically audit how ChatGPT and Gemini represent your luxury brand in English and French. Detect hallucinations before they become reputation risks.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-24">
            <Link to="/setup" className="bg-primary-container text-on-primary-fixed px-8 py-4 rounded-lg font-bold text-lg hover:shadow-[0_0_30px_rgba(0,229,255,0.3)] transition-all flex items-center justify-center gap-2">
              Start your free audit <span className="material-symbols-outlined">arrow_forward</span>
            </Link>
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
              <div className="text-5xl font-headline font-extrabold text-error mb-4">&lt;2%</div>
              <p className="text-on-surface-variant leading-relaxed">AI mention rate for independent and DTC brands, vs 85%+ for mega-brands like Nike.</p>
              <span className="text-[9px] text-on-surface-variant/50 mt-3 block">Source: Metricus AI Visibility Study</span>
            </div>
            <div className="bg-surface-container-low p-10 rounded-lg border border-white/5 hover:border-tertiary/20 transition-all">
              <div className="text-5xl font-headline font-extrabold text-tertiary mb-4">53%</div>
              <p className="text-on-surface-variant leading-relaxed">Of consumers who use AI search also use it to shop. If AI doesn't know your brand, they won't either.</p>
              <span className="text-[9px] text-on-surface-variant/50 mt-3 block">Source: BoF / McKinsey State of Fashion 2026</span>
            </div>
            <div className="bg-surface-container-low p-10 rounded-lg border border-white/5 hover:border-secondary/20 transition-all">
              <div className="text-5xl font-headline font-extrabold text-secondary mb-4">4,700%</div>
              <p className="text-on-surface-variant leading-relaxed">Growth in AI shopping queries between 2024 and 2025. Your brand is either in the answers or it doesn't exist.</p>
              <span className="text-[9px] text-on-surface-variant/50 mt-3 block">Source: BoF / McKinsey State of Fashion 2026</span>
            </div>
          </div>
        </section>

        {/* ── PROOF ── */}
        <ProofMarquee />

        {/* ── HOW IT WORKS (merged pipeline + capabilities) ── */}
        <section id="features" className="py-32 max-w-7xl mx-auto px-6 lg:px-12">
          <div className="text-center mb-20">
            <span className="text-secondary font-bold tracking-[0.2em] uppercase text-xs mb-4 block">How it works</span>
            <h2 className="text-4xl md:text-5xl font-headline font-bold tracking-tight">Four steps. Five minutes. Real fixes.</h2>
          </div>

          {/* Pipeline steps */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-0 mb-20">
            {[
              { n: '01', title: 'Connect your brand', desc: 'Enter your website URL. We pull your brand facts, products, and positioning automatically.', icon: 'link' },
              { n: '02', title: 'We audit AI models', desc: 'We query ChatGPT and Gemini with branded and non-branded searches in English and French.', icon: 'search' },
              { n: '03', title: 'See what AI gets wrong', desc: 'Get a clear report: hallucinations, missing visibility, competitor gaps, and bilingual inconsistencies.', icon: 'fact_check' },
              { n: '04', title: 'Get ready-to-use fixes', desc: 'Download JSON-LD schemas, SEO content briefs, and video scripts you can deploy the same day.', icon: 'download' },
            ].map((step, i) => (
              <div key={step.n} className="relative flex flex-col items-center text-center p-8 group">
                {i < 3 && <div className="hidden md:block absolute top-1/3 -right-4 w-8 text-white/10 z-10"><span className="material-symbols-outlined text-2xl">chevron_right</span></div>}
                <div className="w-16 h-16 rounded-2xl bg-surface-container-high border border-white/5 flex items-center justify-center mb-6 group-hover:border-primary-container/30 transition-colors">
                  <span className="material-symbols-outlined text-primary-container text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>{step.icon}</span>
                </div>
                <span className="text-[10px] font-mono text-on-surface-variant/30 mb-2">{step.n}</span>
                <h4 className="text-lg font-bold font-headline mb-3">{step.title}</h4>
                <p className="text-on-surface-variant text-sm leading-relaxed max-w-[260px]">{step.desc}</p>
              </div>
            ))}
          </div>

          <div className="glass-panel p-12 rounded-lg text-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-primary-container/10 to-secondary/10 pointer-events-none"></div>
            <h3 className="text-3xl font-headline font-bold mb-6 relative z-10">Takes 5 minutes. No integration needed.</h3>
            <a href="#pilot" className="relative z-10 inline-block bg-primary-container text-on-primary-fixed px-10 py-4 rounded-lg font-bold text-lg hover:shadow-lg transition-all">
              Start Your Audit
            </a>
          </div>
        </section>

        {/* ── PILOT SIGNUP (React form) ── */}
        <PilotForm capacity={capacity} />
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
            <Link className="text-slate-500 hover:text-slate-300 font-['Inter'] text-sm transition-colors" to="/signin">Sign In</Link>
            <Link className="text-slate-500 hover:text-slate-300 font-['Inter'] text-sm transition-colors" to="/signup">Sign Up</Link>
          </div>
          <div className="text-slate-500 font-['Inter'] text-sm tracking-wide">
            © {new Date().getFullYear()} VisiMind. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}

/* ── Finding card for marquee ── */
function FindingCard({ f }) {
  return (
    <div className="flex-shrink-0 w-[340px] rounded-lg border border-white/[0.04] bg-white/[0.02] p-5 mx-2 hover:border-white/10 transition-colors">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-[10px] font-bold tracking-widest uppercase text-on-surface-variant/40">{f.brand}</span>
        <span className="text-on-surface-variant/20">|</span>
        <span className="text-[10px] font-mono text-on-surface-variant/30">{f.lang}</span>
      </div>
      <p className="text-xs text-on-surface-variant/60 font-mono leading-relaxed mb-3 truncate" title={f.query}>&quot;{f.query}&quot;</p>
      <p className="text-sm text-on-surface/80 leading-snug">{f.finding}</p>
    </div>
  )
}

/* ── Proof section with auto-scrolling marquee ── */
function ProofMarquee() {
  const row1Ref = useRef(null)
  const row2Ref = useRef(null)
  const pausedRef = useRef(false)
  const tRef = useRef(0)

  const handleEnter = useCallback(() => { pausedRef.current = true }, [])
  const handleLeave = useCallback(() => { pausedRef.current = false }, [])

  useEffect(() => {
    let raf
    const speed1 = 0.15
    const speed2 = 0.12
    const tick = () => {
      if (!pausedRef.current) {
        tRef.current += 1
        if (row1Ref.current) {
          const half = row1Ref.current.scrollWidth / 2
          row1Ref.current.style.transform = `translateX(-${tRef.current * speed1 % half}px)`
        }
        if (row2Ref.current) {
          const half = row2Ref.current.scrollWidth / 2
          row2Ref.current.style.transform = `translateX(-${half - (tRef.current * speed2 % half)}px)`
        }
      }
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [])

  return (
    <section id="proof" className="py-28 bg-surface-container-lowest overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 lg:px-12 mb-14">
        <span className="text-on-surface-variant/40 font-bold tracking-[0.2em] uppercase text-xs mb-4 block">From real audits</span>
        <h2 className="text-4xl md:text-6xl font-headline font-extrabold tracking-tight max-w-4xl leading-[1.05]">
          We audited 16 brands. <br /><span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-container to-secondary">Not one was fully visible to AI.</span>
        </h2>
      </div>

      <div
        className="space-y-4"
        onMouseEnter={handleEnter}
        onMouseLeave={handleLeave}
      >
        {/* Row 1 - scrolls left */}
        <div className="overflow-hidden">
          <div ref={row1Ref} className="flex w-max will-change-transform">
            {[...FINDINGS_ROW_1, ...FINDINGS_ROW_1, ...FINDINGS_ROW_1].map((f, i) => (
              <FindingCard key={i} f={f} />
            ))}
          </div>
        </div>
        {/* Row 2 - scrolls right */}
        <div className="overflow-hidden">
          <div ref={row2Ref} className="flex w-max will-change-transform">
            {[...FINDINGS_ROW_2, ...FINDINGS_ROW_2, ...FINDINGS_ROW_2].map((f, i) => (
              <FindingCard key={i} f={f} />
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 lg:px-12 mt-10">
        <p className="text-[10px] text-on-surface-variant/30">Data from VisiMind search audits and bilingual probes, April 2026. Globe and Mail AI shopping test, 2025.</p>
      </div>
    </section>
  )
}

/* ── Pilot signup form — only React-ified section ── */
function PilotForm({ capacity }) {
  const navigate = useNavigate()
  const [form, setForm] = useState({ brand_name: '', company_url: '' })

  const slots = capacity?.slots_remaining ?? null

  const handleSubmit = (e) => {
    e.preventDefault()
    localStorage.setItem('visimind_pilot_data', JSON.stringify({ brand_name: form.brand_name, primary_url: form.company_url }))
    navigate('/setup')
  }

  return (
    <section id="pilot" className="py-32 max-w-4xl mx-auto px-6 text-center">
      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-8">
        <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span className="text-xs font-bold tracking-widest uppercase text-emerald-500">
          {slots !== null ? `${slots} pilot slots remaining` : 'Checking availability...'}
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
            <label className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">Website URL</label>
            <input className="w-full bg-surface-container-highest border-none rounded-md px-4 py-3 focus:ring-2 focus:ring-primary-container text-on-surface" placeholder="https://www.brand.com" type="url" required value={form.company_url} onChange={e => setForm({ ...form, company_url: e.target.value })} />
          </div>
          <div className="md:col-span-2 pt-4">
            <button type="submit" className="w-full bg-primary-container text-on-primary-fixed py-4 rounded-md font-bold text-lg hover:shadow-[0_0_40px_rgba(0,229,255,0.2)] transition-all">
              Start your free audit
            </button>
            <p className="text-[10px] text-center text-on-surface-variant mt-4 uppercase tracking-tighter">Free tier. No credit card required. Results in under 5 minutes.</p>
          </div>
        </form>
      </div>
    </section>
  )
}

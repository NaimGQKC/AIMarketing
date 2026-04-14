import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Zap,
  Play,
  ArrowRight,
  Search,
  Languages,
  BarChart3,
  Shield,
  Globe,
  MapPin,
  ChevronDown,
} from 'lucide-react'
import { apiFetch, setToken } from '../api/client'

const BLOCKED_DOMAINS = [
  'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
  'icloud.com', 'protonmail.com', 'aol.com',
]

function isWorkEmail(email) {
  const domain = email.split('@')[1]?.toLowerCase()
  return domain && !BLOCKED_DOMAINS.includes(domain)
}

/* ── Animation variants ── */
const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.15, duration: 0.6, ease: [0.16, 1, 0.3, 1] },
  }),
}

const stagger = {
  visible: { transition: { staggerChildren: 0.12 } },
}

/* ── Navbar ── */
function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-[#060a14]/80 backdrop-blur-xl border-b border-white/[0.06]">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-[#f0f2f8] font-['Outfit'] font-bold text-lg">
          <Zap size={22} className="text-[#00e5ff]" />
          VisiMind
        </Link>
        <div className="flex items-center gap-6">
          <Link to="/signin" className="text-[#8b95b0] text-sm hover:text-[#00e5ff] transition-colors">
            Sign In
          </Link>
          <Link
            to="/signup"
            className="text-sm px-4 py-2 rounded-lg bg-white/[0.05] border border-white/[0.08] text-[#f0f2f8] hover:bg-white/[0.08] transition-colors"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </nav>
  )
}

/* ── Hero Section ── */
function Hero() {
  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden px-6 pt-16">
      {/* Grid background */}
      <div
        className="absolute inset-0 opacity-[0.04]"
        style={{
          backgroundImage:
            'linear-gradient(rgba(0,229,255,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(0,229,255,0.3) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
        }}
      />
      {/* Gradient orbs */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-[#00e5ff]/[0.05] rounded-full blur-[120px]" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-[#9b8aff]/[0.04] rounded-full blur-[100px]" />

      <motion.div
        className="relative z-10 max-w-4xl mx-auto text-center"
        initial="hidden"
        animate="visible"
        variants={stagger}
      >
        <motion.div variants={fadeUp} custom={0} className="mb-6">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#00e5ff]/10 border border-[#00e5ff]/20 text-[#00e5ff] text-sm font-medium">
            <Shield size={14} />
            AI Brand Auditing for Quebec &amp; France
          </span>
        </motion.div>

        <motion.h1
          variants={fadeUp}
          custom={1}
          className="font-['Outfit'] text-4xl sm:text-5xl md:text-6xl font-bold text-[#f0f2f8] leading-[1.1] mb-6"
        >
          AI agents are talking about your brand.{' '}
          <span className="text-[#00e5ff]">Are they getting it right?</span>
        </motion.h1>

        <motion.p
          variants={fadeUp}
          custom={2}
          className="text-lg sm:text-xl text-[#8b95b0] max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          VisiMind audits how ChatGPT, Gemini, and Google AI Mode represent your
          brand in French -- and gives you the tools to fix it.
        </motion.p>

        <motion.div variants={fadeUp} custom={3} className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => scrollTo('audit-form')}
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl text-lg shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.35)] hover:-translate-y-0.5 transition-all duration-250 cursor-pointer"
          >
            Audit Your Brand
            <ArrowRight size={20} />
          </button>
          <button
            onClick={() => scrollTo('demo')}
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white/[0.03] text-[#f0f2f8] font-semibold rounded-xl text-lg border border-white/[0.06] hover:bg-white/[0.06] hover:border-white/[0.12] transition-all duration-250 cursor-pointer"
          >
            <Play size={18} />
            Watch the Demo
          </button>
        </motion.div>

        <motion.div variants={fadeUp} custom={4} className="mt-16">
          <ChevronDown size={24} className="mx-auto text-[#5a6480] animate-bounce" />
        </motion.div>
      </motion.div>
    </section>
  )
}

/* ── Demo Video Section ── */
function DemoVideo() {
  return (
    <section id="demo" className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          variants={stagger}
          className="text-center"
        >
          <motion.h2
            variants={fadeUp}
            className="font-['Outfit'] text-3xl sm:text-4xl font-bold text-[#f0f2f8] mb-4"
          >
            See VisiMind in Action
          </motion.h2>
          <motion.p variants={fadeUp} custom={1} className="text-[#8b95b0] mb-10">
            90-second walkthrough of a real brand audit
          </motion.p>
          <motion.div
            variants={fadeUp}
            custom={2}
            className="relative aspect-video rounded-2xl bg-[#0f1424] border border-white/[0.06] overflow-hidden flex items-center justify-center cursor-pointer group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-[#00e5ff]/[0.03] to-[#9b8aff]/[0.03]" />
            <div className="relative z-10 w-20 h-20 rounded-full bg-[#00e5ff]/10 border border-[#00e5ff]/30 flex items-center justify-center group-hover:bg-[#00e5ff]/20 group-hover:border-[#00e5ff]/50 transition-all duration-300">
              <Play size={32} className="text-[#00e5ff] ml-1" />
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}

/* ── Gated Form Section ── */
function GatedForm() {
  const navigate = useNavigate()
  const [capacity, setCapacity] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({ brand_name: '', email: '', company_url: '' })
  const [waitlistEmail, setWaitlistEmail] = useState('')
  const [waitlistSubmitted, setWaitlistSubmitted] = useState(false)

  useEffect(() => {
    fetch('/api/v1/system/capacity')
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (data) setCapacity(data)
      })
      .catch(() => {
        setCapacity({ remaining: 5, total: 10 })
      })
  }, [])

  const slotsRemaining = capacity?.remaining ?? null
  const slotsTotal = capacity?.total ?? 10

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!isWorkEmail(form.email)) {
      setError('Please use your work email address.')
      return
    }

    setLoading(true)
    try {
      const randomPwd =
        Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2)

      const data = await apiFetch('/auth/signup', {
        method: 'POST',
        body: JSON.stringify({
          email: form.email,
          password: randomPwd,
          company_name: form.brand_name,
          company_url: form.company_url,
        }),
      })
      setToken(data.access_token || data.token)
      navigate('/setup')
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleWaitlist = async (e) => {
    e.preventDefault()
    try {
      await apiFetch('/system/waitlist', {
        method: 'POST',
        body: JSON.stringify({ email: waitlistEmail }),
      })
    } catch {
      // silently accept
    }
    setWaitlistSubmitted(true)
  }

  return (
    <section id="audit-form" className="py-24 px-6 bg-[#0a0e1a]">
      <div className="max-w-xl mx-auto">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-80px' }}
          variants={stagger}
        >
          <motion.div variants={fadeUp} className="text-center mb-8">
            <h2 className="font-['Outfit'] text-3xl sm:text-4xl font-bold text-[#f0f2f8] mb-3">
              VisiMind Pilot Program
            </h2>
            <p className="text-[#8b95b0]">
              Currently limiting access to ensure processing quality.
            </p>
          </motion.div>

          {/* Slot counter */}
          <motion.div variants={fadeUp} custom={1} className="text-center mb-8">
            <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-white/[0.03] border border-white/[0.06]">
              <div
                className={`w-2.5 h-2.5 rounded-full ${
                  slotsRemaining > 0 ? 'bg-[#34d399] animate-pulse' : 'bg-[#ff4c6a]'
                }`}
              />
              <span className="text-[#f0f2f8] font-medium">
                {slotsRemaining !== null ? (
                  <>
                    <span className="text-[#00e5ff] font-bold">{slotsRemaining}</span> / {slotsTotal}{' '}
                    Daily Audit Slots Remaining
                  </>
                ) : (
                  'Checking availability...'
                )}
              </span>
            </div>
          </motion.div>

          {/* Form card */}
          <motion.div
            variants={fadeUp}
            custom={2}
            className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-8"
          >
            {slotsRemaining === 0 ? (
              waitlistSubmitted ? (
                <div className="text-center py-6">
                  <div className="w-14 h-14 rounded-full bg-[#34d399]/10 flex items-center justify-center mx-auto mb-4">
                    <Shield size={24} className="text-[#34d399]" />
                  </div>
                  <h3 className="font-['Outfit'] text-xl font-semibold text-[#f0f2f8] mb-2">
                    You're on the list!
                  </h3>
                  <p className="text-[#8b95b0]">We'll notify you when a slot opens up.</p>
                </div>
              ) : (
                <form onSubmit={handleWaitlist} className="space-y-4">
                  <p className="text-[#8b95b0] text-center mb-4">
                    All slots for today are taken. Join the waitlist to get notified.
                  </p>
                  <input
                    type="email"
                    required
                    placeholder="Work email"
                    value={waitlistEmail}
                    onChange={(e) => setWaitlistEmail(e.target.value)}
                    className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg px-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                  />
                  <button
                    type="submit"
                    className="w-full py-3 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.35)] hover:-translate-y-0.5 transition-all duration-250 cursor-pointer"
                  >
                    Join the Waitlist
                  </button>
                </form>
              )
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <input
                    type="text"
                    required
                    placeholder="Brand Name"
                    value={form.brand_name}
                    onChange={(e) => setForm({ ...form, brand_name: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg px-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                  />
                </div>
                <div>
                  <input
                    type="email"
                    required
                    placeholder="Work Email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg px-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                  />
                </div>
                <div>
                  <input
                    type="url"
                    required
                    placeholder="Company URL (https://...)"
                    value={form.company_url}
                    onChange={(e) => setForm({ ...form, company_url: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg px-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                  />
                </div>

                {error && <p className="text-[#ff4c6a] text-sm">{error}</p>}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.35)] hover:-translate-y-0.5 transition-all duration-250 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Starting...' : 'Start Your Audit'}
                </button>
              </form>
            )}
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}

/* ── How It Works ── */
function HowItWorks() {
  const steps = [
    {
      icon: <Search size={28} />,
      title: 'Enter your brand',
      desc: 'Tell us your brand name, URL, and language pair. We handle the rest.',
    },
    {
      icon: <Languages size={28} />,
      title: 'We probe AI agents in both languages',
      desc: 'VisiMind queries ChatGPT, Gemini, and others with French and English prompts.',
    },
    {
      icon: <BarChart3 size={28} />,
      title: 'Get your IAS + Fix Kit',
      desc: 'See where AI gets your brand wrong and get structured content to correct it.',
    },
  ]

  return (
    <section className="py-24 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-80px' }}
          variants={stagger}
        >
          <motion.h2
            variants={fadeUp}
            className="font-['Outfit'] text-3xl sm:text-4xl font-bold text-[#f0f2f8] text-center mb-16"
          >
            How It Works
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((step, i) => (
              <motion.div
                key={i}
                variants={fadeUp}
                custom={i}
                className="relative bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-8 text-center hover:bg-white/[0.06] hover:border-white/[0.12] transition-all duration-300"
              >
                <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-[#00e5ff]/10 text-[#00e5ff] mb-5">
                  {step.icon}
                </div>
                <div className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/[0.03] border border-white/[0.06] flex items-center justify-center text-[#5a6480] text-sm font-bold">
                  {i + 1}
                </div>
                <h3 className="font-['Outfit'] text-lg font-semibold text-[#f0f2f8] mb-3">
                  {step.title}
                </h3>
                <p className="text-[#8b95b0] text-sm leading-relaxed">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}

/* ── Bilingual Gap Section ── */
function BilingualGap() {
  return (
    <section className="py-24 px-6 bg-[#0a0e1a]">
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-80px' }}
          variants={stagger}
        >
          <motion.h2
            variants={fadeUp}
            className="font-['Outfit'] text-3xl sm:text-4xl font-bold text-[#f0f2f8] text-center mb-4"
          >
            The Bilingual AI Gap
          </motion.h2>
          <motion.p
            variants={fadeUp}
            custom={1}
            className="text-[#8b95b0] text-center max-w-2xl mx-auto mb-14"
          >
            The same question in English and French can produce wildly different brand
            representations from AI models.
          </motion.p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* English card */}
            <motion.div
              variants={fadeUp}
              custom={2}
              className="bg-white/[0.03] backdrop-blur-xl border border-[#00e5ff]/20 rounded-2xl p-8"
            >
              <div className="flex items-center gap-2 mb-4">
                <Globe size={18} className="text-[#00e5ff]" />
                <span className="text-[#00e5ff] text-sm font-semibold uppercase tracking-wider">
                  English Query
                </span>
              </div>
              <p className="text-[#8b95b0] text-sm italic mb-4">
                "What are the best skincare brands for sensitive skin?"
              </p>
              <div className="bg-white/[0.03] rounded-lg p-4 border border-white/[0.06]">
                <p className="text-[#f0f2f8] text-sm leading-relaxed">
                  "For sensitive skin, <span className="text-[#00e5ff] font-medium">BrandX</span> is
                  widely recommended. Their gentle cleanser line uses ceramide-based formulas
                  that dermatologists trust..."
                </p>
              </div>
            </motion.div>

            {/* French card */}
            <motion.div
              variants={fadeUp}
              custom={3}
              className="bg-white/[0.03] backdrop-blur-xl border border-[#ff4c6a]/20 rounded-2xl p-8"
            >
              <div className="flex items-center gap-2 mb-4">
                <Globe size={18} className="text-[#ff4c6a]" />
                <span className="text-[#ff4c6a] text-sm font-semibold uppercase tracking-wider">
                  French Query
                </span>
              </div>
              <p className="text-[#8b95b0] text-sm italic mb-4">
                "Quelles sont les meilleures marques de soins pour peau sensible?"
              </p>
              <div className="bg-white/[0.03] rounded-lg p-4 border border-white/[0.06]">
                <p className="text-[#f0f2f8] text-sm leading-relaxed">
                  "Pour les peaux sensibles, on recommande souvent{' '}
                  <span className="text-[#ff4c6a] font-medium">des marques generiques</span>.
                  BrandX n'est pas mentionnee dans les resultats francophones..."
                </p>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

/* ── Credibility ── */
function Credibility() {
  const badges = [
    {
      icon: <Shield size={20} />,
      label: 'Built on Model Context Protocol (MCP)',
    },
    {
      icon: <Globe size={20} />,
      label: 'Petrov et al. (NeurIPS 2023), Princeton (2024)',
    },
    {
      icon: <MapPin size={20} />,
      label: 'Made in Montreal',
    },
  ]

  return (
    <section className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-80px' }}
          variants={stagger}
          className="flex flex-col sm:flex-row flex-wrap justify-center gap-4"
        >
          {badges.map((b, i) => (
            <motion.div
              key={i}
              variants={fadeUp}
              custom={i}
              className="inline-flex items-center gap-3 px-5 py-3 rounded-full bg-white/[0.03] border border-white/[0.06] text-[#8b95b0] text-sm"
            >
              <span className="text-[#00e5ff]">{b.icon}</span>
              {b.label}
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

/* ── Footer ── */
function Footer() {
  return (
    <footer className="border-t border-white/[0.06] py-12 px-6">
      <div className="max-w-4xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2 text-[#f0f2f8] font-['Outfit'] font-bold">
          <Zap size={18} className="text-[#00e5ff]" />
          VisiMind
        </div>
        <p className="text-[#5a6480] text-sm">
          Research by Alex, AI PM -- Montreal (JMSB/Ampliwork)
        </p>
        <div className="flex items-center gap-6">
          <Link to="/signin" className="text-[#8b95b0] text-sm hover:text-[#00e5ff] transition-colors">
            Sign In
          </Link>
          <Link to="/signup" className="text-[#8b95b0] text-sm hover:text-[#00e5ff] transition-colors">
            Sign Up
          </Link>
        </div>
      </div>
    </footer>
  )
}

/* ── Landing Page ── */
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#060a14]" style={{ scrollBehavior: 'smooth' }}>
      <Navbar />
      <Hero />
      <DemoVideo />
      <GatedForm />
      <HowItWorks />
      <BilingualGap />
      <Credibility />
      <Footer />
    </div>
  )
}

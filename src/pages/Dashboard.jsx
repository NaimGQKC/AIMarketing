import { useState, useEffect, useRef } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Globe, DollarSign, Play, Loader2, RefreshCw, FileDown, ArrowRight } from 'lucide-react'
import { apiFetch, authHeaders } from '../api/client'
import { useBrand } from '../context/BrandContext'

const ACCENT = '#00e5ff'
const ACCENT_GLOW = 'rgba(0,229,255,0.12)'

function cleanProvider(raw) {
  if (!raw) return raw
  const p = raw.toLowerCase()
  if (p.includes('gemini')) return 'Gemini'
  if (p.includes('gpt') || p.includes('openai')) return 'ChatGPT'
  return raw
}

const METRIC_META = {
  french_visibility:  { label: 'French visibility',    max: 30, help: 'Does AI surface your brand in French queries?' },
  language_parity:    { label: 'Language parity',       max: 20, help: 'Equal brand visibility across EN and FR?' },
  content_accuracy:   { label: 'Content accuracy',      max: 20, help: 'Are facts correct? Any hallucinations?' },
  brand_protection:   { label: 'Brand protection',      max: 15, help: 'Is AI keeping your brand over competitors?' },
  response_depth:     { label: 'Response depth',        max: 15, help: 'Are AI responses substantive and detailed?' },
}

const GRADE_LABEL = { RED: 'Critical', YELLOW: 'Needs work', GREEN: 'Healthy' }

/* Map finding types to fixkit focus param */
const FINDING_FIX = {
  ghosting: 'structured-data',
  rank_disparity: 'structured-data',
  spec_dilution: 'mcp-feed',
  competitor_hijacking: 'mcp-feed',
}

/* ---- Components ---- */

function AnimatedScore({ target }) {
  const [value, setValue] = useState(0)
  useEffect(() => {
    if (!target && target !== 0) return
    const duration = 1200, start = Date.now()
    const tick = () => {
      const p = Math.min((Date.now() - start) / duration, 1)
      setValue(Math.round((1 - Math.pow(1 - p, 3)) * target))
      if (p < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  }, [target])
  return <span className="text-6xl font-['Outfit'] font-bold" style={{ color: ACCENT }}>{value}</span>
}

function MetricRow({ label, value, max, help }) {
  const pct = max > 0 ? (value / max) * 100 : 0
  return (
    <div className="py-4">
      <div className="flex items-baseline justify-between mb-2">
        <span className="text-[15px] text-[#f0f2f8]">{label}</span>
        <span className="text-sm font-mono text-[#5a6480]">{value}<span className="text-[#3a4050]">/{max}</span></span>
      </div>
      <div className="h-1.5 bg-white/[0.04] rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="h-full rounded-full"
          style={{ background: ACCENT, opacity: pct < 30 ? 0.35 : pct < 60 ? 0.65 : 1 }}
        />
      </div>
      <p className="text-xs text-[#8b95b0] mt-1.5">{help}</p>
    </div>
  )
}

function FindingItem({ finding, onFix }) {
  const key = finding.metric || finding.type || ''
  const typeLabel = key.replace(/_/g, ' ')
  const scorePct = finding.score_pct

  return (
    <div className="py-6">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-[#5a6480]">{typeLabel}</span>
            {scorePct != null && (
              <span className={`text-[11px] font-bold ${scorePct < 40 ? 'text-[#ff4c6a]' : scorePct < 70 ? 'text-[#f0a030]' : 'text-[#00e5ff]'}`}>
                {scorePct}%
              </span>
            )}
          </div>
          <p className="text-[15px] text-[#c8ccd8] leading-relaxed mt-2">{finding.message}</p>
        </div>
        <button
          onClick={() => onFix(key)}
          className="shrink-0 mt-1 flex items-center gap-1.5 px-4 py-2 rounded-lg text-[13px] font-medium text-[#00e5ff] border border-[#00e5ff]/20 hover:bg-[#00e5ff]/[0.06] transition-all"
        >
          Fix this <ArrowRight size={14} />
        </button>
      </div>
    </div>
  )
}

function ResponsePreview({ results }) {
  const en = results.filter(r => r.lang === 'EN' && r.response_text && !r.error)
  const fr = results.filter(r => r.lang === 'FR' && r.response_text && !r.error)
  const enSample = en[0]?.response_text || 'No English response collected'
  const frSample = fr[0]?.response_text || 'No French response collected'

  return (
    <div className="grid md:grid-cols-2 gap-8">
      {[
        { label: 'English', sample: enSample, provider: en[0] && cleanProvider(en[0].provider) },
        { label: 'French',  sample: frSample, provider: fr[0] && cleanProvider(fr[0].provider) },
      ].map(({ label, sample, provider }) => (
        <div key={label}>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Globe size={14} className="text-[#5a6480]" />
              <span className="text-xs font-semibold text-[#5a6480] uppercase tracking-wider">{label}</span>
            </div>
            {provider && <span className="text-xs text-[#3a4050]">{provider}</span>}
          </div>
          <p className="text-sm text-[#8b95b0] italic leading-relaxed max-h-52 overflow-y-auto">
            &ldquo;{sample.slice(0, 500)}{sample.length > 500 ? '...' : ''}&rdquo;
          </p>
        </div>
      ))}
    </div>
  )
}

/* ---- Main Dashboard ---- */

export default function Dashboard() {
  const navigate = useNavigate()
  const { selectedBrand, availableBrands, selectedBrandId } = useBrand()
  const [searchParams, setSearchParams] = useSearchParams()
  const [audit, setAudit] = useState(null)
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState('')
  const autorunTriggered = useRef(false)

  useEffect(() => {
    if (selectedBrandId) loadAudit(selectedBrandId)
    else setLoading(false)
  }, [selectedBrandId])

  useEffect(() => {
    if (searchParams.get('autorun') === '1' && selectedBrand && !audit && !loading && !running && !autorunTriggered.current) {
      autorunTriggered.current = true
      setSearchParams({}, { replace: true })
      runAudit()
    }
  }, [selectedBrand, audit, loading])

  async function loadAudit(brandId) {
    setLoading(true)
    setAudit(null)
    try {
      const results = await apiFetch(`/audits/${brandId}/results`)
      setAudit(results)
    } catch {
      // No audit yet
    } finally {
      setLoading(false)
    }
  }

  async function exportPdf() {
    if (!selectedBrand) return
    try {
      const API_URL = import.meta.env.VITE_API_URL || ''
      const res = await fetch(`${API_URL}/api/v1/exports/${selectedBrand.id}/pdf`, { headers: authHeaders() })
      if (!res.ok) throw new Error('PDF export failed')
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `VisiMind-Audit-${selectedBrand.brand_name}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      setError(err.message)
    }
  }

  async function runAudit() {
    if (!selectedBrand) return
    setRunning(true)
    setError('')
    try {
      const result = await apiFetch(`/audits/${selectedBrand.id}/run`, { method: 'POST' })
      setAudit({
        audit_id: result.audit_id,
        ias: result.ias,
        revenue_impact: result.revenue_impact,
        results: [],
        status: 'completed',
        created_at: new Date().toISOString(),
      })
      const full = await apiFetch(`/audits/${selectedBrand.id}/results`)
      setAudit(full)
    } catch (err) {
      setError(err.message)
    } finally {
      setRunning(false)
    }
  }

  function goToFix(findingType) {
    const focus = FINDING_FIX[findingType] || ''
    navigate(focus ? `/fixkit?focus=${focus}` : '/fixkit')
  }

  if (loading) {
    return (
      <div className="page flex items-center justify-center" style={{ minHeight: '60vh' }}>
        <Loader2 size={32} className="text-[#00e5ff] animate-spin" />
      </div>
    )
  }

  if (!availableBrands.length) {
    return (
      <div className="page">
        <div className="text-center py-20">
          <h2 className="text-3xl font-['Outfit'] font-bold mb-4">No brand configured</h2>
          <p className="text-[#8b95b0] text-lg mb-6">Set up your brand profile first to run an audit.</p>
          <a href="/setup" className="inline-flex px-6 py-3 rounded-xl bg-[#00e5ff] text-[#0a0e1a] font-semibold text-lg">
            Set Up Brand
          </a>
        </div>
      </div>
    )
  }

  const brand = selectedBrand || availableBrands[0]
  const ias = audit?.ias
  const revenue = audit?.revenue_impact
  const results = audit?.results || []
  const findings = ias?.findings || []
  const providers = [...new Set(results.map(r => cleanProvider(r.provider)).filter(Boolean))]

  return (
    <div className="page max-w-5xl">
      {/* Header */}
      <div className="flex items-start justify-between mb-12">
        <div>
          <h1 className="text-3xl font-['Outfit'] font-bold">{brand.brand_name}</h1>
          <p className="text-[#5a6480] text-sm mt-2">
            {audit ? `Audited ${new Date(audit.created_at).toLocaleDateString()}` : 'No audit yet'}
            {providers.length > 0 && <> &middot; {providers.join(', ')}</>}
            {ias && <> &middot; {ias.probes_analyzed} probes</>}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {audit && (
            <button
              onClick={exportPdf}
              className="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-white/[0.08] text-[#5a6480] text-sm hover:text-[#8b95b0] hover:border-white/[0.12] transition-all"
            >
              <FileDown size={16} /> PDF
            </button>
          )}
          <button
            onClick={runAudit}
            disabled={running}
            className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-[#00e5ff] text-[#0a0e1a] font-semibold text-sm shadow-[0_0_20px_rgba(0,229,255,0.15)] hover:shadow-[0_0_30px_rgba(0,229,255,0.25)] transition-all disabled:opacity-50"
          >
            {running ? <><Loader2 size={16} className="animate-spin" /> Running...</> : <><RefreshCw size={16} /> Run Audit</>}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 text-[#c8ccd8] text-sm">{error}</div>
      )}

      {!audit ? (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center py-24">
          <div className="w-24 h-24 rounded-2xl bg-[#00e5ff]/[0.06] flex items-center justify-center mx-auto mb-6">
            <Play size={36} className="text-[#00e5ff] ml-1" />
          </div>
          <h2 className="text-2xl font-['Outfit'] font-bold mb-3">Ready to audit {brand.brand_name}</h2>
          <p className="text-[#5a6480] text-lg mb-8 max-w-md mx-auto">
            We'll query AI models in English and French to measure how they represent your brand.
          </p>
        </motion.div>
      ) : (
        <div>
          {/* Score + Breakdown */}
          <div className="flex flex-col md:flex-row gap-14 items-start pb-10">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex-shrink-0"
            >
              <div className="flex flex-col items-center gap-4">
                <div
                  className="w-40 h-40 rounded-full flex items-center justify-center border-2"
                  style={{ borderColor: ACCENT, boxShadow: `0 0 50px ${ACCENT_GLOW}` }}
                >
                  <AnimatedScore target={ias?.score || 0} />
                </div>
                <div className="text-center">
                  <span className="text-sm font-medium text-[#5a6480] uppercase tracking-wider">
                    {GRADE_LABEL[ias?.grade] || 'Unknown'}
                  </span>
                  <p className="text-xs text-[#3a4050] mt-0.5">Inference Alignment Score</p>
                </div>
              </div>
            </motion.div>

            <div className="flex-1 min-w-0 pt-2">
              {ias?.breakdown && Object.entries(ias.breakdown).map(([key, val]) => {
                const meta = METRIC_META[key] || { label: key, max: 15, help: '' }
                return <MetricRow key={key} label={meta.label} value={val} max={meta.max} help={meta.help} />
              })}
            </div>
          </div>

          {/* Revenue impact */}
          {revenue && (
            <div className="py-10 border-t border-white/[0.04]">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign size={16} className="text-[#5a6480]" />
                <span className="text-xs text-[#5a6480] uppercase tracking-wider font-semibold">Estimated Revenue Impact</span>
              </div>
              <div className="flex items-baseline gap-4 flex-wrap mt-3">
                <span className="text-4xl font-['Outfit'] font-bold text-[#f0f2f8]">
                  ${revenue.lost_revenue_annual?.toLocaleString()}<span className="text-xl text-[#5a6480]">/yr</span>
                </span>
                <span className="text-base text-[#5a6480]">
                  {revenue.visibility_loss_pct}% visibility gap &middot; ~{revenue.lost_conversions_monthly} missed conversions/mo
                </span>
              </div>
              <p className="text-xs text-[#3a4050] mt-3">
                Based on 10K monthly AI searches, 3% conversion rate, $250 avg order.
              </p>
            </div>
          )}

          {/* Key Findings -- above raw responses */}
          {findings.length > 0 && (
            <div className="py-10 border-t border-white/[0.04]">
              <h3 className="text-base font-['Outfit'] font-semibold mb-2 text-[#8b95b0] uppercase tracking-wider">Key findings</h3>
              <div className="divide-y divide-white/[0.04]">
                {findings.map((f, i) => (
                  <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
                    <FindingItem finding={f} onFix={goToFix} />
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Raw AI Responses -- at the bottom */}
          <div className="py-10 border-t border-white/[0.04]">
            <h3 className="text-base font-['Outfit'] font-semibold mb-6 text-[#8b95b0] uppercase tracking-wider">What AI said</h3>
            <ResponsePreview results={results} />
          </div>
        </div>
      )}
    </div>
  )
}

import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle, Ghost, Shuffle, Globe, DollarSign, Play, Loader2, RefreshCw, FileDown, Lock } from 'lucide-react'
import { apiFetch, getToken, authHeaders } from '../api/client'
import { useBrand } from '../context/BrandContext'

const GRADE_COLORS = { RED: '#ff4c6a', YELLOW: '#ffb547', GREEN: '#34d399' }
const GRADE_GLOW = { RED: 'rgba(255,76,106,0.3)', YELLOW: 'rgba(255,181,71,0.3)', GREEN: 'rgba(52,211,153,0.3)' }

function AnimatedScore({ target, grade }) {
  const [value, setValue] = useState(0)
  const ref = useRef(null)

  useEffect(() => {
    if (!target) return
    let start = 0
    const duration = 1200
    const startTime = Date.now()
    const tick = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setValue(Math.round(eased * target))
      if (progress < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  }, [target])

  const color = GRADE_COLORS[grade] || '#00e5ff'
  const glow = GRADE_GLOW[grade] || 'rgba(0,229,255,0.3)'

  return (
    <div className="flex flex-col items-center">
      <div
        className="w-36 h-36 rounded-full flex items-center justify-center border-4"
        style={{ borderColor: color, boxShadow: `0 0 40px ${glow}, 0 0 80px ${glow}` }}
      >
        <span className="text-5xl font-headline font-bold" style={{ color }}>{value}</span>
      </div>
      <span className="mt-3 text-xs font-semibold uppercase tracking-wider" style={{ color }}>
        {grade === 'RED' ? 'Critical' : grade === 'YELLOW' ? 'Moderate' : 'Healthy'}
      </span>
      <span className="text-[#8b95b0] text-xs mt-1">Inference Alignment Score</span>
    </div>
  )
}

function FindingCard({ finding }) {
  const icons = { ghosting: Ghost, spec_dilution: Shuffle, competitor_hijacking: AlertTriangle, rank_disparity: Globe }
  const colors = { critical: '#ff4c6a', warning: '#ffb547' }
  const Icon = icons[finding.type] || AlertTriangle
  const color = colors[finding.severity] || '#ffb547'

  return (
    <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-5 hover:border-white/[0.12] transition-colors">
      <div className="flex items-center gap-2 mb-3">
        <Icon size={16} style={{ color }} />
        <span className="text-xs font-semibold uppercase tracking-wider" style={{ color }}>
          {finding.type.replace(/_/g, ' ')}
        </span>
      </div>
      <p className="text-sm text-[#f0f2f8] mb-3">{finding.message}</p>
      {finding.detail_en && (
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-[#0f1424] rounded-lg p-3 border border-white/[0.04]">
            <div className="text-[10px] font-semibold text-[#00e5ff] uppercase mb-1">English</div>
            <p className="text-xs text-[#8b95b0] leading-relaxed line-clamp-4">{finding.detail_en}</p>
          </div>
          <div className="bg-[#0f1424] rounded-lg p-3 border border-[#ff4c6a]/10">
            <div className="text-[10px] font-semibold text-[#ff4c6a] uppercase mb-1">French</div>
            <p className="text-xs text-[#8b95b0] leading-relaxed line-clamp-4">{finding.detail_fr || 'No response'}</p>
          </div>
        </div>
      )}
    </div>
  )
}

function SideBySide({ results }) {
  const en = results.filter(r => r.lang === 'EN' && r.response_text && !r.error)
  const fr = results.filter(r => r.lang === 'FR' && r.response_text && !r.error)
  const enSample = en[0]?.response_text || 'No English response collected'
  const frSample = fr[0]?.response_text || 'No French response collected'

  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-5">
        <div className="flex items-center gap-2 mb-3">
          <Globe size={14} className="text-[#00e5ff]" />
          <span className="text-xs font-semibold text-[#00e5ff] uppercase tracking-wider">English Response</span>
        </div>
        <p className="text-sm text-[#f0f2f8] italic leading-relaxed max-h-48 overflow-y-auto">
          {enSample.slice(0, 600)}{enSample.length > 600 ? '...' : ''}
        </p>
        {en[0] && <div className="mt-2 text-[10px] text-[#5a6480]">via {en[0].provider} ({en[0].model})</div>}
      </div>
      <div className="bg-white/[0.03] border border-[#ff4c6a]/20 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-3">
          <Globe size={14} className="text-[#ff4c6a]" />
          <span className="text-xs font-semibold text-[#ff4c6a] uppercase tracking-wider">French Response</span>
        </div>
        <p className="text-sm text-[#f0f2f8] italic leading-relaxed max-h-48 overflow-y-auto">
          {frSample.slice(0, 600)}{frSample.length > 600 ? '...' : ''}
        </p>
        {fr[0] && <div className="mt-2 text-[10px] text-[#5a6480]">via {fr[0].provider} ({fr[0].model})</div>}
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { selectedBrand, availableBrands, selectedBrandId } = useBrand()
  const [audit, setAudit] = useState(null)
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (selectedBrandId) {
      loadAudit(selectedBrandId)
    } else {
      setLoading(false)
    }
  }, [selectedBrandId])

  async function loadAudit(brandId) {
    setLoading(true)
    setAudit(null)
    try {
      const results = await apiFetch(`/audits/${brandId}/results`)
      setAudit(results)
    } catch {
      // No audit yet, that's fine
    } finally {
      setLoading(false)
    }
  }

  async function exportPdf() {
    if (!selectedBrand) return
    try {
      const res = await fetch(`/api/v1/exports/${selectedBrand.id}/pdf`, { headers: authHeaders() })
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
          <h2 className="text-2xl font-headline font-bold mb-4">No brand configured</h2>
          <p className="text-[#8b95b0] mb-6">Set up your brand profile first to run an audit.</p>
          <a href="/setup" className="inline-flex px-6 py-3 rounded-xl bg-[#00e5ff] text-[#0a0e1a] font-semibold">
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
  const providers = [...new Set(results.map(r => r.provider).filter(Boolean))]

  return (
    <div className="page">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="text-2xl font-headline font-bold truncate max-w-[70vw]">{brand.brand_name || 'Untitled Brand'} Audit Results</h1>
          <p className="text-[#8b95b0] text-sm mt-1">
            {audit ? `Last audit: ${new Date(audit.created_at).toLocaleDateString()}` : 'No audit run yet'}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {audit && (
            <button
              onClick={exportPdf}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 text-[#8b95b0] font-medium text-sm hover:text-white hover:border-white/20 transition-all"
            >
              <FileDown size={16} /> Export PDF
            </button>
          )}
          <button
            onClick={runAudit}
            disabled={running}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#00e5ff] text-[#0a0e1a] font-semibold text-sm shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.45)] transition-all disabled:opacity-50"
          >
            {running ? <><Loader2 size={16} className="animate-spin" /> Running Audit...</> : <><RefreshCw size={16} /> Run Audit</>}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-[#ff4c6a]/10 border border-[#ff4c6a]/20 text-[#ff4c6a] text-sm flex items-center justify-between gap-3">
          <span>{error}</span>
          <div className="flex items-center gap-2 flex-shrink-0">
            <button
              onClick={runAudit}
              disabled={running}
              className="text-xs underline hover:no-underline"
            >
              Retry
            </button>
            <button
              onClick={() => setError('')}
              className="text-[#ff4c6a]/60 hover:text-[#ff4c6a] transition-colors"
              aria-label="Dismiss error"
            >
              &times;
            </button>
          </div>
        </div>
      )}

      {!audit ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center py-20"
        >
          <div className="w-20 h-20 rounded-full bg-[#00e5ff]/10 flex items-center justify-center mx-auto mb-6">
            <Play size={32} className="text-[#00e5ff] ml-1" />
          </div>
          <h2 className="text-xl font-headline font-bold mb-3">Ready to audit {brand.brand_name || 'your brand'}</h2>
          <p className="text-[#8b95b0] mb-6 max-w-md mx-auto">
            Click "Run Audit" to probe AI agents in English and French and see how they represent your brand.
          </p>
        </motion.div>
      ) : (
        <div className="space-y-8">
          {/* IAS Score + Revenue Impact */}
          <div className="grid md:grid-cols-3 gap-6">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-8 flex items-center justify-center"
            >
              <AnimatedScore target={ias?.score || 0} grade={ias?.grade || 'RED'} />
            </motion.div>

            <div className="md:col-span-2 grid grid-cols-2 gap-4">
              {ias?.breakdown && Object.entries(ias.breakdown).map(([key, val]) => (
                <div key={key} className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-4">
                  <div className="text-xs text-[#8b95b0] uppercase tracking-wider mb-1">
                    {key.replace(/_/g, ' ')}
                  </div>
                  <div className="flex items-end gap-2">
                    <span className="text-2xl font-headline font-bold text-[#f0f2f8]">{val}</span>
                    <span className="text-xs text-[#5a6480] mb-1">/ {key === 'brand_in_fr_search' ? 30 : key === 'rank_parity' || key === 'specs_preserved' ? 20 : 15}</span>
                  </div>
                  <div className="mt-2 h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-700"
                      style={{
                        width: `${(val / (key === 'brand_in_fr_search' ? 30 : key === 'rank_parity' || key === 'specs_preserved' ? 20 : 15)) * 100}%`,
                        background: val > 10 ? '#34d399' : val > 5 ? '#ffb547' : '#ff4c6a'
                      }}
                    />
                  </div>
                </div>
              ))}

              {revenue && (
                <div className="col-span-2 bg-white/[0.03] border border-[#ff4c6a]/20 rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-1">
                    <DollarSign size={14} className="text-[#ff4c6a]" />
                    <span className="text-xs text-[#ff4c6a] uppercase tracking-wider font-semibold">Estimated Revenue Impact</span>
                  </div>
                  <div className="flex items-baseline gap-3 flex-wrap">
                    <span className="text-2xl font-headline font-bold text-[#f0f2f8]">
                      ${(revenue.lost_revenue_annual ?? 0).toLocaleString()}/yr
                    </span>
                    <span className="text-sm text-[#8b95b0]">
                      ({revenue.visibility_loss_pct ?? 0}% visibility loss, ~{revenue.lost_conversions_monthly ?? 0} lost conversions/mo)
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Provider badges */}
          <div className="flex items-center gap-3">
            <span className="text-xs text-[#5a6480] uppercase tracking-wider">Agents tested:</span>
            {providers.map(p => (
              <span key={p} className="px-3 py-1 rounded-full bg-white/[0.03] border border-white/[0.06] text-xs font-semibold text-[#f0f2f8] capitalize">
                {p}
              </span>
            ))}
            {ias && <span className="text-xs text-[#5a6480]">{ias.probes_analyzed} probes ({ias.en_probes} EN, {ias.fr_probes} FR)</span>}
          </div>

          {/* Side-by-side EN/FR */}
          <div>
            <h3 className="text-lg font-headline font-bold mb-4">What AI agents said about {brand.brand_name}</h3>
            <SideBySide results={results} />
          </div>

          {/* Findings */}
          {findings.length > 0 && (
            <div>
              <h3 className="text-lg font-headline font-bold mb-4">Key Findings</h3>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {findings.map((f, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                  >
                    <FindingCard finding={f} />
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Gated Upsell — Fix Kit CTA */}
          {audit && findings.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white/[0.03] backdrop-blur border border-white/[0.06] rounded-xl p-8"
            >
              <div className="flex flex-col items-center text-center max-w-xl mx-auto">
                <div className="w-14 h-14 rounded-full bg-[#00e5ff]/10 flex items-center justify-center mb-5">
                  <Lock size={24} className="text-[#00e5ff]" />
                </div>
                <h3 className="text-xl font-headline font-bold text-[#f0f2f8] mb-3">
                  Unlock Your Fix Kit
                </h3>
                <p className="text-sm text-[#8b95b0] leading-relaxed mb-6">
                  Your audit revealed {findings.length} critical finding{findings.length !== 1 ? 's' : ''}. Get a personalized remediation plan with metadata patches, brand voice corrections, and MCP feed deployment.
                </p>
                <div className="flex items-center gap-4">
                  <a
                    href="#book-call"
                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#00e5ff] text-[#0a0e1a] font-semibold text-sm shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.45)] transition-all"
                  >
                    Book a Strategy Call &rarr;
                  </a>
                  <a
                    href="/remediate"
                    className="inline-flex items-center gap-2 px-6 py-3 rounded-xl border border-white/10 text-[#8b95b0] font-medium text-sm hover:text-white hover:border-white/20 transition-all"
                  >
                    Explore on your own &rarr;
                  </a>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      )}
    </div>
  )
}

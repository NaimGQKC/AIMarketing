import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { RefreshCw, Loader2, TrendingUp, Check, X, Globe } from 'lucide-react'
import { apiFetch } from '../api/client'
import { useBrand } from '../context/BrandContext'

const ACCENT = '#00e5ff'

/* ---- Animated IAS counter ---- */
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

/* ---- Chart tooltip ---- */
function ChartTooltip({ active, payload, label }) {
  if (!active || !payload) return null
  return (
    <div className="bg-[#151b2e] border border-white/10 rounded-lg p-3 text-xs">
      <div className="text-[#5a6480] mb-1">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="flex items-center gap-2 text-[#f0f2f8]">
          <span style={{ color: p.color }}>*</span>
          <span>{p.name}: {p.value}</span>
        </div>
      ))}
    </div>
  )
}

/* ---- Provider mention-rate bar ---- */
function ProviderRow({ provider, mentioned, total, rate }) {
  return (
    <div className="py-5">
      <div className="flex items-baseline justify-between mb-2">
        <span className="text-[15px] text-[#f0f2f8] capitalize">{provider}</span>
        <span className="flex items-center gap-1.5 text-xs font-medium" style={{ color: rate >= 50 ? ACCENT : '#ff4c6a' }}>
          {rate >= 50 ? <Check size={12} /> : <X size={12} />}
          {rate}% mention rate
        </span>
      </div>
      <div className="h-1.5 bg-white/[0.04] rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${rate}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="h-full rounded-full"
          style={{ background: ACCENT, opacity: rate < 30 ? 0.35 : rate < 60 ? 0.65 : 1 }}
        />
      </div>
      <p className="text-xs text-[#5a6480] mt-1.5">
        Brand mentioned in {mentioned}/{total} probes
      </p>
    </div>
  )
}

/* ---- Single probe response row ---- */
function ProbeRow({ result }) {
  const r = result
  return (
    <div className="py-5">
      <div className="flex items-center gap-2 mb-2 flex-wrap">
        <Globe size={12} className="text-[#5a6480]" />
        <span className="text-[11px] font-semibold uppercase tracking-widest text-[#5a6480]">
          {r.lang}
        </span>
        <span className="text-[11px] text-[#3a4050]">{r.probe_type?.replace(/_/g, ' ')}</span>
        <span className="text-[11px] text-[#3a4050] capitalize">via {r.provider}</span>
        {r.brand_mentioned ? (
          <span className="flex items-center gap-1 text-[11px] font-medium" style={{ color: ACCENT }}>
            <Check size={10} /> Mentioned
          </span>
        ) : (
          <span className="flex items-center gap-1 text-[11px] font-medium text-[#ff4c6a]">
            <X size={10} /> Missing
          </span>
        )}
      </div>
      <p className="text-xs text-[#8b95b0] leading-relaxed line-clamp-3">
        {r.response_text?.slice(0, 300) || r.error || 'No response'}
        {r.response_text?.length > 300 ? '...' : ''}
      </p>
    </div>
  )
}

/* ==================================================================== */
/*  Main Monitor Page                                                    */
/* ==================================================================== */
export default function Verify() {
  const { selectedBrand, selectedBrandId, availableBrands } = useBrand()
  const [history, setHistory] = useState([])
  const [latestAudit, setLatestAudit] = useState(null)
  const [loading, setLoading] = useState(true)
  const [reprobing, setReprobing] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (selectedBrandId) {
      loadData(selectedBrandId)
    } else {
      setLoading(false)
    }
  }, [selectedBrandId])

  async function loadData(brandId) {
    setLoading(true)
    setError('')
    try {
      try {
        const hist = await apiFetch(`/audits/${brandId}/history`)
        setHistory(hist)
      } catch {
        // No history yet
      }
      try {
        const results = await apiFetch(`/audits/${brandId}/results`)
        setLatestAudit(results)
      } catch {
        // No results yet
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleReprobe() {
    if (!selectedBrand) return
    setReprobing(true)
    setError('')
    try {
      await apiFetch(`/audits/${selectedBrand.id}/run`, { method: 'POST' })
      await loadData(selectedBrand.id)
    } catch (err) {
      setError(err.message)
    } finally {
      setReprobing(false)
    }
  }

  /* ---- Loading state ---- */
  if (loading) {
    return (
      <div className="page flex items-center justify-center" style={{ minHeight: '60vh' }}>
        <Loader2 size={32} className="text-[#00e5ff] animate-spin" />
      </div>
    )
  }

  /* ---- No brand configured ---- */
  if (!availableBrands.length) {
    return (
      <div className="page max-w-5xl">
        <div className="text-center py-20">
          <h2 className="text-3xl font-['Outfit'] font-bold mb-4">No brand configured</h2>
          <p className="text-[#8b95b0] text-lg mb-6">Set up your brand profile first to start monitoring.</p>
          <a href="/setup" className="inline-flex px-6 py-3 rounded-xl bg-[#00e5ff] text-[#0a0e1a] font-semibold text-lg">
            Set Up Brand
          </a>
        </div>
      </div>
    )
  }

  const brand = selectedBrand || availableBrands[0]
  const ias = latestAudit?.ias
  const results = latestAudit?.results || []
  const providers = [...new Set(results.map(r => r.provider).filter(Boolean))]

  // Build trend data for chart
  const trendData = history.map(h => ({
    date: new Date(h.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    score: h.ias_score || 0,
  }))

  // Per-provider breakdown
  const providerBreakdown = providers.map(p => {
    const provResults = results.filter(r => r.provider === p)
    const mentioned = provResults.filter(r => r.brand_mentioned).length
    const total = provResults.length
    return {
      provider: p,
      mentioned,
      total,
      rate: total > 0 ? Math.round((mentioned / total) * 100) : 0,
    }
  })

  // Trend delta
  const hasMultiplePoints = trendData.length >= 2
  const firstScore = trendData[0]?.score
  const lastScore = trendData[trendData.length - 1]?.score
  const delta = hasMultiplePoints ? lastScore - firstScore : null

  return (
    <div className="page max-w-5xl">
      {/* ---- Header ---- */}
      <div className="flex items-start justify-between mb-12">
        <div>
          <h1 className="text-3xl font-['Outfit'] font-bold">Monitor</h1>
          <p className="text-[#5a6480] text-sm mt-2">
            Track how AI agents update their responses after deploying fixes for {brand.brand_name}
          </p>
        </div>
        <button
          onClick={handleReprobe}
          disabled={reprobing}
          className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-[#00e5ff] text-[#0a0e1a] font-semibold text-sm shadow-[0_0_20px_rgba(0,229,255,0.15)] hover:shadow-[0_0_30px_rgba(0,229,255,0.25)] transition-all disabled:opacity-50"
        >
          {reprobing
            ? <><Loader2 size={16} className="animate-spin" /> Re-probing...</>
            : <><RefreshCw size={16} /> Re-probe Now</>}
        </button>
      </div>

      {/* ---- Error ---- */}
      {error && (
        <div className="mb-6 text-[#ff4c6a] text-sm">{error}</div>
      )}

      {/* ---- Empty state ---- */}
      {!latestAudit ? (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center py-24">
          <h2 className="text-2xl font-['Outfit'] font-bold mb-3">No audit data yet</h2>
          <p className="text-[#5a6480] text-lg max-w-md mx-auto">
            Run an audit from the Dashboard first, then come back here to track changes over time.
          </p>
        </motion.div>
      ) : (
        <div>
          {/* ============================================================ */}
          {/*  1. IAS Score + Trend Chart                                   */}
          {/* ============================================================ */}
          <section className="pb-10">
            {trendData.length === 0 ? (
              /* No history at all -- just show current score */
              <div className="flex flex-col items-center py-8">
                <AnimatedScore target={ias?.score || 0} />
                <p className="text-xs text-[#3a4050] mt-1">Inference Alignment Score</p>
                <p className="text-sm text-[#5a6480] mt-4">Run more audits to see the trend line</p>
              </div>
            ) : trendData.length === 1 ? (
              /* Single data point */
              <div className="flex flex-col items-center py-8">
                <AnimatedScore target={ias?.score || 0} />
                <p className="text-xs text-[#3a4050] mt-1">Inference Alignment Score</p>
                <p className="text-sm text-[#5a6480] mt-4">Run more audits to see the trend line</p>
              </div>
            ) : (
              /* Multiple data points -- show chart */
              <>
                <div className="flex items-center gap-2.5 mb-6">
                  <TrendingUp size={18} className="text-[#00e5ff]" />
                  <h2 className="text-lg font-['Outfit'] font-bold">IAS Score Over Time</h2>
                </div>

                <ResponsiveContainer width="100%" height={240}>
                  <AreaChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="gradScore" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#00e5ff" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#00e5ff" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                    <XAxis dataKey="date" tick={{ fill: '#5a6480', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: '#5a6480', fontSize: 11 }} axisLine={false} tickLine={false} domain={[0, 100]} />
                    <Tooltip content={<ChartTooltip />} />
                    <Area type="monotone" dataKey="score" name="IAS Score" stroke="#00e5ff" fill="url(#gradScore)" strokeWidth={2} dot={{ r: 4, fill: '#00e5ff' }} />
                  </AreaChart>
                </ResponsiveContainer>

                {/* Delta summary */}
                {delta !== null && (
                  <p className="text-sm text-[#c8ccd8] mt-6">
                    Your IAS went from{' '}
                    <span className="font-bold" style={{ color: ACCENT }}>{firstScore}</span>
                    {' '}to{' '}
                    <span className="font-bold" style={{ color: ACCENT }}>{lastScore}</span>
                    {' '}after deploying fixes
                    {delta > 0 && <span className="text-[#5a6480]"> ({'+' + delta} points)</span>}
                    {delta < 0 && <span className="text-[#5a6480]"> ({delta} points)</span>}
                    .
                  </p>
                )}
              </>
            )}
          </section>

          {/* ============================================================ */}
          {/*  2. Per-Agent Breakdown                                       */}
          {/* ============================================================ */}
          <section className="py-10 border-t border-white/[0.04]">
            <h2 className="text-lg font-['Outfit'] font-bold mb-2">Per-Agent Breakdown</h2>
            <p className="text-sm text-[#5a6480] mb-4">Brand mention rate across each AI provider</p>

            {providerBreakdown.length === 0 ? (
              <p className="text-sm text-[#5a6480]">No provider data available</p>
            ) : (
              <div className="divide-y divide-white/[0.04]">
                {providerBreakdown.map(pb => (
                  <ProviderRow
                    key={pb.provider}
                    provider={pb.provider}
                    mentioned={pb.mentioned}
                    total={pb.total}
                    rate={pb.rate}
                  />
                ))}
              </div>
            )}
          </section>

          {/* ============================================================ */}
          {/*  3. Latest Probe Responses                                    */}
          {/* ============================================================ */}
          <section className="py-10 border-t border-white/[0.04]">
            <h3 className="text-base font-['Outfit'] font-semibold mb-2 text-[#8b95b0] uppercase tracking-wider">
              Latest probe responses
            </h3>
            <p className="text-sm text-[#5a6480] mb-4">
              {results.length} probe{results.length !== 1 ? 's' : ''} collected
            </p>

            {results.length === 0 ? (
              <p className="text-sm text-[#5a6480]">No probe responses available</p>
            ) : (
              <div className="divide-y divide-white/[0.04]">
                {results.slice(0, 6).map((r, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.06 }}
                  >
                    <ProbeRow result={r} />
                  </motion.div>
                ))}
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  )
}

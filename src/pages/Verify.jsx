import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { Activity, RefreshCw, Loader2, TrendingUp, Check, X, Globe } from 'lucide-react'
import { apiFetch } from '../api/client'

const GRADE_COLORS = { RED: '#ff4c6a', YELLOW: '#ffb547', GREEN: '#34d399' }

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload) return null
  return (
    <div className="bg-[#151b2e] border border-white/10 rounded-lg p-3 text-xs">
      <div className="text-[#5a6480] mb-1">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="flex items-center gap-2 text-[#f0f2f8]">
          <span style={{ color: p.color }}>●</span>
          <span>{p.name}: {p.value}</span>
        </div>
      ))}
    </div>
  )
}

export default function Verify() {
  const [brands, setBrands] = useState([])
  const [history, setHistory] = useState([])
  const [latestAudit, setLatestAudit] = useState(null)
  const [loading, setLoading] = useState(true)
  const [reprobing, setReprobing] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    try {
      const brandList = await apiFetch('/brands')
      setBrands(brandList)
      if (brandList.length > 0) {
        const brandId = brandList[0].id
        try {
          const hist = await apiFetch(`/audits/${brandId}/history`)
          setHistory(hist)
        } catch {}
        try {
          const results = await apiFetch(`/audits/${brandId}/results`)
          setLatestAudit(results)
        } catch {}
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleReprobe() {
    if (!brands.length) return
    setReprobing(true)
    setError('')
    try {
      await apiFetch(`/audits/${brands[0].id}/run`, { method: 'POST' })
      await loadData()
    } catch (err) {
      setError(err.message)
    } finally {
      setReprobing(false)
    }
  }

  if (loading) {
    return (
      <div className="page flex items-center justify-center" style={{ minHeight: '60vh' }}>
        <Loader2 size={32} className="text-[#00e5ff] animate-spin" />
      </div>
    )
  }

  if (!brands.length) {
    return (
      <div className="page">
        <div className="text-center py-20">
          <h2 className="text-xl font-['Outfit'] font-bold mb-3">No brand configured</h2>
          <p className="text-[#8b95b0]">Set up your brand to start monitoring.</p>
        </div>
      </div>
    )
  }

  const brand = brands[0]
  const ias = latestAudit?.ias
  const results = latestAudit?.results || []
  const enResults = results.filter(r => r.lang === 'EN' && !r.error)
  const frResults = results.filter(r => r.lang === 'FR' && !r.error)
  const providers = [...new Set(results.map(r => r.provider).filter(Boolean))]

  // Build trend data for chart
  const trendData = history.map((h, i) => ({
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

  return (
    <div className="page">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="text-2xl font-['Outfit'] font-bold flex items-center gap-3">
            <Activity size={24} className="text-[#00e5ff]" />
            Agent Monitor
          </h1>
          <p className="text-[#8b95b0] text-sm mt-1">
            Track how AI agents update their responses after deploying fixes for {brand.brand_name}
          </p>
        </div>
        <button
          onClick={handleReprobe}
          disabled={reprobing}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#00e5ff] text-[#0a0e1a] font-semibold text-sm shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.45)] transition-all disabled:opacity-50"
        >
          {reprobing ? <><Loader2 size={16} className="animate-spin" /> Re-probing...</> : <><RefreshCw size={16} /> Re-probe Now</>}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-[#ff4c6a]/10 border border-[#ff4c6a]/20 text-[#ff4c6a] text-sm">
          {error}
        </div>
      )}

      {!latestAudit ? (
        <div className="text-center py-16">
          <p className="text-[#8b95b0]">No audit data yet. Run an audit from the Dashboard first.</p>
        </div>
      ) : (
        <div className="space-y-8">
          {/* IAS Trend Chart */}
          {trendData.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-6"
            >
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp size={18} className="text-[#00e5ff]" />
                <h3 className="text-lg font-['Outfit'] font-bold">IAS Score Over Time</h3>
              </div>
              {trendData.length === 1 ? (
                <div className="text-center py-8">
                  <div className="text-4xl font-['Outfit'] font-bold mb-2" style={{ color: GRADE_COLORS[ias?.grade] || '#00e5ff' }}>
                    {ias?.score || 0}
                  </div>
                  <p className="text-sm text-[#8b95b0]">Run more audits to see the trend line</p>
                </div>
              ) : (
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
                    <Tooltip content={<CustomTooltip />} />
                    <Area type="monotone" dataKey="score" name="IAS Score" stroke="#00e5ff" fill="url(#gradScore)" strokeWidth={2} dot={{ r: 4, fill: '#00e5ff' }} />
                  </AreaChart>
                </ResponsiveContainer>
              )}
              {trendData.length >= 2 && (
                <div className="mt-4 p-4 rounded-xl bg-[#0f1424] border border-white/[0.04]">
                  <p className="text-sm text-[#f0f2f8]">
                    Your IAS went from{' '}
                    <span className="font-bold text-[#ff4c6a]">{trendData[0].score}</span>
                    {' '}to{' '}
                    <span className="font-bold text-[#34d399]">{trendData[trendData.length - 1].score}</span>
                    {' '}after deploying fixes.
                  </p>
                </div>
              )}
            </motion.div>
          )}

          {/* Per-Agent Breakdown */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-6"
          >
            <h3 className="text-lg font-['Outfit'] font-bold mb-4">Per-Agent Breakdown</h3>
            {providerBreakdown.length === 0 ? (
              <p className="text-sm text-[#8b95b0]">No provider data available</p>
            ) : (
              <div className="grid md:grid-cols-2 gap-4">
                {providerBreakdown.map(pb => (
                  <div key={pb.provider} className="bg-[#0f1424] rounded-xl p-4 border border-white/[0.04]">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-semibold text-[#f0f2f8] capitalize">{pb.provider}</span>
                      <span className={`flex items-center gap-1 text-xs font-semibold ${pb.rate >= 50 ? 'text-[#34d399]' : 'text-[#ff4c6a]'}`}>
                        {pb.rate >= 50 ? <Check size={12} /> : <X size={12} />}
                        {pb.rate}% mention rate
                      </span>
                    </div>
                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-700"
                        style={{
                          width: `${pb.rate}%`,
                          background: pb.rate >= 50 ? '#34d399' : pb.rate >= 30 ? '#ffb547' : '#ff4c6a',
                        }}
                      />
                    </div>
                    <div className="mt-2 text-xs text-[#5a6480]">
                      Brand mentioned in {pb.mentioned}/{pb.total} probes
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>

          {/* Before/After Side-by-Side (shows EN vs FR for latest audit) */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-6"
          >
            <h3 className="text-lg font-['Outfit'] font-bold mb-4">Latest Probe Responses</h3>
            <div className="space-y-4">
              {results.slice(0, 6).map((r, i) => (
                <div key={i} className="bg-[#0f1424] rounded-xl p-4 border border-white/[0.04]">
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <Globe size={12} className={r.lang === 'EN' ? 'text-[#00e5ff]' : 'text-[#ff4c6a]'} />
                    <span className={`text-[10px] font-semibold uppercase tracking-wider ${r.lang === 'EN' ? 'text-[#00e5ff]' : 'text-[#ff4c6a]'}`}>
                      {r.lang}
                    </span>
                    <span className="text-[10px] text-[#5a6480]">{r.probe_type?.replace(/_/g, ' ')}</span>
                    <span className="text-[10px] text-[#5a6480] capitalize">via {r.provider}</span>
                    {r.brand_mentioned ? (
                      <span className="flex items-center gap-1 text-[10px] text-[#34d399] font-semibold"><Check size={10} /> Mentioned</span>
                    ) : (
                      <span className="flex items-center gap-1 text-[10px] text-[#ff4c6a] font-semibold"><X size={10} /> Missing</span>
                    )}
                  </div>
                  <p className="text-xs text-[#8b95b0] leading-relaxed line-clamp-3">
                    {r.response_text?.slice(0, 300) || r.error || 'No response'}
                    {r.response_text?.length > 300 ? '...' : ''}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}

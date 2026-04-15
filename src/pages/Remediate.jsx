import { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import {
  Code2,
  FileJson,
  Shield,
  Copy,
  Download,
  Check,
  X,
  Loader2,
  ExternalLink,
  Bot,
} from 'lucide-react'
import { apiFetch } from '../api/client'
import { useBrand } from '../context/BrandContext'

/* ------------------------------------------------------------------ */
/*  Fix Kit Page (Screen 4) - MCP Feed, JSON-LD, robots.txt panels    */
/* ------------------------------------------------------------------ */

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.45, ease: 'easeOut' },
  }),
}

/* ---------- tiny helpers ---------- */
function StatusBadge({ status }) {
  const map = {
    deployed: {
      bg: 'bg-emerald-500/15',
      text: 'text-emerald-400',
      dot: 'bg-emerald-400',
      label: 'Deployed',
    },
    pending: {
      bg: 'bg-amber-500/15',
      text: 'text-amber-400',
      dot: 'bg-amber-400',
      label: 'Pending',
    },
    verified: {
      bg: 'bg-emerald-500/15',
      text: 'text-emerald-400',
      dot: 'bg-emerald-400',
      label: 'Verified',
    },
    not_deployed: {
      bg: 'bg-white/[0.06]',
      text: 'text-[#8b95b0]',
      dot: 'bg-[#8b95b0]',
      label: 'Not deployed',
    },
  }
  const s = map[status] || map.not_deployed
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[0.68rem] font-semibold ${s.bg} ${s.text}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${s.dot}`} />
      {s.label}
    </span>
  )
}

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false)
  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }, [text])
  return (
    <button
      onClick={handleCopy}
      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-white/[0.06] hover:bg-white/[0.1] text-[#c4ccde] transition-colors cursor-pointer"
    >
      {copied ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
      {copied ? 'Copied' : 'Copy URL'}
    </button>
  )
}

/* ---------- Panel wrapper ---------- */
function Panel({ icon: Icon, title, children, index }) {
  return (
    <motion.div
      className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-6"
      variants={fadeUp}
      initial="hidden"
      animate="visible"
      custom={index}
    >
      <div className="flex items-center gap-2.5 mb-5">
        <Icon size={18} className="text-[#00e5ff]" />
        <h3 className="text-lg font-['Outfit'] font-bold text-white">{title}</h3>
      </div>
      {children}
    </motion.div>
  )
}

/* ------------------------------------------------------------------ */
/*  JSON-LD tab names                                                  */
/* ------------------------------------------------------------------ */
const JSONLD_TABS = [
  { key: 'organization', label: 'Organization' },
  { key: 'local_business', label: 'Local Business' },
  { key: 'faq', label: 'FAQ' },
]

/* ================================================================== */
/*  Main Component                                                     */
/* ================================================================== */
export default function Remediate() {
  /* --- brand context --- */
  const { selectedBrandId } = useBrand()
  const brandId = selectedBrandId

  /* --- shared state --- */
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /* --- MCP Feed --- */
  const [mcpPreview, setMcpPreview] = useState(null)
  const [mcpValid, setMcpValid] = useState(false)
  const [mcpDeploying, setMcpDeploying] = useState(false)
  const [mcpStatus, setMcpStatus] = useState('not_deployed')

  /* --- JSON-LD --- */
  const [jsonLdData, setJsonLdData] = useState(null)
  const [jsonLdTab, setJsonLdTab] = useState('organization')
  const [jsonLdStatus, setJsonLdStatus] = useState('not_deployed')

  /* --- robots.txt --- */
  const [robotsUrl, setRobotsUrl] = useState('')
  const [robotsScanning, setRobotsScanning] = useState(false)
  const [robotsResult, setRobotsResult] = useState(null)
  const [robotsStatus, setRobotsStatus] = useState('not_deployed')

  /* ---- fetch MCP + JSON-LD once brandId is known ---- */
  useEffect(() => {
    if (!brandId) return
    let cancelled = false

    async function fetchFeeds() {
      try {
        const [mcp, jld] = await Promise.all([
          apiFetch(`/feeds/${brandId}/mcp/preview`).catch(() => null),
          apiFetch(`/feeds/${brandId}/jsonld`).catch(() => null),
        ])
        if (cancelled) return
        if (mcp) {
          setMcpPreview(mcp)
          setMcpValid(true)
        }
        if (jld) {
          setJsonLdData(jld)
        }
      } catch {
        // individual catches above handle per-request errors
      }
    }
    fetchFeeds()
    return () => { cancelled = true }
  }, [brandId])

  /* ---- handlers ---- */
  const handleDeployMcp = useCallback(async () => {
    if (!brandId) return
    setMcpDeploying(true)
    try {
      await apiFetch(`/feeds/${brandId}/mcp/deploy`, { method: 'POST' })
      setMcpStatus('deployed')
    } catch {
      // silently keep current status
    } finally {
      setMcpDeploying(false)
    }
  }, [brandId])

  const handleDownloadJsonLd = useCallback(() => {
    if (!jsonLdData) return
    const blob = new Blob([JSON.stringify(jsonLdData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `jsonld-patches-${brandId}.json`
    a.click()
    URL.revokeObjectURL(url)
    setJsonLdStatus('pending')
  }, [jsonLdData, brandId])

  const handleScanRobots = useCallback(async () => {
    if (!brandId || !robotsUrl.trim()) return
    setRobotsScanning(true)
    setRobotsResult(null)
    try {
      const result = await apiFetch(`/feeds/${brandId}/robots-check`, {
        method: 'POST',
        body: JSON.stringify({ url: robotsUrl.trim() }),
      })
      /* Normalise: backend returns blocked_bots / allowed_bots string arrays;
         UI expects a unified bots[] with { name, allowed } objects. */
      const bots = [
        ...(result.allowed_bots || []).map((name) => ({ name, allowed: true })),
        ...(result.blocked_bots || []).map((name) => ({ name, allowed: false })),
      ]
      setRobotsResult({ ...result, bots })
      if (result?.blocked_bots?.length === 0) {
        setRobotsStatus('verified')
      } else {
        setRobotsStatus('pending')
      }
    } catch {
      setRobotsResult({ error: 'Failed to scan robots.txt. Check the URL and try again.' })
    } finally {
      setRobotsScanning(false)
    }
  }, [brandId, robotsUrl])

  /* ---- feed URL (for copy) ---- */
  const mcpFeedUrl = brandId
    ? `${window.location.origin}/api/v1/feeds/${brandId}/mcp.json`
    : ''

  /* ================================================================ */
  /*  Loading / Error states                                           */
  /* ================================================================ */
  if (loading) {
    return (
      <div className="min-h-screen bg-[#060a14] flex items-center justify-center">
        <Loader2 size={28} className="animate-spin text-[#00e5ff]" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#060a14] flex items-center justify-center">
        <p className="text-red-400 text-sm">{error}</p>
      </div>
    )
  }

  /* ================================================================ */
  /*  Render                                                           */
  /* ================================================================ */
  return (
    <div className="min-h-screen bg-[#060a14] text-white px-6 py-10 lg:px-10">
      {/* Page header */}
      <motion.div
        className="mb-10"
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h1 className="text-3xl font-['Outfit'] font-bold mb-1">Fix Kit</h1>
        <p className="text-[#8b95b0] text-sm">
          Deploy structured feeds, JSON-LD patches, and crawler policies to
          control how AI models represent your brand.
        </p>
      </motion.div>

      {/* ---- Status row ---- */}
      <motion.div
        className="flex flex-wrap gap-4 mb-8"
        variants={fadeUp}
        initial="hidden"
        animate="visible"
        custom={0}
      >
        {[
          { label: 'MCP Feed', status: mcpStatus, icon: Code2 },
          { label: 'JSON-LD', status: jsonLdStatus, icon: FileJson },
          { label: 'robots.txt', status: robotsStatus, icon: Shield },
        ].map(({ label, status, icon: Ic }) => (
          <div
            key={label}
            className="flex items-center gap-3 bg-white/[0.03] border border-white/[0.06] rounded-xl px-4 py-2.5"
          >
            <Ic size={15} className="text-[#00e5ff]" />
            <span className="text-sm text-[#c4ccde] font-medium">{label}</span>
            <StatusBadge status={status} />
          </div>
        ))}
      </motion.div>

      {/* ---- Panels grid ---- */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ====================================================== */}
        {/*  1. MCP Feed Panel                                      */}
        {/* ====================================================== */}
        <Panel icon={Code2} title="MCP Feed" index={1}>
          {/* Feed URL + copy */}
          <div className="flex items-center gap-2 mb-4 flex-wrap">
            <code className="text-[0.7rem] text-[#8b95b0] bg-[#0a0e1a] px-3 py-1.5 rounded-lg truncate max-w-md">
              {mcpFeedUrl || 'No brand selected'}
            </code>
            {mcpFeedUrl && <CopyButton text={mcpFeedUrl} />}
          </div>

          {/* Validation badge */}
          <div className="flex items-center gap-2 mb-4">
            {mcpValid ? (
              <span className="inline-flex items-center gap-1.5 text-emerald-400 text-xs font-medium">
                <Check size={14} /> Valid JSON
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 text-[#8b95b0] text-xs font-medium">
                <Loader2 size={14} className="animate-spin" /> Loading preview...
              </span>
            )}
          </div>

          {/* JSON preview */}
          <pre className="bg-[#0a0e1a] rounded-xl p-4 font-mono text-xs text-[#8b95b0] overflow-auto max-h-80 mb-5 whitespace-pre-wrap">
            {mcpPreview
              ? JSON.stringify(mcpPreview, null, 2)
              : '// Waiting for MCP feed data...'}
          </pre>

          {/* Deploy button */}
          <button
            onClick={handleDeployMcp}
            disabled={mcpDeploying || mcpStatus === 'deployed'}
            className="inline-flex items-center gap-2 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl px-5 py-2.5 text-sm hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {mcpDeploying ? (
              <>
                <Loader2 size={15} className="animate-spin" />
                Deploying...
              </>
            ) : mcpStatus === 'deployed' ? (
              <>
                <Check size={15} />
                Deployed
              </>
            ) : (
              <>
                <ExternalLink size={15} />
                Deploy MCP Feed
              </>
            )}
          </button>
        </Panel>

        {/* ====================================================== */}
        {/*  2. JSON-LD Panel                                       */}
        {/* ====================================================== */}
        <Panel icon={FileJson} title="JSON-LD Structured Data" index={2}>
          {/* Tabs */}
          <div className="flex gap-1 mb-5 bg-white/[0.04] rounded-xl p-1">
            {JSONLD_TABS.map(({ key, label }) => (
              <button
                key={key}
                onClick={() => setJsonLdTab(key)}
                className={`flex-1 text-xs font-semibold py-2 rounded-lg transition-colors cursor-pointer ${
                  jsonLdTab === key
                    ? 'bg-[#00e5ff]/15 text-[#00e5ff]'
                    : 'text-[#8b95b0] hover:text-white'
                }`}
              >
                {label}
              </button>
            ))}
          </div>

          {/* Before / After comparison */}
          <div className="grid grid-cols-2 gap-3 mb-5">
            {/* Before */}
            <div>
              <div className="text-[0.65rem] font-bold uppercase tracking-wider text-red-400/80 mb-2">
                Current
              </div>
              <pre className="bg-[#0a0e1a] rounded-xl p-4 font-mono text-xs text-[#8b95b0] overflow-auto max-h-52 whitespace-pre-wrap">
                {jsonLdData?.current?.[jsonLdTab]
                  ? JSON.stringify(jsonLdData.current[jsonLdTab], null, 2)
                  : '// No existing structured data'}
              </pre>
            </div>
            {/* After */}
            <div>
              <div className="text-[0.65rem] font-bold uppercase tracking-wider text-emerald-400/80 mb-2">
                Generated
              </div>
              <pre className="bg-[#0a0e1a] rounded-xl p-4 font-mono text-xs text-[#00e5ff]/70 overflow-auto max-h-52 whitespace-pre-wrap">
                {jsonLdData?.generated?.[jsonLdTab]
                  ? JSON.stringify(jsonLdData.generated[jsonLdTab], null, 2)
                  : '// Generating...'}
              </pre>
            </div>
          </div>

          {/* Download button */}
          <button
            onClick={handleDownloadJsonLd}
            disabled={!jsonLdData}
            className="inline-flex items-center gap-2 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl px-5 py-2.5 text-sm hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            <Download size={15} />
            Download Patches
          </button>
        </Panel>

        {/* ====================================================== */}
        {/*  3. robots.txt Panel                                    */}
        {/* ====================================================== */}
        <Panel icon={Shield} title="robots.txt Scanner" index={3}>
          {/* URL input + scan */}
          <div className="flex gap-2 mb-5">
            <input
              type="url"
              value={robotsUrl}
              onChange={(e) => setRobotsUrl(e.target.value)}
              placeholder="https://example.com"
              className="flex-1 bg-[#0a0e1a] border border-white/[0.08] rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-[#8b95b0]/60 focus:outline-none focus:border-[#00e5ff]/40 transition-colors"
            />
            <button
              onClick={handleScanRobots}
              disabled={robotsScanning || !robotsUrl.trim()}
              className="inline-flex items-center gap-2 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl px-5 py-2.5 text-sm hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              {robotsScanning ? (
                <Loader2 size={15} className="animate-spin" />
              ) : (
                <Bot size={15} />
              )}
              Scan
            </button>
          </div>

          {/* Results */}
          {robotsResult && !robotsResult.error && (
            <div className="space-y-4">
              {/* Bot list */}
              <div className="space-y-2">
                <p className="text-xs font-semibold text-[#c4ccde] uppercase tracking-wider mb-2">
                  AI Bot Access
                </p>
                {robotsResult.bots?.map((bot) => (
                  <div
                    key={bot.name}
                    className="flex items-center justify-between bg-white/[0.03] border border-white/[0.05] rounded-lg px-4 py-2.5"
                  >
                    <div className="flex items-center gap-2.5">
                      <Bot size={14} className="text-[#8b95b0]" />
                      <span className="text-sm text-white font-medium">{bot.name}</span>
                    </div>
                    {bot.allowed ? (
                      <span className="inline-flex items-center gap-1 text-emerald-400 text-xs font-semibold">
                        <Check size={13} /> Allowed
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-red-400 text-xs font-semibold">
                        <X size={13} /> Blocked
                      </span>
                    )}
                  </div>
                ))}
              </div>

              {/* Recommendation text */}
              {robotsResult.recommendation && (
                <div className="bg-amber-500/8 border border-amber-500/15 rounded-xl p-4">
                  <p className="text-xs text-amber-300/90 leading-relaxed">
                    {robotsResult.recommendation}
                  </p>
                </div>
              )}

              {/* Recommended robots.txt */}
              {robotsResult.blocked_bots?.length > 0 &&
                robotsResult.recommended_robots_txt && (
                  <div>
                    <p className="text-xs font-semibold text-[#c4ccde] uppercase tracking-wider mb-2">
                      Recommended robots.txt
                    </p>
                    <pre className="bg-[#0a0e1a] rounded-xl p-4 font-mono text-xs text-[#8b95b0] overflow-auto max-h-60 whitespace-pre-wrap">
                      {robotsResult.recommended_robots_txt}
                    </pre>
                  </div>
                )}
            </div>
          )}

          {/* Error state */}
          {robotsResult?.error && (
            <div className="bg-red-500/8 border border-red-500/15 rounded-xl p-4">
              <p className="text-xs text-red-400 leading-relaxed">{robotsResult.error}</p>
            </div>
          )}

          {/* Empty state */}
          {!robotsResult && !robotsScanning && (
            <div className="text-center py-8">
              <Shield size={28} className="mx-auto text-[#8b95b0]/40 mb-3" />
              <p className="text-xs text-[#8b95b0]">
                Enter a URL above to scan its robots.txt for AI crawler policies.
              </p>
            </div>
          )}
        </Panel>

        {/* ====================================================== */}
        {/*  4. Deployment Status Panel                             */}
        {/* ====================================================== */}
        <Panel icon={Check} title="Deployment Status" index={4}>
          <div className="space-y-4">
            {[
              {
                label: 'MCP Feed',
                icon: Code2,
                status: mcpStatus,
                description: 'Structured feed for AI model consumption',
              },
              {
                label: 'JSON-LD Patches',
                icon: FileJson,
                status: jsonLdStatus,
                description: 'Organization, LocalBusiness, and FAQ schemas',
              },
              {
                label: 'robots.txt Policy',
                icon: Shield,
                status: robotsStatus,
                description: 'AI crawler access rules',
              },
            ].map(({ label, icon: Ic, status, description }) => (
              <div
                key={label}
                className="flex items-center justify-between bg-white/[0.03] border border-white/[0.05] rounded-xl px-5 py-4"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-white/[0.05] flex items-center justify-center">
                    <Ic size={16} className="text-[#00e5ff]" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">{label}</p>
                    <p className="text-[0.7rem] text-[#8b95b0]">{description}</p>
                  </div>
                </div>
                <StatusBadge status={status} />
              </div>
            ))}
          </div>

          {/* Summary bar */}
          <div className="mt-6 pt-5 border-t border-white/[0.06]">
            <div className="flex items-center justify-between">
              <span className="text-xs text-[#8b95b0]">Overall readiness</span>
              <span className="text-xs font-semibold text-white">
                {
                  [mcpStatus, jsonLdStatus, robotsStatus].filter(
                    (s) => s === 'deployed' || s === 'verified'
                  ).length
                }{' '}
                / 3 active
              </span>
            </div>
            <div className="mt-2 h-1.5 bg-white/[0.06] rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#00e5ff] to-emerald-400 rounded-full transition-all duration-500"
                style={{
                  width: `${
                    ([mcpStatus, jsonLdStatus, robotsStatus].filter(
                      (s) => s === 'deployed' || s === 'verified'
                    ).length /
                      3) *
                    100
                  }%`,
                }}
              />
            </div>
          </div>
        </Panel>
      </div>
    </div>
  )
}

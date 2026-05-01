import { useState, useEffect, useCallback, useRef } from 'react'
import { motion } from 'framer-motion'
import {
  FileJson,
  Shield,
  Copy,
  Download,
  Check,
  X,
  Loader2,
  Bot,
  FileText,
} from 'lucide-react'
import { apiFetch } from '../api/client'
import { useBrand } from '../context/BrandContext'

/* ------------------------------------------------------------------ */
/*  Fix Kit Page (Screen 4) - MCP Feed, JSON-LD, robots.txt panels    */
/* ------------------------------------------------------------------ */

/* ---------- tiny helpers ---------- */
function StatusLabel({ status }) {
  const map = {
    deployed: 'Deployed',
    pending: 'Pending',
    verified: 'Verified',
    not_deployed: 'Not deployed',
  }
  const label = map[status] || map.not_deployed
  const isActive = status === 'deployed' || status === 'verified'
  return (
    <span
      className={`text-xs font-medium ${
        isActive ? 'text-[#00e5ff]' : 'text-[#5a6480]'
      }`}
    >
      {label}
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
      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-white/[0.06] hover:bg-white/[0.1] text-[#c8ccd8] transition-colors cursor-pointer"
    >
      {copied ? <Check size={13} className="text-[#00e5ff]" /> : <Copy size={13} />}
      {copied ? 'Copied' : 'Copy URL'}
    </button>
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
  const { selectedBrandId, selectedBrand } = useBrand()
  const brandId = selectedBrandId

  /* --- shared state --- */
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  /* --- JSON-LD --- */
  const [jsonLdData, setJsonLdData] = useState(null)
  const [jsonLdTab, setJsonLdTab] = useState('organization')
  const [jsonLdStatus, setJsonLdStatus] = useState('not_deployed')

  /* --- llms.txt --- */
  const [llmsTxtData, setLlmsTxtData] = useState(null)
  const [llmsTxtTab, setLlmsTxtTab] = useState('en')
  const [llmsTxtStatus, setLlmsTxtStatus] = useState('not_deployed')

  /* --- robots.txt --- */
  const [robotsUrl, setRobotsUrl] = useState('')
  const [robotsScanning, setRobotsScanning] = useState(false)
  const [robotsResult, setRobotsResult] = useState(null)
  const [robotsStatus, setRobotsStatus] = useState('not_deployed')

  /* ---- auto-fill robots.txt URL and auto-scan ---- */
  const robotsAutoScanned = useRef(false)
  useEffect(() => {
    if (selectedBrand?.primary_url && !robotsAutoScanned.current) {
      setRobotsUrl(selectedBrand.primary_url)
    }
  }, [selectedBrand])

  // Trigger scan once URL is populated and brand is ready
  useEffect(() => {
    if (brandId && robotsUrl && !robotsAutoScanned.current && !robotsScanning && !robotsResult) {
      robotsAutoScanned.current = true
      handleScanRobots()
    }
  }, [brandId, robotsUrl])

  /* ---- fetch JSON-LD once brandId is known ---- */
  useEffect(() => {
    if (!brandId) return
    let cancelled = false

    async function fetchFeeds() {
      try {
        const [jld, llms] = await Promise.all([
          apiFetch(`/feeds/${brandId}/jsonld`).catch(() => null),
          apiFetch(`/feeds/${brandId}/llmstxt`).catch(() => null),
        ])
        if (cancelled) return
        if (jld) setJsonLdData(jld)
        if (llms) setLlmsTxtData(llms)
      } catch {
        // handled above
      }
    }
    fetchFeeds()
    return () => { cancelled = true }
  }, [brandId])

  /* ---- handlers ---- */
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

  const handleDownloadLlmsTxt = useCallback(() => {
    if (!llmsTxtData) return
    const content = llmsTxtTab === 'index' ? llmsTxtData.index : llmsTxtData[llmsTxtTab]
    if (!content) return
    const filename = llmsTxtTab === 'index' ? 'llms.txt' : `llms-${llmsTxtTab}.txt`
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
    setLlmsTxtStatus('pending')
  }, [llmsTxtData, llmsTxtTab])

  const handleCopyLlmsTxt = useCallback(() => {
    if (!llmsTxtData) return
    const content = llmsTxtTab === 'index' ? llmsTxtData.index : llmsTxtData[llmsTxtTab]
    if (content) navigator.clipboard.writeText(content)
  }, [llmsTxtData, llmsTxtTab])

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

  /* ================================================================ */
  /*  Loading / Error states                                           */
  /* ================================================================ */
  if (loading) {
    return (
      <div className="page flex items-center justify-center" style={{ minHeight: '60vh' }}>
        <Loader2 size={28} className="animate-spin text-[#00e5ff]" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="page flex items-center justify-center" style={{ minHeight: '60vh' }}>
        <p className="text-[#c8ccd8] text-sm">{error}</p>
      </div>
    )
  }

  /* ================================================================ */
  /*  Render                                                           */
  /* ================================================================ */
  return (
    <div className="page max-w-5xl">
      {/* Page header */}
      <motion.div
        className="flex items-start justify-between mb-12"
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div>
          <h1 className="text-3xl font-['Outfit'] font-bold">Fix Kit</h1>
          <p className="text-[#5a6480] text-sm mt-2">
            Deploy structured data, AI-readable summaries, and crawler policies to
            control how AI models represent your brand.
          </p>
        </div>
      </motion.div>

      {/* ========================================================== */}
      {/*  1. JSON-LD Structured Data                                 */}
      {/* ========================================================== */}
      <section className="py-10 border-t border-white/[0.04]">
        <div className="flex items-center gap-2.5 mb-6">
          <FileJson size={18} className="text-[#00e5ff]" />
          <h2 className="text-lg font-['Outfit'] font-bold">JSON-LD Structured Data</h2>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 bg-white/[0.04] rounded-xl p-1 max-w-md">
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
          {/* Current */}
          <div>
            <span className="text-[11px] font-semibold uppercase tracking-widest text-[#5a6480] mb-2 block">
              Current
            </span>
            <pre className="bg-[#0a0e1a] rounded-xl p-4 font-mono text-xs text-[#8b95b0] overflow-auto max-h-52 whitespace-pre-wrap">
              {jsonLdData?.current?.[jsonLdTab]
                ? JSON.stringify(jsonLdData.current[jsonLdTab], null, 2)
                : '// No structured data detected on your site'}
            </pre>
          </div>
          {/* Generated */}
          <div>
            <span className="text-[11px] font-semibold uppercase tracking-widest text-[#5a6480] mb-2 block">
              Generated
            </span>
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
      </section>

      {/* ========================================================== */}
      {/*  2. llms.txt — AI-Readable Brand Summary                    */}
      {/* ========================================================== */}
      <section className="py-10 border-t border-white/[0.04]">
        <div className="flex items-center gap-2.5 mb-2">
          <FileText size={18} className="text-[#00e5ff]" />
          <h2 className="text-lg font-['Outfit'] font-bold">llms.txt</h2>
        </div>
        <p className="text-sm text-[#5a6480] mb-6">
          A markdown file AI models read to understand your brand. Deploy at your domain root so
          ChatGPT, Gemini, and other assistants get your facts right.
        </p>

        {/* Language tabs */}
        <div className="flex gap-1 mb-6 bg-white/[0.04] rounded-xl p-1 max-w-xs">
          {[
            { key: 'en', label: 'English' },
            { key: 'fr', label: 'French' },
            { key: 'index', label: 'Index' },
          ].map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setLlmsTxtTab(key)}
              className={`flex-1 text-xs font-semibold py-2 rounded-lg transition-colors cursor-pointer ${
                llmsTxtTab === key
                  ? 'bg-[#00e5ff]/15 text-[#00e5ff]'
                  : 'text-[#8b95b0] hover:text-white'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Preview */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold uppercase tracking-widest text-[#5a6480]">
              {llmsTxtTab === 'index' ? 'Root /llms.txt' : llmsTxtTab === 'en' ? '/en/llms.txt' : '/fr/llms.txt'}
            </span>
            <CopyButton text={llmsTxtData?.[llmsTxtTab] || ''} />
          </div>
          <pre className="bg-[#0a0e1a] rounded-xl p-4 font-mono text-xs text-[#00e5ff]/70 overflow-auto max-h-72 whitespace-pre-wrap">
            {llmsTxtData?.[llmsTxtTab] || '// Generating...'}
          </pre>
        </div>

        {/* Where to deploy hint */}
        <div className="bg-white/[0.02] rounded-xl p-4 mb-6">
          <p className="text-xs text-[#8b95b0] leading-relaxed">
            <span className="font-semibold text-[#c8ccd8]">How to deploy:</span>{' '}
            Upload <code className="text-[#00e5ff]/70">llms.txt</code> to your domain root (e.g. <code className="text-[#00e5ff]/70">yoursite.com/llms.txt</code>).
            For bilingual sites, also place the EN and FR versions at <code className="text-[#00e5ff]/70">/en/llms.txt</code> and <code className="text-[#00e5ff]/70">/fr/llms.txt</code>.
          </p>
        </div>

        {/* Download button */}
        <button
          onClick={handleDownloadLlmsTxt}
          disabled={!llmsTxtData}
          className="inline-flex items-center gap-2 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl px-5 py-2.5 text-sm hover:brightness-110 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          <Download size={15} />
          Download {llmsTxtTab === 'index' ? 'llms.txt' : `llms-${llmsTxtTab}.txt`}
        </button>
      </section>

      {/* ========================================================== */}
      {/*  3. robots.txt Scanner                                      */}
      {/* ========================================================== */}
      <section className="py-10 border-t border-white/[0.04]">
        <div className="flex items-center gap-2.5 mb-2">
          <Shield size={18} className="text-[#00e5ff]" />
          <h2 className="text-lg font-['Outfit'] font-bold">robots.txt Scanner</h2>
        </div>
        <p className="text-sm text-[#5a6480] mb-6">
          Check whether your site allows or blocks AI crawlers like GPTBot, Google-Extended, and others.
        </p>

        {/* URL input + scan */}
        <div className="flex gap-2 mb-6 max-w-xl">
          <input
            type="url"
            value={robotsUrl}
            onChange={(e) => setRobotsUrl(e.target.value)}
            placeholder="https://example.com"
            className="flex-1 bg-[#0a0e1a] border border-white/[0.08] rounded-xl px-4 py-2.5 text-sm text-white placeholder:text-[#5a6480] focus:outline-none focus:border-[#00e5ff]/40 transition-colors"
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
          <div className="space-y-6">
            {/* Bot list */}
            <div>
              <span className="text-[11px] font-semibold text-[#5a6480] uppercase tracking-widest mb-3 block">
                AI Bot Access
              </span>
              <div className="divide-y divide-white/[0.04]">
                {robotsResult.bots?.map((bot) => (
                  <div
                    key={bot.name}
                    className="flex items-center justify-between py-3"
                  >
                    <div className="flex items-center gap-2.5">
                      <Bot size={14} className="text-[#5a6480]" />
                      <span className="text-sm text-[#f0f2f8] font-medium">{bot.name}</span>
                    </div>
                    {bot.allowed ? (
                      <span className="inline-flex items-center gap-1.5 text-[#00e5ff] text-xs font-medium">
                        <Check size={13} /> Allowed
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 text-[#ff4c6a] text-xs font-medium">
                        <X size={13} /> Blocked
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendation text */}
            {robotsResult.recommendation && (
              <p className="text-sm text-[#8b95b0] leading-relaxed">
                {robotsResult.recommendation}
              </p>
            )}

            {/* Recommended robots.txt */}
            {robotsResult.blocked_bots?.length > 0 &&
              robotsResult.recommended_robots_txt && (
                <div>
                  <span className="text-[11px] font-semibold text-[#5a6480] uppercase tracking-widest mb-2 block">
                    Recommended robots.txt
                  </span>
                  <pre className="bg-[#0a0e1a] rounded-xl p-4 font-mono text-xs text-[#8b95b0] overflow-auto max-h-60 whitespace-pre-wrap">
                    {robotsResult.recommended_robots_txt}
                  </pre>
                </div>
              )}
          </div>
        )}

        {/* Error state */}
        {robotsResult?.error && (
          <p className="text-sm text-[#ff4c6a]">{robotsResult.error}</p>
        )}

        {/* Empty state -- minimal, no big icon/card */}
        {!robotsResult && !robotsScanning && (
          <p className="text-sm text-[#5a6480]">
            Enter your site URL and scan to see which AI crawlers are allowed or blocked.
          </p>
        )}
      </section>

      {/* ========================================================== */}
      {/*  4. Deployment Status -- simple inline list                 */}
      {/* ========================================================== */}
      <section className="py-10 border-t border-white/[0.04]">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-base font-['Outfit'] font-semibold text-[#8b95b0] uppercase tracking-wider">
            Deployment Status
          </h3>
          <span className="text-xs text-[#5a6480]">
            {
              [jsonLdStatus, llmsTxtStatus, robotsStatus].filter(
                (s) => s === 'deployed' || s === 'verified'
              ).length
            }{' '}
            / 3 active
          </span>
        </div>

        <div className="divide-y divide-white/[0.04]">
          {[
            {
              label: 'JSON-LD Patches',
              icon: FileJson,
              status: jsonLdStatus,
              description: 'Organization, LocalBusiness, and FAQ schemas',
            },
            {
              label: 'llms.txt',
              icon: FileText,
              status: llmsTxtStatus,
              description: 'AI-readable brand summary (EN/FR)',
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
              className="flex items-center justify-between py-4"
            >
              <div className="flex items-center gap-3">
                <Ic size={16} className="text-[#5a6480]" />
                <div>
                  <p className="text-sm font-medium text-[#f0f2f8]">{label}</p>
                  <p className="text-xs text-[#5a6480]">{description}</p>
                </div>
              </div>
              <StatusLabel status={status} />
            </div>
          ))}
        </div>

        {/* Progress bar */}
        <div className="mt-6">
          <div className="h-1.5 bg-white/[0.04] rounded-full overflow-hidden">
            <div
              className="h-full bg-[#00e5ff] rounded-full transition-all duration-500"
              style={{
                width: `${
                  ([jsonLdStatus, llmsTxtStatus, robotsStatus].filter(
                    (s) => s === 'deployed' || s === 'verified'
                  ).length /
                    3) *
                  100
                }%`,
              }}
            />
          </div>
        </div>
      </section>
    </div>
  )
}

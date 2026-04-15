import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  AlertTriangle,
  Target,
  Globe,
  Gift,
  Users,
  Mail,
  Copy,
  Check,
  Loader2,
  Send,
  Linkedin,
  ChevronRight,
} from 'lucide-react'
import { apiFetch } from '../api/client'
import { useBrand } from '../context/BrandContext'

/* ─── Constants ─── */
const SEQUENCE_ICONS = {
  scary_report: AlertTriangle,
  competitor_advantage: Target,
  french_gap: Globe,
  free_audit: Gift,
  design_partner: Users,
}

const SEQUENCE_DEFAULTS = [
  { id: 'scary_report', name: 'Scary Report', description: 'Lead with alarming audit findings to create urgency', icon: 'scary_report' },
  { id: 'competitor_advantage', name: 'Competitor Advantage', description: 'Show how competitors outperform them in AI visibility', icon: 'competitor_advantage' },
  { id: 'french_gap', name: 'French Gap', description: 'Highlight missing French-language AI optimization', icon: 'french_gap' },
  { id: 'free_audit', name: 'Free Audit', description: 'Offer a complimentary AI visibility audit as hook', icon: 'free_audit' },
  { id: 'design_partner', name: 'Design Partner', description: 'Invite them to co-build the product as early partner', icon: 'design_partner' },
]

const GRADE_COLORS = { RED: '#ff4c6a', YELLOW: '#ffb547', GREEN: '#34d399' }

const TAB_LABELS = ['Email 1', 'Email 2', 'Email 3', 'LinkedIn']

/* ─── Helpers ─── */
function GlassInput({ label, value, onChange, placeholder }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-[#8b95b0] uppercase tracking-wider">{label}</label>
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-xl px-4 py-2.5 text-sm text-[#f0f2f8] placeholder-[#5a6480] outline-none focus:border-[#00e5ff]/40 transition-colors"
      />
    </div>
  )
}

function SequenceCard({ seq, selected, onSelect }) {
  const Icon = SEQUENCE_ICONS[seq.icon || seq.id] || Mail
  const isActive = selected === seq.id

  return (
    <button
      onClick={() => onSelect(seq.id)}
      className={`w-full text-left bg-white/[0.03] backdrop-blur-xl border rounded-xl p-3.5 transition-all cursor-pointer ${
        isActive
          ? 'border-[#00e5ff]/50 shadow-[0_0_20px_rgba(0,229,255,0.12)]'
          : 'border-white/[0.06] hover:border-white/[0.12]'
      }`}
    >
      <div className="flex items-center gap-3">
        <div
          className={`w-8 h-8 rounded-lg flex items-center justify-center ${
            isActive ? 'bg-[#00e5ff]/10' : 'bg-white/[0.04]'
          }`}
        >
          <Icon size={15} className={isActive ? 'text-[#00e5ff]' : 'text-[#8b95b0]'} />
        </div>
        <div className="flex-1 min-w-0">
          <div className={`text-sm font-medium ${isActive ? 'text-[#00e5ff]' : 'text-[#f0f2f8]'}`}>
            {seq.name}
          </div>
          <div className="text-xs text-[#5a6480] truncate">{seq.description}</div>
        </div>
        {isActive && <ChevronRight size={14} className="text-[#00e5ff] flex-shrink-0" />}
      </div>
    </button>
  )
}

function CopyButton({ text, copiedKey, copiedState, onCopy }) {
  const isCopied = copiedState === copiedKey

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      onCopy(copiedKey)
    } catch {
      // fallback
      const ta = document.createElement('textarea')
      ta.value = text
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
      onCopy(copiedKey)
    }
  }

  return (
    <button
      onClick={handleCopy}
      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
        isCopied
          ? 'bg-[#34d399]/10 text-[#34d399]'
          : 'bg-white/[0.04] text-[#8b95b0] hover:bg-white/[0.08] hover:text-[#f0f2f8]'
      }`}
    >
      {isCopied ? <Check size={12} /> : <Copy size={12} />}
      {isCopied ? 'Copied!' : 'Copy'}
    </button>
  )
}

/* ─── Main Page ─── */
export default function Outreach() {
  const { selectedBrand: ctxBrand, availableBrands } = useBrand()
  const [sequences, setSequences] = useState(SEQUENCE_DEFAULTS)
  const [selectedSequence, setSelectedSequence] = useState('scary_report')
  const [formData, setFormData] = useState({ target_name: '', target_title: '', target_company: '' })
  const [generated, setGenerated] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(null)
  const [activeTab, setActiveTab] = useState(0)
  const selectedBrand = ctxBrand || availableBrands[0] || null

  /* ─── Fetch sequences when brand changes ─── */
  useEffect(() => {
    if (!selectedBrand?.id) return
    let cancelled = false
    async function loadSequences() {
      try {
        const data = await apiFetch(`/outreach/${selectedBrand.id}/sequences`)
        if (cancelled) return
        const list = Array.isArray(data) ? data : data?.sequences || []
        if (list.length > 0) {
          setSequences(list)
          if (!list.find(s => s.id === selectedSequence)) {
            setSelectedSequence(list[0].id)
          }
        }
      } catch {
        // Keep defaults on failure
      }
    }
    loadSequences()
    return () => { cancelled = true }
  }, [selectedBrand])

  /* ─── Copy feedback timer ─── */
  const handleCopy = useCallback((key) => {
    setCopied(key)
    setTimeout(() => setCopied(null), 2000)
  }, [])

  /* ─── Generate outreach ─── */
  const handleGenerate = async () => {
    if (!selectedBrand?.id) {
      setError('No brand selected.')
      return
    }
    if (!formData.target_name || !formData.target_company) {
      setError('Please fill in at least the target name and company.')
      return
    }

    setLoading(true)
    setError(null)
    setGenerated(null)
    setActiveTab(0)

    try {
      const result = await apiFetch(`/outreach/${selectedBrand.id}/generate`, {
        method: 'POST',
        body: JSON.stringify({
          sequence_id: selectedSequence,
          target_name: formData.target_name,
          target_title: formData.target_title,
          target_company: formData.target_company,
        }),
      })
      setGenerated(result)
    } catch (err) {
      setError(err.message || 'Failed to generate outreach.')
    } finally {
      setLoading(false)
    }
  }

  /* ─── Derived data from generated result ─── */
  const emails = generated?.emails || []
  const linkedin = generated?.linkedin || {}
  const audit = generated?.audit_data_used || {}

  const gradeColor = GRADE_COLORS[audit.grade] || '#00e5ff'

  return (
    <div className="min-h-screen bg-[#0a0e1a] p-6 lg:p-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-['Outfit'] font-bold text-[#f0f2f8] flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#00e5ff]/10 flex items-center justify-center">
            <Send size={20} className="text-[#00e5ff]" />
          </div>
          Outreach Studio
        </h1>
        <p className="text-sm text-[#8b95b0] mt-1 ml-[52px]">
          Generate personalized cold emails and LinkedIn messages from AI audit data
        </p>
      </div>

      {/* Two-column layout */}
      <div className="flex flex-col lg:flex-row gap-6">
        {/* ─── Left column: Configuration ─── */}
        <div className="w-full lg:w-1/3 flex flex-col gap-5">
          {/* Brand selector */}
          {availableBrands.length > 1 && (
            <div className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-5">
              <label className="text-xs font-medium text-[#8b95b0] uppercase tracking-wider mb-2 block">
                Brand
              </label>
              <p className="text-xs text-[#5a6480]">Switch brands from the header dropdown</p>
            </div>
          )}

          {/* Sequence selector */}
          <div className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-5">
            <label className="text-xs font-medium text-[#8b95b0] uppercase tracking-wider mb-3 block">
              Outreach Sequence
            </label>
            <div className="flex flex-col gap-2">
              {sequences.map(seq => (
                <SequenceCard
                  key={seq.id}
                  seq={seq}
                  selected={selectedSequence}
                  onSelect={setSelectedSequence}
                />
              ))}
            </div>
          </div>

          {/* Target info form */}
          <div className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-5">
            <label className="text-xs font-medium text-[#8b95b0] uppercase tracking-wider mb-3 block">
              Target Details
            </label>
            <div className="flex flex-col gap-3">
              <GlassInput
                label="Name"
                value={formData.target_name}
                onChange={(e) => setFormData(prev => ({ ...prev, target_name: e.target.value }))}
                placeholder="e.g. Sarah Chen"
              />
              <GlassInput
                label="Title"
                value={formData.target_title}
                onChange={(e) => setFormData(prev => ({ ...prev, target_title: e.target.value }))}
                placeholder="e.g. Head of Marketing"
              />
              <GlassInput
                label="Company"
                value={formData.target_company}
                onChange={(e) => setFormData(prev => ({ ...prev, target_company: e.target.value }))}
                placeholder="e.g. Acme Corp"
              />
            </div>
          </div>

          {/* Generate button */}
          <button
            onClick={handleGenerate}
            disabled={loading}
            className={`w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium text-sm transition-all ${
              loading
                ? 'bg-[#00e5ff]/20 text-[#00e5ff]/50 cursor-not-allowed'
                : 'bg-[#00e5ff] text-[#0a0e1a] hover:bg-[#00e5ff]/90 hover:shadow-[0_0_30px_rgba(0,229,255,0.25)] cursor-pointer'
            }`}
          >
            {loading ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Send size={16} />
                Generate Outreach
              </>
            )}
          </button>

          {/* Error message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-[#ff4c6a]/10 border border-[#ff4c6a]/20 rounded-xl px-4 py-3 text-sm text-[#ff4c6a]"
            >
              {error}
            </motion.div>
          )}
        </div>

        {/* ─── Right column: Output ─── */}
        <div className="w-full lg:w-2/3">
          <AnimatePresence mode="wait">
            {!generated && !loading ? (
              /* Empty state */
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl flex flex-col items-center justify-center py-32"
              >
                <div className="w-20 h-20 rounded-2xl bg-[#00e5ff]/[0.06] flex items-center justify-center mb-6 shadow-[0_0_40px_rgba(0,229,255,0.1)]">
                  <Mail size={36} className="text-[#00e5ff]" />
                </div>
                <p className="text-[#f0f2f8] font-medium text-lg mb-2">
                  Select a sequence and fill in the target details
                </p>
                <p className="text-[#5a6480] text-sm">
                  Your personalized outreach will appear here
                </p>
              </motion.div>
            ) : loading ? (
              /* Loading state */
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl flex flex-col items-center justify-center py-32"
              >
                <Loader2 size={40} className="text-[#00e5ff] animate-spin mb-4" />
                <p className="text-[#8b95b0] text-sm">Crafting personalized outreach...</p>
              </motion.div>
            ) : (
              /* Generated state */
              <motion.div
                key="generated"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.4, ease: 'easeOut' }}
                className="flex flex-col gap-5"
              >
                {/* Audit data badges */}
                {(audit.ias_score != null || audit.grade || audit.fr_visibility_gap != null) && (
                  <div className="flex flex-wrap items-center gap-3">
                    {audit.ias_score != null && (
                      <div
                        className="flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold"
                        style={{
                          backgroundColor: `${gradeColor}10`,
                          color: gradeColor,
                          border: `1px solid ${gradeColor}25`,
                        }}
                      >
                        IAS Score: {audit.ias_score}
                      </div>
                    )}
                    {audit.grade && (
                      <div
                        className="flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold"
                        style={{
                          backgroundColor: `${gradeColor}10`,
                          color: gradeColor,
                          border: `1px solid ${gradeColor}25`,
                        }}
                      >
                        Grade: {audit.grade}
                      </div>
                    )}
                    {audit.fr_visibility_gap != null && (
                      <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-[#9b8aff]/10 text-[#9b8aff] border border-[#9b8aff]/25">
                        <Globe size={12} />
                        FR Gap: {typeof audit.fr_visibility_gap === 'number' ? `${audit.fr_visibility_gap}%` : audit.fr_visibility_gap}
                      </div>
                    )}
                  </div>
                )}

                {/* Tab bar */}
                <div className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl overflow-hidden">
                  <div className="flex border-b border-white/[0.06]">
                    {TAB_LABELS.map((label, idx) => {
                      const isEmail = idx < 3
                      const hasContent = isEmail ? emails[idx] : (linkedin.connection_request || linkedin.follow_up_message)
                      return (
                        <button
                          key={label}
                          onClick={() => setActiveTab(idx)}
                          disabled={!hasContent}
                          className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium transition-all ${
                            activeTab === idx
                              ? 'text-[#00e5ff] border-b-2 border-[#00e5ff] bg-[#00e5ff]/[0.04]'
                              : hasContent
                                ? 'text-[#8b95b0] hover:text-[#f0f2f8] hover:bg-white/[0.02] cursor-pointer'
                                : 'text-[#5a6480]/40 cursor-not-allowed'
                          }`}
                        >
                          {idx === 3 ? <Linkedin size={14} /> : <Mail size={14} />}
                          {label}
                        </button>
                      )
                    })}
                  </div>

                  {/* Tab content */}
                  <div className="p-6">
                    <AnimatePresence mode="wait">
                      {activeTab < 3 ? (
                        /* Email tab */
                        <motion.div
                          key={`email-${activeTab}`}
                          initial={{ opacity: 0, y: 12 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -12 }}
                          transition={{ duration: 0.25 }}
                        >
                          {emails[activeTab] ? (
                            <div className="flex flex-col gap-4">
                              {/* Send day */}
                              {emails[activeTab].send_day != null && (
                                <div className="flex items-center gap-2 text-xs text-[#8b95b0]">
                                  <div className="w-5 h-5 rounded-md bg-[#ffb547]/10 flex items-center justify-center">
                                    <span className="text-[10px] font-bold text-[#ffb547]">
                                      D{emails[activeTab].send_day}
                                    </span>
                                  </div>
                                  Send on day {emails[activeTab].send_day}
                                </div>
                              )}

                              {/* Subject line */}
                              {emails[activeTab].subject && (
                                <div className="bg-[#00e5ff]/[0.04] border border-[#00e5ff]/10 rounded-xl px-4 py-3">
                                  <div className="flex items-center justify-between">
                                    <div>
                                      <span className="text-[10px] uppercase tracking-wider text-[#00e5ff] font-semibold">
                                        Subject
                                      </span>
                                      <p className="text-sm text-[#f0f2f8] mt-0.5 font-medium">
                                        {emails[activeTab].subject}
                                      </p>
                                    </div>
                                    <CopyButton
                                      text={emails[activeTab].subject}
                                      copiedKey={`subject-${activeTab}`}
                                      copiedState={copied}
                                      onCopy={handleCopy}
                                    />
                                  </div>
                                </div>
                              )}

                              {/* Body */}
                              {emails[activeTab].body && (
                                <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-5">
                                  <div className="flex items-center justify-between mb-3">
                                    <span className="text-[10px] uppercase tracking-wider text-[#8b95b0] font-semibold">
                                      Body
                                    </span>
                                    <CopyButton
                                      text={emails[activeTab].body}
                                      copiedKey={`body-${activeTab}`}
                                      copiedState={copied}
                                      onCopy={handleCopy}
                                    />
                                  </div>
                                  <p className="text-sm text-[#f0f2f8] leading-relaxed whitespace-pre-wrap">
                                    {emails[activeTab].body}
                                  </p>
                                </div>
                              )}
                            </div>
                          ) : (
                            <div className="text-center py-12 text-[#5a6480] text-sm">
                              No content generated for this email step.
                            </div>
                          )}
                        </motion.div>
                      ) : (
                        /* LinkedIn tab */
                        <motion.div
                          key="linkedin"
                          initial={{ opacity: 0, y: 12 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -12 }}
                          transition={{ duration: 0.25 }}
                          className="flex flex-col gap-5"
                        >
                          {/* Connection request */}
                          {linkedin.connection_request && (
                            <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-5">
                              <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-2">
                                  <Linkedin size={14} className="text-[#0A66C2]" />
                                  <span className="text-[10px] uppercase tracking-wider text-[#8b95b0] font-semibold">
                                    Connection Request
                                  </span>
                                </div>
                                <CopyButton
                                  text={linkedin.connection_request}
                                  copiedKey="linkedin-cr"
                                  copiedState={copied}
                                  onCopy={handleCopy}
                                />
                              </div>
                              <p className="text-sm text-[#f0f2f8] leading-relaxed whitespace-pre-wrap">
                                {linkedin.connection_request}
                              </p>
                              <div className="mt-3 flex items-center gap-2">
                                <div
                                  className="h-1 rounded-full flex-1 bg-white/[0.06] overflow-hidden"
                                >
                                  <div
                                    className="h-full rounded-full transition-all"
                                    style={{
                                      width: `${Math.min((linkedin.connection_request.length / 300) * 100, 100)}%`,
                                      backgroundColor:
                                        linkedin.connection_request.length > 300 ? '#ff4c6a' : '#00e5ff',
                                    }}
                                  />
                                </div>
                                <span
                                  className={`text-xs font-mono ${
                                    linkedin.connection_request.length > 300
                                      ? 'text-[#ff4c6a]'
                                      : 'text-[#8b95b0]'
                                  }`}
                                >
                                  {linkedin.connection_request.length}/300
                                </span>
                              </div>
                            </div>
                          )}

                          {/* Follow-up message */}
                          {linkedin.follow_up_message && (
                            <div className="bg-white/[0.02] border border-white/[0.06] rounded-xl p-5">
                              <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-2">
                                  <Linkedin size={14} className="text-[#0A66C2]" />
                                  <span className="text-[10px] uppercase tracking-wider text-[#8b95b0] font-semibold">
                                    Follow-up Message
                                  </span>
                                </div>
                                <CopyButton
                                  text={linkedin.follow_up_message}
                                  copiedKey="linkedin-fu"
                                  copiedState={copied}
                                  onCopy={handleCopy}
                                />
                              </div>
                              <p className="text-sm text-[#f0f2f8] leading-relaxed whitespace-pre-wrap">
                                {linkedin.follow_up_message}
                              </p>
                            </div>
                          )}

                          {!linkedin.connection_request && !linkedin.follow_up_message && (
                            <div className="text-center py-12 text-[#5a6480] text-sm">
                              No LinkedIn content generated.
                            </div>
                          )}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}

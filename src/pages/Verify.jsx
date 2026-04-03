import { useState, useEffect } from 'react'
import api from '../api/client'
import { Calendar, Clock, CheckCircle, XCircle, AlertCircle, ChevronDown, ChevronUp, MessageSquare, Zap, Languages, Target, Eye, Timer, FlaskConical } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { useLanguage } from '../context/LanguageContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import AnimatedCounter from '../components/AnimatedCounter'
import {
  auditSchedule, auditTimeline, confidenceShift, sideBySideReasoning,
  evaluationRubric, remediationEfficiency, tokenFertility,
} from '../data/mockData'
import './Verify.css'

const statusIcons = {
  passed: CheckCircle,
  failed: XCircle,
  warning: AlertCircle,
  pending: Clock,
  info: AlertCircle,
  scheduled: Calendar,
}

const rubricIcons = {
  semanticAlignment: Target,
  temporalAccuracy: Timer,
  linguisticDensity: Languages,
  discoverability: Eye,
}

const rubricColors = {
  semanticAlignment: 'cyan',
  temporalAccuracy: 'green',
  linguisticDensity: 'lavender',
  discoverability: 'amber',
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload) return null
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-label">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="chart-tooltip-row">
          <span style={{ color: p.color }}>●</span>
          <span>{p.name}: {p.value !== null ? `${p.value}%` : 'Pending'}</span>
        </div>
      ))}
    </div>
  )
}

/* Circular progress ring for rubric metrics */
function RubricGauge({ value, max = 10, size = 64, color = 'var(--cyan)' }) {
  const radius = (size - 8) / 2
  const circumference = 2 * Math.PI * radius
  const pct = Math.min(value / max, 1)
  const offset = circumference - pct * circumference

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="rubric-gauge">
      <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
        stroke="rgba(255,255,255,0.06)" strokeWidth="4" />
      <circle cx={size / 2} cy={size / 2} r={radius} fill="none"
        stroke={color} strokeWidth="4" strokeLinecap="round"
        strokeDasharray={circumference} strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.16,1,0.3,1)' }} />
      <text x="50%" y="50%" textAnchor="middle" dominantBaseline="central"
        fill="var(--text-primary)" fontSize="14" fontWeight="800" fontFamily="var(--font-heading)">
        {typeof value === 'number' && value < 100 ? value.toFixed(1) : value}
      </text>
    </svg>
  )
}

/* Bilateral fertility bar */
function FertilityBar({ lang, pre, post }) {
  const maxFertility = 3.0
  const preWidth = Math.min((pre.fertility / maxFertility) * 100, 100)
  const postWidth = Math.min((post.fertility / maxFertility) * 100, 100)

  const severityColors = {
    healthy: 'var(--green)',
    warning: 'var(--amber)',
    degraded: 'var(--coral)',
    critical: 'var(--coral)',
  }

  return (
    <div className="fertility-bar-group">
      <div className="fertility-bar-label">{lang.toUpperCase()}</div>
      <div className="fertility-bar-rows">
        <div className="fertility-bar-row">
          <span className="fertility-bar-tag fertility-pre">PRE</span>
          <div className="fertility-bar-track">
            <div className="fertility-bar-fill"
              style={{ width: `${preWidth}%`, background: severityColors[pre.severity] }} />
          </div>
          <span className="fertility-bar-value" style={{ color: severityColors[pre.severity] }}>
            {pre.fertility}×
          </span>
        </div>
        <div className="fertility-bar-row">
          <span className="fertility-bar-tag fertility-post">POST</span>
          <div className="fertility-bar-track">
            <div className="fertility-bar-fill"
              style={{ width: `${postWidth}%`, background: severityColors[post.severity] }} />
          </div>
          <span className="fertility-bar-value" style={{ color: severityColors[post.severity] }}>
            {post.fertility}×
          </span>
        </div>
      </div>
    </div>
  )
}

export default function Verify() {
  const { t } = useLanguage()
  const [expandedReasoning, setExpandedReasoning] = useState(null)
  const [deepDiveOpen, setDeepDiveOpen] = useState(false)

  // State initialized with mockData, overwritten by API
  const [schedule, setSchedule] = useState(auditSchedule)
  const [timeline, setTimeline] = useState(auditTimeline)
  const [confidence, setConfidence] = useState(confidenceShift)
  const [reasoning, setReasoning] = useState(sideBySideReasoning)
  const [efficiency, setEfficiency] = useState({
    ...remediationEfficiency,
    sIn: 3.2, sOut: 8.5, delta: 0.15, eScore: 2.26
  })
  const [fertility, setFertility] = useState(tokenFertility)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [sched, time, conf, reas, eff] = await Promise.all([
          api.verify.schedule(),
          api.verify.timeline(),
          api.verify.confidence(),
          api.verify.reasoning(),
          api.verify.efficiency()
        ])
        
        if (sched && sched.length > 0) setSchedule(sched)
        if (time && time.length > 0) setTimeline(time)
        if (conf && conf.length > 0) setConfidence(conf)
        if (reas && reas.length > 0) {
          setReasoning(reas)
          if (reas.length > 0) setExpandedReasoning(reas[0].id)
        }
        if (eff) {
          setEfficiency(prev => ({
            ...prev,
            sIn: eff.s_in,
            sOut: eff.s_out,
            delta: eff.delta,
            eScore: eff.e_score
          }))
          setFertility(prev => ({
            ...prev,
            postFix: {
              en: { fertility: eff.en_fertility, severity: eff.en_fertility > 1.2 ? 'warning' : 'healthy' },
              fr: { fertility: eff.fr_fertility, severity: eff.fr_fertility > 1.2 ? 'warning' : 'healthy' }
            }
          }))
        }
      } catch (err) {
        console.error("Failed to fetch verify data:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const { sIn, sOut, delta, eScore, trend: eTrend, history: eHistory } = efficiency

  if (loading) return <div className="page" style={{ padding: '2rem' }}>Loading Verification...</div>

  return (
    <div className="page">
      <div className="page-header fade-in-up">
        <h1>{t('verifyTitle')}</h1>
        <p>{t('verifySubtitle')}</p>
      </div>

      {/* ═══════════════ HERO ROW: E Score + Token Fertility ═══════════════ */}
      <div className="verify-hero fade-in-up fade-in-up-delay-1">
        {/* Remediation Efficiency — THE number */}
        <GlassCard className="e-score-card" glow="cyan">
          <div className="e-score-top">
            <div className="e-score-icon">
              <Zap size={22} />
            </div>
            <div className="e-score-trend">
              <span className={`e-trend-badge ${eTrend > 0 ? 'trend-up' : 'trend-down'}`}>
                {eTrend > 0 ? '+' : ''}{eTrend}%
              </span>
            </div>
          </div>
          <div className="e-score-value">
            <span className="animated-counter" style={{ animation: 'countUp 0.8s ease both' }}>{eScore}</span>
          </div>
          <div className="e-score-label">{t('remediationEfficiency')}</div>
          <div className="e-score-formula">
            E = (S<sub>out</sub> / S<sub>in</sub>) · (1 − δ)
          </div>
          <div className="e-score-breakdown">
            <div className="e-param">
              <span className="e-param-label">S<sub>in</sub></span>
              <span className="e-param-value">{sIn}</span>
            </div>
            <div className="e-param-arrow">→</div>
            <div className="e-param">
              <span className="e-param-label">S<sub>out</sub></span>
              <span className="e-param-value e-param-highlight">{sOut}</span>
            </div>
            <div className="e-param-divider" />
            <div className="e-param">
              <span className="e-param-label">δ</span>
              <span className="e-param-value">{delta}</span>
            </div>
          </div>
        </GlassCard>

        {/* Token Fertility Gauge */}
        <GlassCard className="fertility-card">
          <div className="fertility-header">
            <div className="fertility-header-left">
              <Languages size={16} style={{ color: 'var(--lavender)' }} />
              <h3>{t('tokenFertilityTitle')}</h3>
            </div>
            <div className="fertility-improvement">
              <span className="badge badge-success">↓ {tokenFertility.improvementPct}% decay</span>
            </div>
          </div>
          <p className="fertility-desc">{t('tokenFertilityDesc')}</p>

          <div className="fertility-bars">
            <FertilityBar lang="en" pre={fertility.preFix.en} post={fertility.postFix.en} />
            <FertilityBar lang="fr" pre={fertility.preFix.fr} post={fertility.postFix.fr} />
          </div>

          <div className="fertility-legend">
            <span className="fertility-legend-item">
              <span className="fertility-legend-dot fertility-pre" />
              {t('preFix')}
            </span>
            <span className="fertility-legend-item">
              <span className="fertility-legend-dot fertility-post" />
              {t('postFix')}
            </span>
          </div>
        </GlassCard>
      </div>

      {/* ═══════════════ TECHNICAL DEEP DIVE (Collapsible) ═══════════════ */}
      <div className="deep-dive-section fade-in-up fade-in-up-delay-2">
        <button className="deep-dive-toggle" onClick={() => setDeepDiveOpen(!deepDiveOpen)}>
          <div className="deep-dive-toggle-left">
            <FlaskConical size={16} style={{ color: 'var(--cyan)' }} />
            <span className="deep-dive-toggle-label">{t('technicalDeepDive')}</span>
            <span className="deep-dive-toggle-sub">{t('evaluationRubric')}</span>
          </div>
          {deepDiveOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>

        {deepDiveOpen && (
          <div className="deep-dive-body">
            {/* Rubric Cards */}
            <div className="rubric-grid">
              {Object.entries(evaluationRubric).map(([key, metric], i) => {
                const Icon = rubricIcons[key]
                const color = rubricColors[key]
                const colorVar = `var(--${color})`
                const isTimeMetric = key === 'temporalAccuracy'
                const pctOfTarget = isTimeMetric
                  ? Math.min(((metric.target - metric.current) / metric.target) * 10, 10)
                  : metric.current

                return (
                  <div key={key} className={`rubric-card rubric-${color}`}
                    style={{ animationDelay: `${0.1 * i}s` }}>
                    <div className="rubric-card-top">
                      <div className={`rubric-card-icon icon-${color}`}>
                        <Icon size={16} />
                      </div>
                      <RubricGauge
                        value={isTimeMetric ? pctOfTarget : metric.current}
                        max={10}
                        size={56}
                        color={colorVar}
                      />
                    </div>
                    <div className="rubric-card-label">{t(key)}</div>
                    <div className="rubric-card-desc">{metric.description}</div>

                    <div className="rubric-card-stats">
                      <div className="rubric-stat">
                        <span className="rubric-stat-label">{t('current')}</span>
                        <span className="rubric-stat-value" style={{ color: colorVar }}>
                          {isTimeMetric ? `${metric.current}s` : `${metric.current}${metric.unit}`}
                        </span>
                      </div>
                      <div className="rubric-stat">
                        <span className="rubric-stat-label">{t('the9Standard')}</span>
                        <span className="rubric-stat-value">{metric.standard}</span>
                      </div>
                    </div>

                    {!isTimeMetric && (
                      <div className="rubric-card-bar">
                        <div className="rubric-bar-track">
                          <div className="rubric-bar-before"
                            style={{ width: `${(metric.before / 10) * 100}%` }} />
                          <div className="rubric-bar-current"
                            style={{ width: `${(metric.current / 10) * 100}%`, background: colorVar }} />
                        </div>
                        <div className="rubric-bar-labels">
                          <span>Before: {metric.before}{metric.unit}</span>
                          <span>Now: {metric.current}{metric.unit}</span>
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>

            {/* Formula Proof Block */}
            <GlassCard className="formula-proof">
              <div className="formula-proof-header">
                <h4>Remediation Efficiency Proof</h4>
                <span className="badge badge-cyan">Live</span>
              </div>
              <div className="formula-proof-body">
                <div className="formula-rendered">
                  E = (<span className="formula-val formula-sout">{sOut}</span> / <span className="formula-val formula-sin">{sIn}</span>) · (1 − <span className="formula-val formula-delta">{delta}</span>) = <span className="formula-val formula-result">{eScore}</span>
                </div>
                <div className="formula-interpretation">
                  <p>
                    Your remediation layer has a <strong>{eScore}× semantic multiplier</strong>.
                    For every unit of raw PIM data quality going in, you're outputting {eScore}× the semantic clarity —
                    even after accounting for a {(delta * 100).toFixed(0)}% Token Decay penalty from French technical term fragmentation.
                  </p>
                </div>
              </div>
            </GlassCard>
          </div>
        )}
      </div>

      {/* ═══════════════ EXISTING VERIFY LAYOUT ═══════════════ */}
      <div className="verify-layout">
        {/* Left column: Audit Schedule + Timeline */}
        <div className="verify-left">
          {/* Auto-Audit Schedule */}
          <GlassCard className="fade-in-up fade-in-up-delay-1">
            <div className="verify-section-header">
              <h3>
                <Calendar size={16} style={{ color: 'var(--lavender)' }} />
                {' '}{t('autoAudit')}
              </h3>
              <button className="btn btn-primary btn-sm">{t('scheduleAudit')}</button>
            </div>
            <div className="schedule-cards">
              {schedule.map((s) => (
                <div key={s.day} className="schedule-card">
                  <div className="schedule-day">{t('day')} {s.day}</div>
                  <div className="schedule-date">{s.date}</div>
                  <StatusBadge status={s.status} label={s.label} />
                </div>
              ))}
            </div>
          </GlassCard>

          {/* Audit Timeline */}
          <GlassCard className="fade-in-up fade-in-up-delay-2">
            <h3 style={{ marginBottom: 'var(--space-xl)', fontSize: '0.95rem' }}>
              <Clock size={16} style={{ color: 'var(--cyan)' }} />
              {' '}{t('auditTimeline')}
            </h3>
            <div className="timeline">
              {timeline.map((event, i) => {
                const Icon = statusIcons[event.status] || Clock
                return (
                  <div key={event.id} className={`timeline-item timeline-${event.status}`}>
                    <div className="timeline-line-wrap">
                      <div className={`timeline-dot dot-${event.status}`}>
                        <Icon size={12} />
                      </div>
                      {i < timeline.length - 1 && <div className="timeline-line" />}
                    </div>
                    <div className="timeline-content">
                      <div className="timeline-date">{event.date}</div>
                      <div className="timeline-label">{event.label}</div>
                      <p className="timeline-detail">{event.detail}</p>
                      {event.score !== null && (
                        <div className={`timeline-score ${event.score >= 70 ? 'score-good' : event.score >= 40 ? 'score-mid' : 'score-bad'}`}>
                          Score: {event.score}%
                        </div>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          </GlassCard>
        </div>

        {/* Right column: Chart + Side-by-Side */}
        <div className="verify-right">
          {/* Confidence Shift Chart */}
          <GlassCard className="fade-in-up fade-in-up-delay-2">
            <h3 style={{ marginBottom: 'var(--space-lg)', fontSize: '0.95rem' }}>
              {t('confidenceShift')}
            </h3>
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={confidence} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="gradMackage" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00e5ff" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#00e5ff" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gradSsense" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#9b8aff" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#9b8aff" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gradAldo" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#34d399" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#34d399" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" tick={{ fill: '#5a6480', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#5a6480', fontSize: 11 }} axisLine={false} tickLine={false} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="mackage" name="Mackage" stroke="#00e5ff" fill="url(#gradMackage)" strokeWidth={2} dot={{ r: 3, fill: '#00e5ff' }} connectNulls={false} />
                <Area type="monotone" dataKey="ssense" name="SSENSE" stroke="#9b8aff" fill="url(#gradSsense)" strokeWidth={2} dot={{ r: 3, fill: '#9b8aff' }} connectNulls={false} />
                <Area type="monotone" dataKey="aldo" name="Aldo" stroke="#34d399" fill="url(#gradAldo)" strokeWidth={2} dot={{ r: 3, fill: '#34d399' }} connectNulls={false} />
              </AreaChart>
            </ResponsiveContainer>
            <div className="chart-legend" style={{ marginTop: 'var(--space-md)' }}>
              <span className="legend-item"><span className="legend-dot" style={{ background: '#00e5ff' }} /> Mackage</span>
              <span className="legend-item"><span className="legend-dot" style={{ background: '#9b8aff' }} /> SSENSE</span>
              <span className="legend-item"><span className="legend-dot" style={{ background: '#34d399' }} /> Aldo</span>
            </div>
          </GlassCard>

          {/* Side-by-Side Reasoning */}
          <GlassCard className="fade-in-up fade-in-up-delay-3">
            <h3 style={{ marginBottom: 'var(--space-xl)', fontSize: '0.95rem' }}>
              <MessageSquare size={16} style={{ color: 'var(--cyan)' }} />
              {' '}{t('sideBySide')}
            </h3>

            <div className="reasoning-list">
              {reasoning.map((item) => {
                const isExpanded = expandedReasoning === item.id
                return (
                  <div key={item.id} className="reasoning-item">
                    <button
                      className="reasoning-header"
                      onClick={() => setExpandedReasoning(isExpanded ? null : item.id)}
                    >
                      <div className="reasoning-header-left">
                        <span className="reasoning-brand">{item.brand}</span>
                        <span className="reasoning-query">{item.query}</span>
                      </div>
                      {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </button>

                    {isExpanded && (
                      <div className="reasoning-body">
                        <div className="reasoning-columns">
                          {/* Before */}
                          <div className="reasoning-col reasoning-before">
                            <div className="reasoning-col-header before-header">
                              <XCircle size={14} />
                              {t('beforeFix')}
                            </div>
                            <div className="reasoning-verdict verdict-bad">
                              {item.before.verdict}
                            </div>
                            <p className="reasoning-text">{item.before.reasoning}</p>
                            <div className="reasoning-citations">
                              <span className="citations-label">Citations:</span>
                              {item.before.citations?.map((c, i) => (
                                <span key={i} className="citation-tag citation-toxic">{c}</span>
                              ))}
                            </div>
                            <div className="reasoning-confidence confidence-low">
                              Confidence: {item.before.confidence}
                            </div>
                          </div>

                          {/* After */}
                          <div className="reasoning-col reasoning-after">
                            <div className="reasoning-col-header after-header">
                              <CheckCircle size={14} />
                              {t('afterFix')}
                            </div>
                            <div className="reasoning-verdict verdict-good">
                              {item.after.verdict}
                            </div>
                            <p className="reasoning-text">{item.after.reasoning}</p>
                            <div className="reasoning-citations">
                              <span className="citations-label">Citations:</span>
                              {item.after.citations?.map((c, i) => (
                                <span key={i} className="citation-tag citation-clean">{c}</span>
                              ))}
                            </div>
                            <div className="reasoning-confidence confidence-high">
                              Confidence: {item.after.confidence}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  )
}

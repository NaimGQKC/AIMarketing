import { useState, useEffect } from 'react'
import api from '../api/client'
import { Calendar, Clock, CheckCircle, XCircle, AlertCircle, ChevronDown, ChevronUp, MessageSquare, Zap, Languages, Target, Eye, Timer, FlaskConical, GitBranch, Shield, RefreshCw } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { useLanguage } from '../context/LanguageContext'
import { useBrand } from '../context/BrandContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import AnimatedCounter from '../components/AnimatedCounter'
// Rubric structure — values populated from real audit data
const evaluationRubric = {
  semanticAlignment: {
    label: 'Semantic Alignment',
    description: 'Accuracy of product truths after LLM processing',
    standard: 'Zero hallucinations',
    current: 0,
    target: 9,
    before: 0,
    unit: '/10',
  },
  temporalAccuracy: {
    label: 'Temporal Accuracy',
    description: 'Delta between PIM update and Agent awareness',
    standard: '< 60 seconds',
    current: 0,
    target: 60,
    before: 0,
    unit: 's',
  },
  linguisticDensity: {
    label: 'Linguistic Density',
    description: 'Preservation of technical French terms',
    standard: 'No tokenization premium',
    current: 0,
    target: 9,
    before: 0,
    unit: '/10',
  },
  discoverability: {
    label: 'Discoverability',
    description: 'Probability of appearing in top agentic selection',
    standard: 'Top 3 for non-branded queries',
    current: 0,
    target: 9,
    before: 0,
    unit: '/10',
  },
}
/**
 * Statistical Confidence badge — shows the precision of probe results
 * based on the probe tier used for the latest probe run.
 *
 * Tiers:
 *   scout      (50 probes)   — directional estimate only
 *   standard   (250 probes)  — 95% CI +/-6%
 *   enterprise (1,000 probes) — 95% CI +/-3%
 */
const PROBE_TIER_BADGES = {
  scout: {
    icon: '\u26A1',
    label: 'Directional estimate',
    tooltip: 'Based on 50 probes. Upgrade for statistical significance.',
    color: 'var(--amber)',
  },
  standard: {
    icon: '\uD83D\uDCCA',
    label: '95% CI \u00B16%',
    tooltip: 'Based on 250 probes (50 iterations x 5 Golden Set angles).',
    color: 'var(--cyan)',
  },
  enterprise: {
    icon: '\uD83C\uDFAF',
    label: '95% CI \u00B13%',
    tooltip: 'Based on 1,000 probes (200 iterations x 5 Golden Set angles).',
    color: 'var(--green)',
  },
}

function StatisticalConfidenceBadge({ probeTier }) {
  const tier = (probeTier || 'standard').toLowerCase()
  const badge = PROBE_TIER_BADGES[tier] || PROBE_TIER_BADGES.standard
  return (
    <span
      className="stat-confidence-badge"
      title={badge.tooltip}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '0.35rem',
        padding: '0.2rem 0.6rem',
        borderRadius: '6px',
        fontSize: '0.75rem',
        fontWeight: 600,
        color: badge.color,
        background: 'rgba(255,255,255,0.04)',
        border: `1px solid ${badge.color}33`,
        cursor: 'help',
      }}
    >
      <span>{badge.icon}</span>
      <span>{badge.label}</span>
    </span>
  )
}

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

const eScoreStatusColors = {
  critical_failure: 'var(--coral)',
  sub_threshold: 'var(--amber)',
  marginal: 'var(--lavender)',
  strong: 'var(--cyan)',
  optimal: 'var(--green)',
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload) return null
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-label">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="chart-tooltip-row">
          <span style={{ color: p.color }}>{'\u25CF'}</span>
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
            {pre.fertility}x
          </span>
        </div>
        <div className="fertility-bar-row">
          <span className="fertility-bar-tag fertility-post">POST</span>
          <div className="fertility-bar-track">
            <div className="fertility-bar-fill"
              style={{ width: `${postWidth}%`, background: severityColors[post.severity] }} />
          </div>
          <span className="fertility-bar-value" style={{ color: severityColors[post.severity] }}>
            {post.fertility}x
          </span>
        </div>
      </div>
    </div>
  )
}

export default function Verify() {
  const { t } = useLanguage()
  const { selectedBrandId } = useBrand()
  const [expandedReasoning, setExpandedReasoning] = useState(null)
  const [deepDiveOpen, setDeepDiveOpen] = useState(false)
  const [raftOpen, setRaftOpen] = useState(false)
  const [kgOpen, setKgOpen] = useState(false)
  const [pathOpen, setPathOpen] = useState(false)

  const [schedule, setSchedule] = useState([])
  const [timeline, setTimeline] = useState([])
  const [confidence, setConfidence] = useState([])
  const [reasoning, setReasoning] = useState([])
  const [efficiency, setEfficiency] = useState({
    s_in: 0, s_out: 0, delta: 0, e_score: 0, delta_e: 0,
    status: '', interpretation: '', formula: '',
    thresholds: {}, path_to_optimal: [], history: [],
  })
  const [raft, setRaft] = useState(null)
  const [kgStats, setKgStats] = useState(null)
  const [fertility, setFertility] = useState({
    improvementPct: 0,
    preFix: {
      en: { fertility: 1.0, severity: 'healthy' },
      fr: { fertility: 1.0, severity: 'healthy' }
    },
    postFix: {
      en: { fertility: 1.0, severity: 'healthy' },
      fr: { fertility: 1.0, severity: 'healthy' }
    }
  })
  // probe_tier from the most recent probe run — defaults to "standard" for backward compat
  const [probeTier, setProbeTier] = useState('standard')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [sched, time, conf, reas, eff, raftData, kgData] = await Promise.all([
          api.verify.schedule(),
          api.verify.timeline(),
          api.verify.confidence(),
          api.verify.reasoning(),
          api.verify.efficiency(),
          api.verify.raft(selectedBrandId),
          api.verify.kg(selectedBrandId),
        ])

        if (sched) setSchedule(sched)
        if (time) setTimeline(time)
        if (conf) setConfidence(conf)
        if (reas) {
          setReasoning(reas)
          if (reas.length > 0) setExpandedReasoning(reas[0].id)
        }
        if (eff) {
          setEfficiency(eff)
          // If the efficiency data includes a probe_tier field, use it for the confidence badge.
          // Falls back to "standard" for backward compatibility with older API responses.
          if (eff.probe_tier) setProbeTier(eff.probe_tier)
          setFertility(prev => ({
            ...prev,
            postFix: {
              en: { fertility: eff.en_fertility, severity: eff.en_fertility > 1.2 ? 'warning' : 'healthy' },
              fr: { fertility: eff.fr_fertility, severity: eff.fr_fertility > 1.2 ? 'warning' : 'healthy' }
            }
          }))
        }
        if (raftData) setRaft(raftData)
        if (kgData) setKgStats(kgData)
      } catch (err) {
        console.error("Failed to fetch verify data:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [selectedBrandId])

  const { s_in: sIn, s_out: sOut, delta, e_score: eScore, delta_e: deltaE, status: eStatus,
    interpretation, path_to_optimal: pathToOptimal, history: eHistory } = efficiency

  if (loading) return <div className="page" style={{ padding: '2rem' }}>Loading Verification...</div>

  return (
    <div className="page">
      <div className="page-header fade-in-up">
        <h1>{t('verifyTitle')}</h1>
        <p>{t('verifySubtitle')}</p>
      </div>

      {/* HERO ROW: E Score + Token Fertility */}
      <div className="verify-hero fade-in-up fade-in-up-delay-1">
        {/* Remediation Efficiency */}
        <GlassCard className="e-score-card" glow="cyan">
          <div className="e-score-top">
            <div className="e-score-icon">
              <Zap size={22} />
            </div>
            <div className="e-score-trend">
              <span className={`e-trend-badge ${eStatus === 'optimal' || eStatus === 'strong' ? 'trend-up' : 'trend-down'}`}
                style={{ color: eScoreStatusColors[eStatus] || 'var(--text-secondary)' }}>
                {eStatus?.replace('_', ' ')}
              </span>
            </div>
          </div>
          <div className="e-score-value">
            <span className="animated-counter" style={{ animation: 'countUp 0.8s ease both' }}>{eScore}</span>
          </div>
          <div className="e-score-label">
            {t('remediationEfficiency')}
            <span style={{ marginLeft: '0.5rem' }}>
              <StatisticalConfidenceBadge probeTier={probeTier} />
            </span>
          </div>
          <div className="e-score-formula">
            E = (S<sub>out</sub> / S<sub>in</sub>) {'\u00B7'} (1 {'\u2212'} {'\u03B4'})
          </div>
          <div className="e-score-breakdown">
            <div className="e-param">
              <span className="e-param-label">S<sub>in</sub></span>
              <span className="e-param-value">{sIn}</span>
            </div>
            <div className="e-param-arrow">{'\u2192'}</div>
            <div className="e-param">
              <span className="e-param-label">S<sub>out</sub></span>
              <span className="e-param-value e-param-highlight">{sOut}</span>
            </div>
            <div className="e-param-divider" />
            <div className="e-param">
              <span className="e-param-label">{'\u03B4'}</span>
              <span className="e-param-value">{delta}</span>
            </div>
            <div className="e-param-divider" />
            <div className="e-param">
              <span className="e-param-label">{'\u0394'}E</span>
              <span className="e-param-value" style={{ color: deltaE > 0 ? 'var(--green)' : 'var(--coral)' }}>
                {deltaE > 0 ? '+' : ''}{deltaE}
              </span>
            </div>
          </div>
          {interpretation && (
            <div className="e-score-interpretation">{interpretation}</div>
          )}
        </GlassCard>

        {/* Token Fertility Gauge */}
        <GlassCard className="fertility-card">
          <div className="fertility-header">
            <div className="fertility-header-left">
              <Languages size={16} style={{ color: 'var(--lavender)' }} />
              <h3>{t('tokenFertilityTitle')}</h3>
            </div>
            <div className="fertility-improvement">
              <span className="badge badge-success">{'\u2193'} {fertility.improvementPct}% premium</span>
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

      {/* E-SCORE PATH TO OPTIMAL */}
      {pathToOptimal && pathToOptimal.length > 0 && (
        <div className="path-section fade-in-up fade-in-up-delay-1">
          <button className="deep-dive-toggle" onClick={() => setPathOpen(!pathOpen)}>
            <div className="deep-dive-toggle-left">
              <Target size={16} style={{ color: 'var(--cyan)' }} />
              <span className="deep-dive-toggle-label">Remediation Path: 0.6 {'\u2192'} 1.4+</span>
              <span className="deep-dive-toggle-sub">Step-by-step to optimal E-Score</span>
            </div>
            {pathOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </button>

          {pathOpen && (
            <div className="path-milestones">
              {pathToOptimal.map((step, i) => (
                <GlassCard key={i} className="path-milestone-card">
                  <div className="path-milestone-header">
                    <span className="path-milestone-num">{i + 1}</span>
                    <span className="path-milestone-title">{step.milestone}</span>
                    {step.projected_e && (
                      <span className="path-milestone-e" style={{
                        color: step.projected_e >= 1.4 ? 'var(--green)' : step.projected_e >= 1.0 ? 'var(--cyan)' : 'var(--amber)'
                      }}>
                        E = {step.projected_e}
                      </span>
                    )}
                  </div>
                  <div className="path-milestone-mechanism">{step.mechanism}</div>
                  {step.kit_type && (
                    <div className="path-milestone-kit">
                      <StatusBadge status="info" label={step.kit_type} />
                      {step.s_out_delta && <span className="path-delta">S_out {step.s_out_delta}</span>}
                      {step.delta_reduction && <span className="path-delta">{'\u03B4'} {step.delta_reduction}</span>}
                    </div>
                  )}
                </GlassCard>
              ))}
            </div>
          )}
        </div>
      )}

      {/* KG STATS + RAFT CADENCE ROW */}
      <div className="neuro-symbolic-row fade-in-up fade-in-up-delay-2">
        {/* Knowledge Graph Stats */}
        <div className="neuro-section">
          <button className="deep-dive-toggle" onClick={() => setKgOpen(!kgOpen)}>
            <div className="deep-dive-toggle-left">
              <GitBranch size={16} style={{ color: 'var(--lavender)' }} />
              <span className="deep-dive-toggle-label">Knowledge Graph</span>
              <span className="deep-dive-toggle-sub">Neuro-symbolic entity binding</span>
            </div>
            {kgOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </button>

          {kgOpen && kgStats && (
            <GlassCard className="kg-card">
              <div className="kg-stats-grid">
                <div className="kg-stat">
                  <span className="kg-stat-value">{kgStats.entity_count}</span>
                  <span className="kg-stat-label">Entities</span>
                </div>
                <div className="kg-stat">
                  <span className="kg-stat-value">{kgStats.triple_count}</span>
                  <span className="kg-stat-label">Triples</span>
                </div>
                <div className="kg-stat">
                  <span className="kg-stat-value" style={{ color: 'var(--cyan)' }}>{kgStats.hard_constraint_count}</span>
                  <span className="kg-stat-label">Hard Constraints</span>
                </div>
                <div className="kg-stat">
                  <span className="kg-stat-value" style={{ color: 'var(--green)' }}>{kgStats.boundary_score}</span>
                  <span className="kg-stat-label">Boundary Score</span>
                </div>
              </div>
              <div className="kg-formulas">
                <div className="kg-formula">
                  <span className="kg-formula-label">KGQA:</span>
                  <code>S_KGQA_out = {'{'}(e, Score(e)) : e {'\u2208'} E{'}'}</code>
                </div>
                <div className="kg-formula">
                  <span className="kg-formula-label">Fuzzy Union:</span>
                  <code>T(v?) = I - {'\u220F'}(I - T(v_i))</code>
                </div>
              </div>
            </GlassCard>
          )}
        </div>

        {/* RAFT Cadence */}
        <div className="neuro-section">
          <button className="deep-dive-toggle" onClick={() => setRaftOpen(!raftOpen)}>
            <div className="deep-dive-toggle-left">
              <RefreshCw size={16} style={{ color: 'var(--green)' }} />
              <span className="deep-dive-toggle-label">RAFT Cadence</span>
              <span className="deep-dive-toggle-sub">
                {raft ? `${raft.urgency} — every ${raft.cadence_interval_days}d` : 'Persistence plan'}
              </span>
            </div>
            {raftOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </button>

          {raftOpen && raft && (
            <GlassCard className="raft-card">
              <div className="raft-header-info">
                <div className="raft-stat">
                  <span className="raft-stat-label">Current E</span>
                  <span className="raft-stat-value">{raft.current_e_score}</span>
                </div>
                <div className="raft-stat">
                  <span className="raft-stat-label">Target E</span>
                  <span className="raft-stat-value" style={{ color: 'var(--green)' }}>{raft.target_e_score}</span>
                </div>
                <div className="raft-stat">
                  <span className="raft-stat-label">Urgency</span>
                  <StatusBadge status={raft.urgency === 'critical' ? 'failed' : raft.urgency === 'high' ? 'warning' : 'passed'} label={raft.urgency} />
                </div>
                <div className="raft-stat">
                  <span className="raft-stat-label">Cycles</span>
                  <span className="raft-stat-value">{raft.total_cycles}</span>
                </div>
              </div>

              {/* RAFT methodology */}
              <div className="raft-methodology">
                <h4>Retrieval-Augmented Fine-Tuning</h4>
                <ol className="raft-steps">
                  {raft.methodology?.steps?.map((step, i) => (
                    <li key={i} className="raft-step">{step}</li>
                  ))}
                </ol>
              </div>

              {/* Schedule preview (first 5 cycles) */}
              <div className="raft-schedule-preview">
                <h4>Next Cycles</h4>
                <div className="raft-cycles">
                  {raft.schedule?.slice(0, 5).map((cycle, i) => (
                    <div key={i} className="raft-cycle">
                      <span className="raft-cycle-num">#{cycle.cycle}</span>
                      <span className="raft-cycle-date">{cycle.scheduled_date}</span>
                      <span className="raft-cycle-e" style={{
                        color: cycle.projected_e_score >= 1.4 ? 'var(--green)' : 'var(--cyan)'
                      }}>
                        E {'\u2192'} {cycle.projected_e_score}
                      </span>
                      <StatusBadge status={cycle.status} label={cycle.status} />
                    </div>
                  ))}
                </div>
              </div>
            </GlassCard>
          )}
        </div>
      </div>

      {/* TECHNICAL DEEP DIVE (Collapsible) */}
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
                  E = (<span className="formula-val formula-sout">{sOut}</span> / <span className="formula-val formula-sin">{sIn}</span>) {'\u00B7'} (1 {'\u2212'} <span className="formula-val formula-delta">{delta}</span>) = <span className="formula-val formula-result">{eScore}</span>
                </div>
                <div className="formula-interpretation">
                  <p>
                    Your remediation layer has a <strong>{eScore}x semantic multiplier</strong>.
                    For every unit of raw PIM data quality going in, you're outputting {eScore}x the semantic clarity —
                    even after accounting for a {(delta * 100).toFixed(0)}% tokenization premium from French technical term fragmentation (Token Fertility ratio; Petrov et al., NeurIPS 2023).
                  </p>
                </div>
              </div>
            </GlassCard>
          </div>
        )}
      </div>

      {/* EXISTING VERIFY LAYOUT */}
      <div className="verify-layout">
        {/* Left column: Audit Schedule + Timeline */}
        <div className="verify-left">
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

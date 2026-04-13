import { useState, useEffect } from 'react'
import { Target, Globe, Clock, Shield, GitBranch, ChevronDown, ChevronUp, Zap, Radio, ShoppingCart, AlertTriangle, CheckCircle, MessageSquare, Wifi, Calculator, Languages } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useBrand } from '../context/BrandContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import api from '../api/client'
import './Roadmap.css'

const phaseIcons = [Globe, Shield, Radio, Clock, GitBranch]
const phaseColors = ['lavender', 'cyan', 'green', 'amber', 'lavender']

export default function Roadmap() {
  const { t } = useLanguage()
  const { selectedBrandId } = useBrand()
  const [roadmap, setRoadmap] = useState(null)
  const [syndication, setSyndication] = useState(null)
  const [freshness, setFreshness] = useState(null)
  const [authority, setAuthority] = useState(null)
  const [priority, setPriority] = useState(null)
  const [drift, setDrift] = useState(null)
  const [tax, setTax] = useState(null)
  const [moat, setMoat] = useState(null)
  const [replies, setReplies] = useState(null)
  const [pings, setPings] = useState(null)
  const [loading, setLoading] = useState(true)
  const [expandedPhase, setExpandedPhase] = useState(0)
  const [synOpen, setSynOpen] = useState(false)
  const [freshOpen, setFreshOpen] = useState(false)
  const [authOpen, setAuthOpen] = useState(false)
  const [priorityOpen, setPriorityOpen] = useState(false)
  const [repliesOpen, setRepliesOpen] = useState(false)
  const [pingsOpen, setPingsOpen] = useState(false)

  useEffect(() => {
    async function fetchData() {
      try {
        const [rm, syn, fr, auth, pri, dr, tx, mt, rp, pg] = await Promise.all([
          api.eee.roadmap(selectedBrandId),
          api.eee.syndication(selectedBrandId),
          api.eee.freshness(selectedBrandId),
          api.eee.authority(selectedBrandId),
          api.eee.priority(selectedBrandId),
          api.eee.drift(selectedBrandId),
          api.eee.tax(selectedBrandId),
          api.eee.moat(selectedBrandId),
          api.eee.replies(selectedBrandId),
          api.eee.pings(selectedBrandId),
        ])
        if (rm) setRoadmap(rm)
        if (syn) setSyndication(syn)
        if (fr) setFreshness(fr)
        if (auth) setAuthority(auth)
        if (pri) setPriority(pri)
        if (dr) setDrift(dr)
        if (tx) setTax(tx)
        if (mt) setMoat(mt)
        if (rp) setReplies(rp)
        if (pg) setPings(pg)
      } catch (err) {
        console.error('Failed to fetch EEE data:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [selectedBrandId])

  if (loading) return <div className="page" style={{ padding: '2rem' }}>Loading Roadmap...</div>

  return (
    <div className="page">
      <div className="page-header fade-in-up">
        <h1>External Environment Engineering</h1>
        <p>Control the retrieval environment. Force black-box models to treat brand specs as hard constraints.</p>
      </div>

      {/* DRIFT WARNING BANNER with Binary-Search Probe */}
      {drift?.drift_detected && (
        <div className="drift-banner fade-in-up">
          <div className="drift-banner-top">
            <AlertTriangle size={18} />
            <div className="drift-banner-text">
              <strong>DRIFT WARNING</strong> — E-Score dropped {drift.drop} from peak {drift.peak_e} to {drift.current_e}
            </div>
            <div className="drift-banner-action">Defensive Cycle: {drift.defensive_action?.cycle_hours}h / {'\u03BB'}=0.5</div>
          </div>
          {drift.toxic_probe?.suspected_source && (
            <div className="drift-probe">
              <div className="drift-probe-label">Binary-Search Probe ({drift.toxic_probe.iterations} iterations):</div>
              <div className="drift-probe-suspect">
                <span className="drift-probe-source">{drift.toxic_probe.suspected_source.toxic_source}</span>
                <span className="drift-probe-type">{drift.toxic_probe.suspected_source.gap_type}</span>
                <span className="drift-probe-damage">Damage: {(drift.toxic_probe.suspected_source.damage_score * 100).toFixed(0)}%</span>
              </div>
              <div className="drift-probe-action">{drift.toxic_probe.recommended_action?.immediate}</div>
            </div>
          )}
        </div>
      )}

      {/* HERO ROW: E-Score Journey + Interpretation Tax + Montreal Moat */}
      <div className="roadmap-hero-grid fade-in-up fade-in-up-delay-1">
        {/* E-Score Journey */}
        {roadmap && (
          <GlassCard className="journey-card" glow="cyan">
            <div className="journey-header">
              <div className="journey-start">
                <span className="journey-e-label">Current</span>
                <span className="journey-e-value journey-e-bad">{roadmap.starting_e}</span>
              </div>
              <div className="journey-arrow">
                <div className="journey-arrow-line" />
                <div className="journey-arrow-phases">
                  {roadmap.phases.map((p, i) => (
                    <div key={i} className="journey-phase-dot" style={{
                      left: `${((i + 1) / roadmap.phases.length) * 100}%`,
                      background: `var(--${phaseColors[i]})`
                    }}>
                      <span className="journey-phase-e">{p.projected_e}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="journey-end">
                <span className="journey-e-label">Target</span>
                <span className="journey-e-value journey-e-good">{roadmap.projected_final_e}</span>
              </div>
            </div>
            <div className="journey-principle">{roadmap.core_principle}</div>
            <div className="journey-meta">
              <span className="journey-meta-item"><Clock size={12} /> {roadmap.estimated_timeline}</span>
              <span className="journey-meta-item"><Target size={12} /> {roadmap.total_phases} phases</span>
              <span className="journey-meta-item"><Zap size={12} /> {'\u03B4'} = {roadmap.current_delta}</span>
            </div>
          </GlassCard>
        )}

        {/* Interpretation Tax Counter */}
        {tax && (
          <GlassCard className="tax-card" glow="lavender">
            <div className="tax-header">
              <Calculator size={16} style={{ color: 'var(--lavender)' }} />
              <h3>Interpretation Tax</h3>
            </div>
            <div className="tax-comparison">
              <div className="tax-side tax-html">
                <div className="tax-side-label">Unstructured HTML</div>
                <div className="tax-side-tokens">{tax.unstructured_html?.total_tokens?.toLocaleString()}</div>
                <div className="tax-side-unit">tokens</div>
              </div>
              <div className="tax-vs">
                <div className="tax-vs-ratio">{tax.interpretation_tax?.ratio}</div>
                <div className="tax-vs-label">cheaper</div>
              </div>
              <div className="tax-side tax-graph">
                <div className="tax-side-label">@graph JSON-LD</div>
                <div className="tax-side-tokens">{tax.deterministic_graph?.total_tokens}</div>
                <div className="tax-side-unit">tokens</div>
              </div>
            </div>
            <div className="tax-savings">
              <span className="tax-savings-num">{tax.interpretation_tax?.tokens_saved?.toLocaleString()}</span>
              <span className="tax-savings-label"> tokens saved per query</span>
            </div>
            {tax.per_attribute?.length > 0 && (
              <div className="tax-attrs">
                {tax.per_attribute.map((a, i) => (
                  <div key={i} className="tax-attr">
                    <span className="tax-attr-name">{a.attribute}</span>
                    <span className="tax-attr-savings" style={{ color: 'var(--green)' }}>{a.savings}</span>
                  </div>
                ))}
              </div>
            )}
            {tax.tax_driven_priorities?.length > 0 && (
              <div className="tax-priority-section">
                <div className="tax-priority-label">Agentic Priority</div>
                {tax.tax_driven_priorities.slice(0, 3).map((tdp, i) => (
                  <div key={i} className="tax-priority-item">
                    <span className="tax-priority-name">{tdp.product_name}</span>
                    <span className="tax-priority-score" style={{ color: 'var(--cyan)' }}>{tdp.priority_score}</span>
                  </div>
                ))}
                {tax.avg_priority_score && (
                  <div className="tax-priority-avg">
                    Avg: <strong>{tax.avg_priority_score}</strong>
                  </div>
                )}
              </div>
            )}
          </GlassCard>
        )}

        {/* Montreal Moat — EN vs FR */}
        {moat && (
          <GlassCard className="moat-card" glow="green">
            <div className="moat-header">
              <Languages size={16} style={{ color: 'var(--green)' }} />
              <h3>The Montreal Moat</h3>
              <StatusBadge status={moat.bypass_status === 'active' ? 'passed' : 'failed'} label={moat.bypass_status} />
            </div>
            <div className="moat-scores">
              <div className="moat-score">
                <div className="moat-score-lang">EN</div>
                <div className="moat-score-value" style={{ color: 'var(--cyan)' }}>{moat.en_e_score}</div>
                <div className="moat-score-fert">{moat.en_fertility}x fert.</div>
              </div>
              <div className="moat-gap-indicator">
                <div className="moat-gap-value">{'\u0394'} {moat.moat_gap}</div>
                <div className="moat-gap-arrow">{'\u2190'} gap {'\u2192'}</div>
              </div>
              <div className="moat-score">
                <div className="moat-score-lang">FR</div>
                <div className="moat-score-value" style={{ color: moat.fr_e_score < moat.en_e_score - 0.3 ? 'var(--coral)' : 'var(--amber)' }}>{moat.fr_e_score}</div>
                <div className="moat-score-fert">{moat.fr_fertility}x fert.</div>
              </div>
            </div>
            <div className="moat-detail">
              <div className="moat-detail-row">
                <span>Tokenization Premium:</span>
                <span style={{ color: 'var(--coral)' }}>+{moat.token_tax_pct}%</span>
              </div>
              <div className="moat-detail-row">
                <span>Attention Cost:</span>
                <span style={{ color: 'var(--coral)' }}>{moat.attention_scaling?.ratio}x (O(n{'\u00B2'}))</span>
              </div>
            </div>
            <div className="moat-competitive">{moat.competitive_position}</div>
            {moat.segment_3_fusion && (
              <div className="moat-fusion">
                <div className="moat-fusion-label">
                  <Radio size={10} /> Segment 3: Text-Visual Fusion
                </div>
                <div className="moat-fusion-desc">{moat.segment_3_fusion.why_it_bypasses_french_decay}</div>
                <div className="moat-fusion-stats">
                  <span>EN: {moat.segment_3_fusion.en_cost_tokens} tokens</span>
                  <span>FR: {moat.segment_3_fusion.fr_cost_tokens} tokens</span>
                  <span style={{ color: 'var(--green)' }}>Parity: {moat.segment_3_fusion.parity_achieved ? 'YES' : 'NO'}</span>
                </div>
              </div>
            )}
          </GlassCard>
        )}
      </div>

      {/* PHASE CARDS */}
      {roadmap && (
        <div className="phases-section fade-in-up fade-in-up-delay-2">
          <h2 className="section-title">Remediation Phases</h2>
          <div className="phases-list">
            {roadmap.phases.map((phase, i) => {
              const Icon = phaseIcons[i] || Target
              const color = phaseColors[i] || 'cyan'
              const isExpanded = expandedPhase === i

              return (
                <GlassCard key={i} className={`phase-card ${isExpanded ? 'phase-expanded' : ''}`}>
                  <button className="phase-header" onClick={() => setExpandedPhase(isExpanded ? -1 : i)}>
                    <div className="phase-header-left">
                      <div className={`phase-icon icon-${color}`}><Icon size={16} /></div>
                      <div className="phase-header-text">
                        <div className="phase-num">Phase {phase.phase}</div>
                        <div className="phase-name">{phase.name}</div>
                        <div className="phase-vector">{phase.eee_vector}</div>
                      </div>
                    </div>
                    <div className="phase-header-right">
                      <div className="phase-e" style={{
                        color: phase.projected_e >= 1.4 ? 'var(--green)' : phase.projected_e >= 1.0 ? 'var(--cyan)' : 'var(--amber)'
                      }}>E = {phase.projected_e}</div>
                      <div className="phase-duration">{phase.duration}</div>
                      {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                  </button>

                  {isExpanded && (
                    <div className="phase-body">
                      <div className="phase-mechanism">{phase.e_score_mechanism}</div>
                      <div className="phase-actions">
                        <h4>Actions</h4>
                        <ul>{phase.actions.map((action, j) => <li key={j}>{action}</li>)}</ul>
                      </div>
                      <div className="phase-metric">
                        <span className="phase-metric-label">Success Metric:</span>
                        <span className="phase-metric-value">{phase.success_metric}</span>
                      </div>
                      {phase.montreal_moat && (
                        <div className="phase-moat">
                          <h4>The Montreal Moat</h4>
                          <div className="moat-problem"><AlertTriangle size={12} /><span>{phase.montreal_moat.problem}</span></div>
                          <div className="moat-bypass"><CheckCircle size={12} /><span>{phase.montreal_moat.bypass}</span></div>
                        </div>
                      )}
                      {phase.cache_flush_formula && (
                        <div className="phase-formulas">
                          <h4>Cache Flush Mathematics</h4>
                          <div className="formula-row"><code>{phase.cache_flush_formula.freshness_score}</code></div>
                          <div className="formula-row"><code>{phase.cache_flush_formula.kgqa_freshened}</code></div>
                          <div className="formula-effect">{phase.cache_flush_formula.effect}</div>
                        </div>
                      )}
                    </div>
                  )}
                </GlassCard>
              )
            })}
          </div>
        </div>
      )}

      {/* DETAIL PANELS */}
      <div className="eee-details fade-in-up fade-in-up-delay-3">

        {/* Counter-Sentiment Replies */}
        {replies && replies.replies_generated > 0 && (
          <div className="eee-panel">
            <button className="eee-toggle" onClick={() => setRepliesOpen(!repliesOpen)}>
              <div className="eee-toggle-left">
                <MessageSquare size={16} style={{ color: 'var(--coral)' }} />
                <span className="eee-toggle-label">Counter-Sentiment Replies</span>
                <span className="eee-toggle-sub">
                  {replies.replies_generated} replies | {replies.platforms_targeted?.length} platforms
                </span>
              </div>
              {repliesOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
            {repliesOpen && (
              <GlassCard className="eee-detail-card">
                <div className="reply-mechanism">{replies.mechanism?.description}</div>
                <div className="reply-chain">
                  <code>{replies.mechanism?.chain}</code>
                </div>
                <div className="reply-list">
                  {replies.replies?.slice(0, 5).map((reply, i) => (
                    <div key={i} className="reply-item">
                      <div className="reply-item-header">
                        <span className="reply-platform">{reply.platform}</span>
                        <span className="reply-target">{reply.target_citation}</span>
                        <StatusBadge status={reply.status === 'draft' ? 'pending' : 'passed'} label={reply.status} />
                      </div>
                      <div className="reply-body-preview">{reply.reply_body?.slice(0, 200)}...</div>
                      <div className="reply-backlinks">
                        {reply.tier2_backlinks?.map((link, j) => (
                          <span key={j} className="reply-backlink">{link}</span>
                        ))}
                      </div>
                      <div className="reply-effectiveness">
                        <StatusBadge
                          status={reply.status === 'deployed' ? 'passed' : reply.status === 'draft' ? 'pending' : 'info'}
                          label={reply.status}
                        />
                        <span className="reply-sentiment-type">{reply.sentiment_type}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </GlassCard>
            )}
          </div>
        )}

        {/* External Pings */}
        {pings && (
          <div className="eee-panel">
            <button className="eee-toggle" onClick={() => setPingsOpen(!pingsOpen)}>
              <div className="eee-toggle-left">
                <Wifi size={16} style={{ color: 'var(--amber)' }} />
                <span className="eee-toggle-label">External Pings</span>
                <span className="eee-toggle-sub">
                  {pings.sitemap?.url_count} URLs | {pings.ping_targets?.length} engines | {pings.cycle_hours}h cycle
                </span>
              </div>
              {pingsOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
            {pingsOpen && (
              <GlassCard className="eee-detail-card">
                <div className="ping-flush-steps">
                  <h4>Cache Flush Mechanism</h4>
                  {Object.entries(pings.flush_mechanism || {}).map(([key, val]) => (
                    <div key={key} className="ping-step">
                      <span className="ping-step-num">{key.replace('step_', '')}</span>
                      <span className="ping-step-text">{val}</span>
                    </div>
                  ))}
                </div>
                <div className="ping-headers">
                  <h4>HTTP Headers</h4>
                  {Object.entries(pings.http_headers || {}).map(([key, val]) => (
                    <div key={key} className="ping-header-row">
                      <span className="ping-header-key">{key}:</span>
                      <span className="ping-header-val">{val}</span>
                    </div>
                  ))}
                </div>
                <div className="ping-targets">
                  <h4>Ping Targets</h4>
                  {pings.ping_targets?.map((target, i) => (
                    <div key={i} className="ping-target">
                      <span className="ping-target-engine">{target.engine}</span>
                      <span className="ping-target-url">{target.url}</span>
                    </div>
                  ))}
                </div>
              </GlassCard>
            )}
          </div>
        )}

        {/* Syndication Network */}
        {syndication && (
          <div className="eee-panel">
            <button className="eee-toggle" onClick={() => setSynOpen(!synOpen)}>
              <div className="eee-toggle-left">
                <Globe size={16} style={{ color: 'var(--lavender)' }} />
                <span className="eee-toggle-label">Syndication Network</span>
                <span className="eee-toggle-sub">
                  {syndication.total_nodes} nodes | Saturation: {(syndication.saturation_score?.overall * 100 || 0).toFixed(0)}%
                </span>
              </div>
              {synOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
            {synOpen && (
              <GlassCard className="eee-detail-card">
                <div className="syn-tiers">
                  {Object.entries(syndication.tiers || {}).map(([key, label]) => {
                    const tierNodes = syndication.nodes?.filter(n => n.tier === key) || []
                    return (
                      <div key={key} className="syn-tier">
                        <div className="syn-tier-header">
                          <span className="syn-tier-key">{key.replace('_', ' ')}</span>
                          <span className="syn-tier-label">{label}</span>
                          <span className="syn-tier-count">{tierNodes.length} nodes</span>
                        </div>
                        <div className="syn-nodes">
                          {tierNodes.map((node, i) => (
                            <div key={i} className="syn-node">
                              <span className="syn-node-type">{node.type.replace(/_/g, ' ')}</span>
                              <span className="syn-node-weight">{node.authority_weight}</span>
                              <StatusBadge status={node.status === 'active' ? 'passed' : 'pending'} label={node.status} />
                            </div>
                          ))}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </GlassCard>
            )}
          </div>
        )}

        {/* Citation Authority */}
        {authority && (
          <div className="eee-panel">
            <button className="eee-toggle" onClick={() => setAuthOpen(!authOpen)}>
              <div className="eee-toggle-left">
                <Shield size={16} style={{ color: 'var(--cyan)' }} />
                <span className="eee-toggle-label">Citation Authority</span>
                <span className="eee-toggle-sub">
                  Ratio: {(authority.authority_ratio * 100).toFixed(0)}% | Toxic: {authority.toxic_source_count}
                </span>
              </div>
              {authOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
            {authOpen && (
              <GlassCard className="eee-detail-card">
                <div className="auth-summary">
                  <div className="auth-stat">
                    <span className="auth-stat-value" style={{ color: authority.authority_ratio >= 0.7 ? 'var(--green)' : 'var(--coral)' }}>{(authority.authority_ratio * 100).toFixed(0)}%</span>
                    <span className="auth-stat-label">Authority Ratio</span>
                  </div>
                  <div className="auth-stat">
                    <span className="auth-stat-value" style={{ color: 'var(--coral)' }}>{authority.toxic_source_count}</span>
                    <span className="auth-stat-label">Toxic Citations</span>
                  </div>
                  <div className="auth-stat">
                    <span className="auth-stat-value" style={{ color: 'var(--green)' }}>{authority.clean_source_count}</span>
                    <span className="auth-stat-label">Clean Citations</span>
                  </div>
                </div>
                {authority.countermeasures?.map((cm, i) => (
                  <div key={i} className="auth-cm">
                    <div className="auth-cm-header">
                      <span className="auth-cm-source">{cm.toxic_source}</span>
                      <span className="auth-cm-danger">Danger: {(cm.danger_score * 100).toFixed(0)}%</span>
                    </div>
                    <div className="auth-cm-strategy">{cm.counter_strategy}</div>
                  </div>
                ))}
              </GlassCard>
            )}
          </div>
        )}

        {/* Freshness Cycle */}
        {freshness && (
          <div className="eee-panel">
            <button className="eee-toggle" onClick={() => setFreshOpen(!freshOpen)}>
              <div className="eee-toggle-left">
                <Clock size={16} style={{ color: 'var(--amber)' }} />
                <span className="eee-toggle-label">Freshness Bias Cycle</span>
                <span className="eee-toggle-sub">
                  Every {freshness.cycle_frequency_hours}h | {'\u03BB'} = {freshness.lambda_decay} | {freshness.urgency}
                </span>
              </div>
              {freshOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
            {freshOpen && (
              <GlassCard className="eee-detail-card">
                <div className="fresh-formulas">
                  <div className="fresh-formula">
                    <span className="fresh-formula-label">Freshness:</span>
                    <code>F(t) = exp(-{freshness.lambda_decay} * (t_now - t_updated))</code>
                  </div>
                  <div className="fresh-formula">
                    <span className="fresh-formula-label">KGQA:</span>
                    <code>S_KGQA_out = {'{'}(e, Score(e) * F(t)) : e {'\u2208'} E{'}'}</code>
                  </div>
                </div>
                <div className="fresh-cycles">
                  <h4>Next Cycles ({freshness.total_cycles_30d} in 30 days)</h4>
                  <div className="fresh-cycle-list">
                    {freshness.schedule?.slice(0, 8).map((cycle, i) => (
                      <div key={i} className="fresh-cycle">
                        <span className="fresh-cycle-num">#{cycle.cycle}</span>
                        <span className="fresh-cycle-time">{cycle.timestamp_utc}</span>
                        <span className="fresh-cycle-f">F = {cycle.freshness_score}</span>
                        <span className="fresh-cycle-e" style={{
                          color: cycle.projected_e >= 1.4 ? 'var(--green)' : 'var(--cyan)'
                        }}>E {'\u2192'} {cycle.projected_e}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </GlassCard>
            )}
          </div>
        )}

        {/* Agentic Commerce Priority */}
        {priority && (
          <div className="eee-panel">
            <button className="eee-toggle" onClick={() => setPriorityOpen(!priorityOpen)}>
              <div className="eee-toggle-left">
                <ShoppingCart size={16} style={{ color: 'var(--green)' }} />
                <span className="eee-toggle-label">Agentic Commerce Priority</span>
                <span className="eee-toggle-sub">
                  {priority.total_products} products | Avg priority: {priority.avg_priority_score}
                </span>
              </div>
              {priorityOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
            {priorityOpen && (
              <GlassCard className="eee-detail-card">
                <div className="priority-strategy">{priority.strategy?.principle}</div>
                <div className="priority-protocols">
                  <h4>Protocol Coverage</h4>
                  {Object.entries(priority.protocols || {}).map(([key, proto]) => (
                    <div key={key} className="priority-protocol">
                      <span className="proto-name">{key.toUpperCase()}</span>
                      <span className="proto-consumer">{proto.consumer}</span>
                      <StatusBadge status={proto.status === 'active' ? 'passed' : 'pending'} label={proto.status} />
                    </div>
                  ))}
                </div>
              </GlassCard>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

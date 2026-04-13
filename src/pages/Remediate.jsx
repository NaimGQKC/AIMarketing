import { useState, useEffect } from 'react'
import { Cpu, FileJson, Film, Rocket, ChevronRight, Check, ChevronDown, ChevronUp, Shield, GitBranch, Zap } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import { useBrand } from '../context/BrandContext'
import api from '../api/client'
import './Remediate.css'

const typeIcons = { hardAttributes: Cpu, jsonLd: FileJson, truthClip: Film }
const typeColors = { hardAttributes: 'cyan', jsonLd: 'lavender', truthClip: 'green' }

const typeLabels = {
  hardAttributes: 'DPO Constraint Decoding',
  jsonLd: 'Deterministic @graph Schema',
  truthClip: 'MRC Q-Former Truth Clip',
}

const typeMechanisms = {
  hardAttributes: 'P(contradictory_token) = 0 — eliminates E1 Semantic Override errors',
  jsonLd: 'Deterministic @graph ID overrides heuristic text-generation-inference parsers',
  truthClip: 'Bypasses text tokenization entirely by anchoring brand identity in language-agnostic visual embeddings',
}

export default function Remediate() {
  const { t } = useLanguage()
  const { selectedBrandId } = useBrand()
  const [fixKits, setFixKits] = useState([])
  const [selectedKit, setSelectedKit] = useState(null)
  const [kitPreview, setKitPreview] = useState(null)
  const [deploying, setDeploying] = useState(false)
  const [deployed, setDeployed] = useState({})
  const [progress, setProgress] = useState(0)
  const [comparison, setComparison] = useState({ before: null, after: null })
  const [loading, setLoading] = useState(true)
  const [expandDPO, setExpandDPO] = useState(false)
  const [expandGraph, setExpandGraph] = useState(false)
  const [expandClip, setExpandClip] = useState(false)

  useEffect(() => {
    async function fetchData() {
      try {
        const [kitsData, compareData] = await Promise.all([
          api.remediate.kits(selectedBrandId),
          api.remediate.compare(),
        ])
        if (kitsData) {
          setFixKits(kitsData)
          if (kitsData[0]) {
            setSelectedKit(kitsData[0])
          }
        }
        if (compareData) {
          setComparison(compareData)
        }
      } catch (err) {
        console.error('Failed to fetch remediate data:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [selectedBrandId])

  // Fetch full preview when kit is selected
  useEffect(() => {
    if (!selectedKit) return
    async function fetchPreview() {
      const preview = await api.remediate.preview(selectedKit.id)
      if (preview) setKitPreview(preview)
    }
    fetchPreview()
  }, [selectedKit?.id])

  const handleDeploy = (kitId) => {
    setDeploying(true)
    setProgress(0)
    api.remediate.deploy(kitId)
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setDeploying(false)
          setDeployed(d => ({ ...d, [kitId]: true }))
          return 100
        }
        return prev + 2
      })
    }, 40)
  }

  if (loading) return <div className="page" style={{ padding: '2rem' }}>Loading Remediation...</div>

  return (
    <div className="page">
      <div className="page-header fade-in-up">
        <h1>{t('remediateTitle')}</h1>
        <p>{t('remediateSubtitle')}</p>
      </div>

      <div className="remediate-layout">
        {/* Fix Kit Cards */}
        <div className="fix-kits-column fade-in-up fade-in-up-delay-1">
          <h3>{t('fixKits')}</h3>
          <div className="fix-kits-list">
            {fixKits.map((kit) => {
              const Icon = typeIcons[kit.type]
              const color = typeColors[kit.type]
              const isSelected = selectedKit?.id === kit.id
              const isDone = deployed[kit.id]

              return (
                <GlassCard
                  key={kit.id}
                  className={`fix-kit-card ${isSelected ? 'fix-kit-selected' : ''}`}
                  glow={color}
                  onClick={() => setSelectedKit(kit)}
                >
                  <div className="fix-kit-header">
                    <div className={`fix-kit-icon icon-${color}`}>
                      <Icon size={18} />
                    </div>
                    {isDone ? (
                      <StatusBadge status="deployed" label={t('deployed')} />
                    ) : (
                      <StatusBadge status={kit.status} label={kit.status} />
                    )}
                  </div>
                  <div className="fix-kit-type">{typeLabels[kit.type] || t(kit.type)}</div>
                  <div className="fix-kit-brand">{kit.brand}</div>
                  <div className="fix-kit-product">{kit.product}</div>
                  <p className="fix-kit-impact">{kit.impact}</p>
                  <div className="fix-kit-mechanism">
                    <Shield size={10} style={{ opacity: 0.5 }} />
                    <span>{typeMechanisms[kit.type]}</span>
                  </div>
                  {isSelected && <ChevronRight size={16} className="fix-kit-arrow" />}
                </GlassCard>
              )
            })}
          </div>
        </div>

        {/* Preview Panel */}
        <div className="preview-column fade-in-up fade-in-up-delay-2">
          {selectedKit && (
            <>
              <h3>{t('preview')} — {selectedKit.brand} {selectedKit.product}</h3>

              {/* === HARD ATTRIBUTES — DPO Constraint Set === */}
              {selectedKit.type === 'hardAttributes' && (
                <>
                  <GlassCard className="preview-card">
                    <div className="preview-label">
                      <Cpu size={14} style={{ color: 'var(--cyan)' }} />
                      DPO Hard Attribute Constraints
                    </div>
                    <div className="dpo-summary">
                      <div className="dpo-stat">
                        <span className="dpo-stat-label">Method</span>
                        <span className="dpo-stat-value">Direct Preference Optimization</span>
                      </div>
                      <div className="dpo-stat">
                        <span className="dpo-stat-label">Error Target</span>
                        <span className="dpo-stat-value" style={{ color: 'var(--coral)' }}>E1 Semantic Override</span>
                      </div>
                      <div className="dpo-stat">
                        <span className="dpo-stat-label">Enforcement</span>
                        <span className="dpo-stat-value" style={{ color: 'var(--cyan)' }}>P(contradiction) = 0</span>
                      </div>
                      {kitPreview?.dpo_constraints && (
                        <div className="dpo-stat">
                          <span className="dpo-stat-label">CSR</span>
                          <span className="dpo-stat-value">{kitPreview.dpo_constraints.contextual_success_rate}</span>
                        </div>
                      )}
                    </div>

                    {/* Constraint list */}
                    {kitPreview?.dpo_constraints?.constraints && (
                      <div className="constraints-list">
                        {kitPreview.dpo_constraints.constraints.map((c, i) => (
                          <div key={i} className="constraint-row">
                            <span className="constraint-id">{c.id}</span>
                            <span className="constraint-attr">{c.attribute}</span>
                            <span className="constraint-val">{c.required_value}</span>
                            <span className="constraint-badge">HARD</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </GlassCard>

                  {/* Expandable raw payload */}
                  <button className="expand-toggle" onClick={() => setExpandDPO(!expandDPO)}>
                    <span>Full DPO Payload</span>
                    {expandDPO ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                  </button>
                  {expandDPO && (
                    <GlassCard className="preview-card">
                      <pre className="json-preview">
                        <code>{JSON.stringify(kitPreview?.dpo_constraints || selectedKit.payload, null, 2)}</code>
                      </pre>
                    </GlassCard>
                  )}
                </>
              )}

              {/* === JSON-LD — Deterministic @graph === */}
              {selectedKit.type === 'jsonLd' && (
                <>
                  <GlassCard className="preview-card">
                    <div className="preview-label">
                      <GitBranch size={14} style={{ color: 'var(--lavender)' }} />
                      Deterministic @graph Schema
                    </div>
                    <div className="graph-summary">
                      {kitPreview?.graph?.['@graph'] && (
                        <div className="graph-nodes">
                          {kitPreview.graph['@graph'].map((node, i) => (
                            <div key={i} className="graph-node">
                              <span className="graph-node-type">{node['@type']}</span>
                              <span className="graph-node-id">{node['@id']}</span>
                              <span className="graph-node-name">{node.name || ''}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </GlassCard>

                  <button className="expand-toggle" onClick={() => setExpandGraph(!expandGraph)}>
                    <span>Full @graph JSON-LD</span>
                    {expandGraph ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                  </button>
                  {expandGraph && (
                    <GlassCard className="preview-card">
                      <pre className="json-preview">
                        <code>{JSON.stringify(kitPreview?.graph || selectedKit.payload, null, 2)}</code>
                      </pre>
                    </GlassCard>
                  )}
                </>
              )}

              {/* === TRUTH CLIP — MRC Q-Former === */}
              {selectedKit.type === 'truthClip' && (
                <>
                  <GlassCard className="preview-card">
                    <div className="preview-label">
                      <Film size={14} style={{ color: 'var(--green)' }} />
                      MRC Q-Former Truth Clip
                    </div>
                    <div className="clip-summary">
                      <div className="clip-stat">
                        <span className="clip-stat-label">Architecture</span>
                        <span className="clip-stat-value">Multi-Resolution Causal Q-Former</span>
                      </div>
                      <div className="clip-stat">
                        <span className="clip-stat-label">Duration</span>
                        <span className="clip-stat-value">15s (3 x 5s segments)</span>
                      </div>
                      <div className="clip-stat">
                        <span className="clip-stat-label">Bypass</span>
                        <span className="clip-stat-value" style={{ color: 'var(--green)' }}>Tokenization Premium</span>
                      </div>
                      <div className="clip-stat">
                        <span className="clip-stat-label">Mechanism</span>
                        <span className="clip-stat-value">Cross-modal attention → visual embeddings</span>
                      </div>
                    </div>

                    {/* Temporal segments */}
                    {kitPreview?.truth_clip?.hasPart && (
                      <div className="clip-segments">
                        {kitPreview.truth_clip.hasPart.map((seg, i) => (
                          <div key={i} className="clip-segment">
                            <div className="clip-seg-time">
                              {seg.startOffset}s — {seg.endOffset}s
                            </div>
                            <div className="clip-seg-name">{seg.name}</div>
                            <div className="clip-seg-desc">{seg.description}</div>
                            {seg['visimind:qformerResolution'] && (
                              <div className="clip-seg-meta">
                                <span className="clip-seg-tag">{seg['visimind:featureType']}</span>
                                <span className="clip-seg-budget">{seg['visimind:attentionBudget']}</span>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </GlassCard>

                  <button className="expand-toggle" onClick={() => setExpandClip(!expandClip)}>
                    <span>Full Truth Clip Metadata</span>
                    {expandClip ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                  </button>
                  {expandClip && (
                    <GlassCard className="preview-card">
                      <pre className="json-preview">
                        <code>{JSON.stringify(kitPreview?.truth_clip || selectedKit.payload, null, 2)}</code>
                      </pre>
                    </GlassCard>
                  )}
                </>
              )}

              {/* Before/After */}
              {comparison.before && comparison.after && (
                <>
                  <h3 style={{ marginTop: 'var(--space-xl)' }}>{t('beforeAfter')}</h3>
                  <div className="before-after">
                    <GlassCard className="before-card">
                      <div className="ba-header ba-before">Before — Passive Data</div>
                      <pre className="ba-code"><code>{JSON.stringify(comparison.before, null, 2)}</code></pre>
                    </GlassCard>
                    <GlassCard className="after-card">
                      <div className="ba-header ba-after">After — Active Entity Integrity</div>
                      <pre className="ba-code"><code>{JSON.stringify(comparison.after, null, 2)}</code></pre>
                    </GlassCard>
                  </div>
                </>
              )}

              {/* Deploy Button */}
              <div className="deploy-section">
                {deploying ? (
                  <div className="deploy-progress">
                    <div className="deploy-progress-bar" style={{ width: `${progress}%` }} />
                    <span className="deploy-progress-text">{t('deploying')} {progress}%</span>
                  </div>
                ) : deployed[selectedKit.id] ? (
                  <button className="btn btn-primary deploy-btn" disabled>
                    <Check size={16} /> {t('deployed')}
                  </button>
                ) : (
                  <button className="btn btn-primary deploy-btn" onClick={() => handleDeploy(selectedKit.id)}>
                    <Rocket size={16} /> {t('deployFix')}
                  </button>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

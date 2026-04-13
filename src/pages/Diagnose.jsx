import { useState, useEffect } from 'react'
import { AlertTriangle, ExternalLink, X, FileWarning, Globe, Cpu, FileJson, Film, Rocket, Check } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import { useBrand } from '../context/BrandContext'
import api from '../api/client'
import './Diagnose.css'

const typeIcons = { hardAttributes: Cpu, jsonLd: FileJson, truthClip: Film }
const typeLabels = { hardAttributes: 'Hard Attributes', jsonLd: 'JSON-LD Injection', truthClip: 'Truth Clip' }

export default function Diagnose() {
  const { t } = useLanguage()
  const [selectedGap, setSelectedGap] = useState(null)
  const [signalGaps, setSignalGaps] = useState([])
  const [reasoningParity, setReasoningParity] = useState({
    en: 0, fr: 0, enQueries: 0, frQueries: 0,
    enHallucinations: 0, frHallucinations: 0,
    tokenBreakdown: { en: { avgTokens: 0, maxTokens: 0 }, fr: { avgTokens: 0, maxTokens: 0 } }
  })
  const [loading, setLoading] = useState(true)
  const { selectedBrandId } = useBrand()

  // Fix kit state for the detail panel
  const [fixKit, setFixKit] = useState(null)
  const [loadingKit, setLoadingKit] = useState(false)
  const [deploying, setDeploying] = useState(false)
  const [deployProgress, setDeployProgress] = useState(0)
  const [deployed, setDeployed] = useState({})

  useEffect(() => {
    async function fetchData() {
      try {
        const [gapsData, parityData] = await Promise.all([
          api.diagnose.gaps(selectedBrandId),
          api.diagnose.parity(selectedBrandId),
        ])

        if (gapsData) {
          const transformedGaps = gapsData.map((g, idx) => ({
            id: g.id || idx + 1,
            query: g.query,
            lang: g.lang,
            gapType: g.gap_type,
            severity: g.severity,
            aiResponseQuality: g.ai_response_quality,
            sourceOfTruth: {
              label: g.source_of_truth?.label || '',
              url: g.source_of_truth?.url || null,
              detail: g.source_of_truth?.detail || '',
            },
            sourceOfHallucination: {
              label: g.source_of_hallucination?.label || '',
              url: g.source_of_hallucination?.url || null,
              detail: g.source_of_hallucination?.detail || '',
            },
            aiSaid: g.ai_said || '',
            brandTruth: g.brand_truth || '',
          }))
          setSignalGaps(transformedGaps)
        }

        if (parityData && parityData.en !== undefined) {
          setReasoningParity({
            en: parityData.en,
            fr: parityData.fr,
            enQueries: parityData.en_queries,
            frQueries: parityData.fr_queries,
            enHallucinations: parityData.en_hallucinations,
            frHallucinations: parityData.fr_hallucinations,
            tokenBreakdown: parityData.token_breakdown || {
              en: { avgTokens: 0, maxTokens: 0 },
              fr: { avgTokens: 0, maxTokens: 0 },
            },
          })
        }
      } catch (err) {
        console.error('Failed to fetch diagnose data:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [selectedBrandId])

  // Fetch fix kit when a gap is selected
  useEffect(() => {
    if (!selectedGap) {
      setFixKit(null)
      return
    }
    setLoadingKit(true)
    api.diagnose.gapFixKit(selectedGap.id)
      .then(kit => setFixKit(kit))
      .catch(() => setFixKit(null))
      .finally(() => setLoadingKit(false))
  }, [selectedGap])

  const handleDeploy = (kitId) => {
    setDeploying(true)
    setDeployProgress(0)
    // Simulate deploy progress, then call actual API
    const interval = setInterval(() => {
      setDeployProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          api.diagnose.deployKit(kitId).catch(() => {})
          setDeploying(false)
          setDeployed(d => ({ ...d, [kitId]: true }))
          return 100
        }
        return prev + 2
      })
    }, 40)
  }

  if (loading) return <div className="page" style={{ padding: '2rem' }}>Loading Diagnostics...</div>

  return (
    <div className="page">
      <div className="page-header fade-in-up">
        <h1>{t('diagnoseTitle')}</h1>
        <p>{t('diagnoseSubtitle')}</p>
      </div>

      {/* Reasoning Parity Bar */}
      <GlassCard className="parity-section fade-in-up fade-in-up-delay-1">
        <div className="parity-header">
          <h3>
            <Globe size={16} style={{ color: 'var(--cyan)' }} />
            {' '}{t('reasoningParity')}
          </h3>
          <div className="parity-stats">
            <span className="badge badge-info">{reasoningParity.enQueries} EN queries</span>
            <span className="badge badge-info">{reasoningParity.frQueries} FR queries</span>
          </div>
        </div>

        <div className="parity-bars">
          <div className="parity-bar-row">
            <div className="parity-bar-label">
              <span className="parity-lang">EN</span>
              <span className="parity-label">{t('enVisibility')}</span>
            </div>
            <div className="parity-bar-track">
              <div
                className="parity-bar-fill parity-en"
                style={{ width: `${reasoningParity.en}%` }}
              >
                <span className="parity-bar-value">{reasoningParity.en}%</span>
              </div>
            </div>
            <div className="parity-bar-meta">
              <span className="parity-hallucinations">{reasoningParity.enHallucinations} hallucinations</span>
              <span className="parity-tokens">~{reasoningParity.tokenBreakdown.en.avgTokens} tokens/query</span>
            </div>
          </div>

          <div className="parity-bar-row">
            <div className="parity-bar-label">
              <span className="parity-lang parity-lang-fr">FR</span>
              <span className="parity-label">{t('frVisibility')}</span>
            </div>
            <div className="parity-bar-track">
              <div
                className="parity-bar-fill parity-fr"
                style={{ width: `${reasoningParity.fr}%` }}
              >
                <span className="parity-bar-value">{reasoningParity.fr}%</span>
              </div>
            </div>
            <div className="parity-bar-meta">
              <span className="parity-hallucinations parity-hallucinations-high">{reasoningParity.frHallucinations} hallucinations</span>
              <span className="parity-tokens parity-tokens-high">~{reasoningParity.tokenBreakdown.fr.avgTokens} tokens/query</span>
            </div>
          </div>
        </div>

        <div className="parity-message">
          <AlertTriangle size={16} />
          <p>{t('parityMessage', { en: reasoningParity.en, fr: reasoningParity.fr })}</p>
        </div>
      </GlassCard>

      {/* Signal Gap Table */}
      <div className="diagnose-layout">
        <GlassCard className="gap-table-card fade-in-up fade-in-up-delay-2">
          <h3>
            <FileWarning size={16} style={{ color: 'var(--coral)' }} />
            {' '}{t('signalGapTable')}
          </h3>
          <div className="table-scroll">
            <table className="data-table" id="signal-gap-table">
              <thead>
                <tr>
                  <th>{t('query')}</th>
                  <th>{t('language')}</th>
                  <th>{t('sourceOfTruth')}</th>
                  <th>{t('sourceOfHallucination')}</th>
                  <th>{t('gapType')}</th>
                  <th>{t('severity')}</th>
                </tr>
              </thead>
              <tbody>
                {signalGaps.map((gap) => (
                  <tr
                    key={gap.id}
                    onClick={() => setSelectedGap(gap)}
                    className={selectedGap?.id === gap.id ? 'row-selected' : ''}
                  >
                    <td>
                      <span className="query-text">{gap.query}</span>
                    </td>
                    <td>
                      <span className={`badge ${gap.lang === 'FR' ? 'badge-warning' : 'badge-cyan'}`}>{gap.lang}</span>
                    </td>
                    <td>
                      <div className="source-cell source-truth">
                        <span className="source-dot source-dot-truth" />
                        <span className="source-label">{gap.sourceOfTruth.label}</span>
                      </div>
                    </td>
                    <td>
                      <div className="source-cell source-toxic">
                        <span className="source-dot source-dot-toxic" />
                        <div className="source-toxic-content">
                          <span className="source-label">{gap.sourceOfHallucination.label}</span>
                          {gap.sourceOfHallucination.url && (
                            <a href={gap.sourceOfHallucination.url} className="source-link" target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>
                              <ExternalLink size={10} />
                            </a>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${gap.gapType === 'Token Decay' || gap.gapType === 'Tokenization Premium' ? 'badge-warning' : gap.gapType === 'Entity Trust' ? 'badge-critical' : 'badge-info'}`}>
                        {gap.gapType === 'Token Decay' ? 'Tokenization Premium' : gap.gapType}
                      </span>
                    </td>
                    <td><StatusBadge status={gap.severity} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>

        {/* Detail Panel — Signal Analysis + Fix Kit */}
        {selectedGap && (
          <div className="gap-detail-panel fade-in-up">
            <div className="gap-detail-header">
              <h3>Signal Analysis</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setSelectedGap(null)}>
                <X size={14} />
              </button>
            </div>

            <div className="gap-detail-query">
              <span className="detail-label">{t('query')}</span>
              <span className="detail-query-text">{selectedGap.query}</span>
            </div>

            <div className="gap-detail-sources">
              <div className="gap-source-card source-truth-card">
                <div className="gap-source-header">
                  <span className="source-dot source-dot-truth" />
                  <span>{t('sourceOfTruth')}</span>
                </div>
                <div className="gap-source-name">{selectedGap.sourceOfTruth.label}</div>
                <code className="gap-source-url">{selectedGap.sourceOfTruth.url}</code>
                <p className="gap-source-detail">{selectedGap.sourceOfTruth.detail}</p>
              </div>

              <div className="vs-divider">VS</div>

              <div className="gap-source-card source-toxic-card">
                <div className="gap-source-header">
                  <span className="source-dot source-dot-toxic" />
                  <span>{t('sourceOfHallucination')}</span>
                </div>
                <div className="gap-source-name">{selectedGap.sourceOfHallucination.label}</div>
                {selectedGap.sourceOfHallucination.url && (
                  <code className="gap-source-url toxic-url">{selectedGap.sourceOfHallucination.url}</code>
                )}
                <p className="gap-source-detail">{selectedGap.sourceOfHallucination.detail}</p>
              </div>
            </div>

            <div className="gap-detail-diff">
              <div className="diff-section">
                <div className="diff-header diff-ai">
                  <span>What AI Said</span>
                  <span className="diff-quality">Quality: {selectedGap.aiResponseQuality}%</span>
                </div>
                <div className="diff-body diff-body-ai">{selectedGap.aiSaid}</div>
              </div>
              <div className="diff-section">
                <div className="diff-header diff-truth">
                  <span>Brand Truth</span>
                </div>
                <div className="diff-body diff-body-truth">{selectedGap.brandTruth}</div>
              </div>
            </div>

            {/* Inline Fix Kit Section */}
            <div className="fix-kit-inline">
              <div className="fix-kit-inline-header">
                <h4>{t('fixKits')}</h4>
              </div>

              {loadingKit ? (
                <div className="fix-kit-loading">Loading fix kit...</div>
              ) : fixKit ? (
                <GlassCard className="fix-kit-inline-card">
                  <div className="fix-kit-inline-top">
                    <div className="fix-kit-inline-icon">
                      {(() => {
                        const Icon = typeIcons[fixKit.type] || Cpu
                        return <Icon size={16} />
                      })()}
                    </div>
                    <div className="fix-kit-inline-info">
                      <span className="fix-kit-inline-type">{typeLabels[fixKit.type] || fixKit.type}</span>
                      <span className="fix-kit-inline-target">{fixKit.brand} — {fixKit.product}</span>
                    </div>
                    {deployed[fixKit.id] ? (
                      <StatusBadge status="deployed" label={t('deployed')} />
                    ) : (
                      <StatusBadge status={fixKit.status} label={fixKit.status} />
                    )}
                  </div>

                  {/* Payload preview */}
                  {fixKit.payload && (
                    <div className="fix-kit-payload">
                      <span className="detail-label">Payload</span>
                      <div className="fix-kit-attributes">
                        {Object.entries(fixKit.payload).map(([key, val]) => (
                          <div key={key} className="attribute-row">
                            <span className="attribute-key">{key}:</span>
                            <span className="attribute-value">{typeof val === 'object' ? JSON.stringify(val) : String(val)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <p className="fix-kit-impact">{fixKit.impact}</p>

                  {/* Deploy button */}
                  <div className="deploy-section">
                    {deploying ? (
                      <div className="deploy-progress">
                        <div className="deploy-progress-bar" style={{ width: `${deployProgress}%` }} />
                        <span className="deploy-progress-text">{t('deploying')} {deployProgress}%</span>
                      </div>
                    ) : deployed[fixKit.id] ? (
                      <button className="btn btn-primary deploy-btn" disabled>
                        <Check size={16} /> {t('deployed')}
                      </button>
                    ) : (
                      <button className="btn btn-primary deploy-btn" onClick={() => handleDeploy(fixKit.id)}>
                        <Rocket size={16} /> {t('deployFix')}
                      </button>
                    )}
                  </div>
                </GlassCard>
              ) : (
                <div className="fix-kit-empty">No fix kit available for this gap yet.</div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

import { useState } from 'react'
import { AlertTriangle, ExternalLink, X, FileWarning, Globe } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import { signalGaps, reasoningParity } from '../data/mockData'
import './Diagnose.css'

export default function Diagnose() {
  const { t } = useLanguage()
  const [selectedGap, setSelectedGap] = useState(null)

  const parityMsg = t('parityMessage', { en: reasoningParity.en, fr: reasoningParity.fr })

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
          <p>{parityMsg}</p>
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
                      <span className={`badge ${gap.gapType === 'Token Decay' ? 'badge-warning' : gap.gapType === 'Entity Trust' ? 'badge-critical' : 'badge-info'}`}>
                        {gap.gapType}
                      </span>
                    </td>
                    <td><StatusBadge status={gap.severity} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassCard>

        {/* Detail Panel */}
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
                  <span>🤖 What AI Said</span>
                  <span className="diff-quality">Quality: {selectedGap.aiResponseQuality}%</span>
                </div>
                <div className="diff-body diff-body-ai">{selectedGap.aiSaid}</div>
              </div>
              <div className="diff-section">
                <div className="diff-header diff-truth">
                  <span>✅ Brand Truth</span>
                </div>
                <div className="diff-body diff-body-truth">{selectedGap.brandTruth}</div>
              </div>
            </div>

            <button className="btn btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: 'var(--space-lg)' }}>
              {t('deployFix')} →
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

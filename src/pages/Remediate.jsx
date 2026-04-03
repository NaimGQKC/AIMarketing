import { useState, useEffect } from 'react'
import { Cpu, FileJson, Film, Rocket, ChevronRight, Check } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import { useBrand } from '../context/BrandContext'
import api from '../api/client'
import { fixKits as mockKits, deploymentBefore, deploymentAfter } from '../data/mockData'
import './Remediate.css'

const typeIcons = { hardAttributes: Cpu, jsonLd: FileJson, truthClip: Film }
const typeColors = { hardAttributes: 'cyan', jsonLd: 'lavender', truthClip: 'green' }

export default function Remediate() {
  const { t } = useLanguage()
  const { selectedBrandId } = useBrand()
  const [fixKits, setFixKits] = useState(mockKits)
  const [selectedKit, setSelectedKit] = useState(mockKits[0])
  const [deploying, setDeploying] = useState(false)
  const [deployed, setDeployed] = useState({})
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    async function fetchKits() {
      try {
        const data = await api.remediate.kits(selectedBrandId)
        if (data && data.length > 0) {
          setFixKits(data)
          setSelectedKit(data[0])
        } else {
          // If no kits found, empty or mock based on preference
          // For demo purposes, we can fall back to mocks filtered by brand if we wanted, but let's just use what API returns
          setFixKits(data || [])
          setSelectedKit(data?.[0] || null)
        }
      } catch (err) {
        console.warn('Failed to fetch fix kits, using mock', err)
      }
    }
    fetchKits()
  }, [selectedBrandId])

  const handleDeploy = (kitId) => {
    setDeploying(true)
    setProgress(0)
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
                  <div className="fix-kit-type">{t(kit.type)}</div>
                  <div className="fix-kit-brand">{kit.brand}</div>
                  <div className="fix-kit-product">{kit.product}</div>
                  <p className="fix-kit-impact">{kit.impact}</p>
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

              {selectedKit.type === 'hardAttributes' && (
                <GlassCard className="preview-card">
                  <div className="preview-label">Hard Attributes to Inject</div>
                  <div className="attributes-grid">
                    {Object.entries(selectedKit.payload || selectedKit.attributes || {}).map(([key, val]) => (
                      <div key={key} className="attribute-row">
                        <span className="attribute-key">{key}:</span>
                        <span className="attribute-value">{val}</span>
                      </div>
                    ))}
                  </div>
                </GlassCard>
              )}

              {selectedKit.type === 'jsonLd' && (
                <GlassCard className="preview-card">
                  <div className="preview-label">JSON-LD Preview</div>
                  <pre className="json-preview">
                    <code>{JSON.stringify(selectedKit.payload || selectedKit.jsonLdPreview, null, 2)}</code>
                  </pre>
                </GlassCard>
              )}

              {selectedKit.type === 'truthClip' && (
                <GlassCard className="preview-card">
                  <div className="preview-label">Truth Clip Specification</div>
                  <div className="truth-clip-grid">
                    {Object.entries(selectedKit.payload || selectedKit.truthClip || {}).map(([key, val]) => (
                      <div key={key} className="attribute-row">
                        <span className="attribute-key">{key}:</span>
                        <span className="attribute-value">{val}</span>
                      </div>
                    ))}
                  </div>
                </GlassCard>
              )}

              {/* Before/After */}
              <h3 style={{ marginTop: 'var(--space-xl)' }}>{t('beforeAfter')}</h3>
              <div className="before-after">
                <GlassCard className="before-card">
                  <div className="ba-header ba-before">Before</div>
                  <pre className="ba-code"><code>{JSON.stringify(deploymentBefore.data, null, 2)}</code></pre>
                </GlassCard>
                <GlassCard className="after-card">
                  <div className="ba-header ba-after">After</div>
                  <pre className="ba-code"><code>{JSON.stringify(deploymentAfter.data, null, 2)}</code></pre>
                </GlassCard>
              </div>

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

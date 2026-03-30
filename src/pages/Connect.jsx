import { useState } from 'react'
import { ShoppingBag, Database, Eye, Search, CheckCircle, XCircle, RefreshCw, ArrowRight, Zap } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import { pimIntegrations, monitoringAccounts, feedStatus } from '../data/mockData'
import './Connect.css'

const iconMap = { ShoppingBag, Database, Eye, Search }

export default function Connect() {
  const { t } = useLanguage()
  const [connecting, setConnecting] = useState(null)

  const handleConnect = (id) => {
    setConnecting(id)
    setTimeout(() => setConnecting(null), 2500)
  }

  return (
    <div className="page">
      <div className="page-header fade-in-up">
        <h1>{t('connectTitle')}</h1>
        <p>{t('connectSubtitle')}</p>
      </div>

      {/* Data Flow Visual */}
      <div className="data-flow fade-in-up fade-in-up-delay-1">
        <div className="flow-node flow-source">
          <Database size={20} />
          <span>PIM Sources</span>
        </div>
        <div className="flow-connector">
          <div className="flow-dot" />
          <div className="flow-dot flow-dot-2" />
          <div className="flow-dot flow-dot-3" />
          <ArrowRight size={16} className="flow-arrow" />
        </div>
        <div className="flow-node flow-engine">
          <Zap size={20} />
          <span>VisiMind</span>
        </div>
        <div className="flow-connector">
          <div className="flow-dot" />
          <div className="flow-dot flow-dot-2" />
          <div className="flow-dot flow-dot-3" />
          <ArrowRight size={16} className="flow-arrow" />
        </div>
        <div className="flow-node flow-dest">
          <span className="flow-dest-label">UCP / ACP</span>
        </div>
      </div>

      {/* PIM Integrations */}
      <h3 className="section-title fade-in-up fade-in-up-delay-2">{t('pimIntegrations')}</h3>
      <div className="page-grid grid-2" style={{ marginBottom: 'var(--space-2xl)' }}>
        {pimIntegrations.map((pim) => {
          const Icon = iconMap[pim.icon]
          return (
            <GlassCard key={pim.id} className={`connect-card fade-in-up fade-in-up-delay-2 ${pim.status === 'connected' ? 'card-connected' : ''}`}>
              <div className="connect-card-header">
                <div className="connect-card-icon">
                  <Icon size={22} />
                </div>
                <StatusBadge status={pim.status} label={t(pim.status)} />
              </div>
              <h4>{pim.name}</h4>
              <p className="connect-card-desc">{pim.description}</p>
              {pim.status === 'connected' ? (
                <div className="connect-card-stats">
                  <div className="connect-stat">
                    <span className="connect-stat-value">{pim.itemsSynced.toLocaleString()}</span>
                    <span className="connect-stat-label">{t('itemsSynced')}</span>
                  </div>
                  <div className="connect-stat">
                    <span className="connect-stat-value" style={{ color: pim.errors > 0 ? 'var(--coral)' : 'var(--green)' }}>{pim.errors}</span>
                    <span className="connect-stat-label">{t('errors')}</span>
                  </div>
                  <button className="btn btn-ghost btn-sm">
                    <RefreshCw size={14} /> Resync
                  </button>
                </div>
              ) : (
                <button
                  className="btn btn-primary"
                  onClick={() => handleConnect(pim.id)}
                  disabled={connecting === pim.id}
                >
                  {connecting === pim.id ? (
                    <><RefreshCw size={14} className="spin" /> {t('syncing')}</>
                  ) : (
                    t('connectNow')
                  )}
                </button>
              )}
            </GlassCard>
          )
        })}
      </div>

      {/* Monitoring Sync */}
      <h3 className="section-title fade-in-up fade-in-up-delay-3">{t('monitoringSync')}</h3>
      <div className="page-grid grid-2" style={{ marginBottom: 'var(--space-2xl)' }}>
        {monitoringAccounts.map((acc) => {
          const Icon = iconMap[acc.icon]
          return (
            <GlassCard key={acc.id} className="connect-card card-connected fade-in-up fade-in-up-delay-3">
              <div className="connect-card-header">
                <div className="connect-card-icon">
                  <Icon size={22} />
                </div>
                <StatusBadge status={acc.status} label={t(acc.status)} />
              </div>
              <h4>{acc.name}</h4>
              <p className="connect-card-desc">{acc.description}</p>
              <div className="connect-card-stats">
                <div className="connect-stat">
                  <span className="connect-stat-value">{acc.queriesTracked}</span>
                  <span className="connect-stat-label">Queries Tracked</span>
                </div>
                <button className="btn btn-ghost btn-sm">
                  <RefreshCw size={14} /> Resync
                </button>
              </div>
            </GlassCard>
          )
        })}
      </div>

      {/* Feed Status Table */}
      <h3 className="section-title fade-in-up fade-in-up-delay-4">{t('feedStatus')}</h3>
      <GlassCard className="fade-in-up fade-in-up-delay-4">
        <table className="data-table" id="feed-status-table">
          <thead>
            <tr>
              <th>Feed</th>
              <th>Items</th>
              <th>{t('lastSync')}</th>
              <th>Status</th>
              <th>{t('errors')}</th>
            </tr>
          </thead>
          <tbody>
            {feedStatus.map((row, i) => (
              <tr key={i}>
                <td style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{row.feed}</td>
                <td>{row.items.toLocaleString()}</td>
                <td>{row.lastSync}</td>
                <td><StatusBadge status={row.status} /></td>
                <td style={{ color: row.errors > 0 ? 'var(--coral)' : 'var(--green)' }}>{row.errors}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </GlassCard>
    </div>
  )
}

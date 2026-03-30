import { Activity, Wrench, ShieldCheck, Hash, AlertTriangle, Wifi } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { useLanguage } from '../context/LanguageContext'
import MetricCard from '../components/MetricCard'
import GlassCard from '../components/GlassCard'
import StatusBadge from '../components/StatusBadge'
import { metrics, alignmentTrend, redAlerts, protocolStatus } from '../data/mockData'
import './Dashboard.css'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload) return null
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip-label">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="chart-tooltip-row">
          <span style={{ color: p.color }}>●</span>
          <span>{p.name}: {p.value}%</span>
        </div>
      ))}
    </div>
  )
}

export default function Dashboard() {
  const { t } = useLanguage()

  return (
    <div className="page">
      <div className="page-header fade-in-up">
        <h1>{t('dashboardTitle')}</h1>
        <p>{t('dashboardSubtitle')}</p>
      </div>

      {/* KPI Cards */}
      <div className="page-grid grid-4" style={{ marginBottom: 'var(--space-xl)' }}>
        <MetricCard icon={Activity} label={t('inferenceScore')} value={metrics.inferenceScore} suffix="%" trend={metrics.inferenceScoreTrend} color="cyan" delay={0} />
        <MetricCard icon={Wrench} label={t('activeRemediations')} value={metrics.activeRemediations} trend={metrics.activeRemediationsTrend} color="coral" delay={0.1} />
        <MetricCard icon={ShieldCheck} label={t('verifiedFixes')} value={metrics.verifiedFixes} trend={metrics.verifiedFixesTrend} color="green" delay={0.2} />
        <MetricCard icon={Hash} label={t('tokenDensity')} value={metrics.tokenDensity} suffix="%" trend={metrics.tokenDensityTrend} color="lavender" delay={0.3} />
      </div>

      <div className="dashboard-grid">
        {/* Alignment Trend Chart */}
        <GlassCard className="chart-card fade-in-up fade-in-up-delay-2">
          <h3>{t('alignmentTrend')}</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={260}>
              <AreaChart data={alignmentTrend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="gradCyan" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00e5ff" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#00e5ff" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gradLavender" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#9b8aff" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#9b8aff" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" tick={{ fill: '#5a6480', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#5a6480', fontSize: 11 }} axisLine={false} tickLine={false} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="en" name="English" stroke="#00e5ff" fill="url(#gradCyan)" strokeWidth={2} dot={false} />
                <Area type="monotone" dataKey="fr" name="Français" stroke="#9b8aff" fill="url(#gradLavender)" strokeWidth={2} dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-legend">
            <span className="legend-item"><span className="legend-dot" style={{ background: '#00e5ff' }} /> English</span>
            <span className="legend-item"><span className="legend-dot" style={{ background: '#9b8aff' }} /> Français</span>
          </div>
        </GlassCard>

        {/* Red Alerts */}
        <GlassCard className="alerts-card fade-in-up fade-in-up-delay-3">
          <div className="alerts-header">
            <h3>
              <AlertTriangle size={16} style={{ color: 'var(--coral)' }} />
              {' '}{t('redAlerts')}
            </h3>
            <span className="badge badge-critical">{redAlerts.length}</span>
          </div>
          <div className="alerts-list">
            {redAlerts.map((alert) => (
              <div key={alert.id} className="alert-item">
                <div className="alert-item-top">
                  <span className="alert-query">{alert.query}</span>
                  <StatusBadge status={alert.severity} />
                </div>
                <p className="alert-issue">{alert.issue}</p>
                <div className="alert-meta">
                  <span className="badge badge-info">{alert.agent}</span>
                  <span className="badge badge-cyan">{alert.lang}</span>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Protocol Status */}
        <GlassCard className="protocol-card fade-in-up fade-in-up-delay-4">
          <h3>
            <Wifi size={16} style={{ color: 'var(--green)' }} />
            {' '}{t('protocolStatus')}
          </h3>
          <div className="protocol-list">
            {protocolStatus.map((proto) => (
              <div key={proto.name} className="protocol-item">
                <div className="protocol-item-left">
                  <div className="protocol-indicator" />
                  <div>
                    <div className="protocol-name">{proto.name}</div>
                    <div className="protocol-ping">Ping: {proto.lastPing}</div>
                  </div>
                </div>
                <div className="protocol-feeds">{proto.feeds} feeds</div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  )
}

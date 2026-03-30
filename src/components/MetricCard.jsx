import { TrendingUp, TrendingDown } from 'lucide-react'
import AnimatedCounter from './AnimatedCounter'
import './MetricCard.css'

export default function MetricCard({ icon: Icon, label, value, trend, suffix = '', prefix = '', color = 'cyan', delay = 0 }) {
  const isPositive = trend > 0

  return (
    <div className={`metric-card fade-in-up`} style={{ animationDelay: `${delay}s` }}>
      <div className="metric-card-header">
        <div className={`metric-card-icon icon-${color}`}>
          <Icon size={20} />
        </div>
        {trend !== undefined && (
          <div className={`metric-card-trend ${isPositive ? 'trend-up' : 'trend-down'}`}>
            {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
            <span>{isPositive ? '+' : ''}{trend}%</span>
          </div>
        )}
      </div>
      <div className="metric-card-value">
        <AnimatedCounter value={value} prefix={prefix} suffix={suffix} />
      </div>
      <div className="metric-card-label">{label}</div>
    </div>
  )
}

export default function StatusBadge({ status, label }) {
  const classMap = {
    critical: 'badge-critical',
    warning: 'badge-warning',
    success: 'badge-success',
    info: 'badge-info',
    passed: 'badge-success',
    failed: 'badge-critical',
    pending: 'badge-info',
    connected: 'badge-success',
    disconnected: 'badge-critical',
    ready: 'badge-cyan',
    deployed: 'badge-success',
    scheduled: 'badge-info',
  }

  return (
    <span className={`badge ${classMap[status] || 'badge-info'}`}>
      <span style={{
        width: 6,
        height: 6,
        borderRadius: '50%',
        background: 'currentColor',
        display: 'inline-block',
        animation: status === 'critical' ? 'pulse 2s infinite' : 'none',
      }} />
      {label || status}
    </span>
  )
}

import './GlassCard.css'

export default function GlassCard({ children, className = '', glow, onClick, style }) {
  return (
    <div
      className={`glass-card-component ${glow ? `glow-${glow}` : ''} ${onClick ? 'clickable' : ''} ${className}`}
      onClick={onClick}
      style={style}
    >
      {children}
    </div>
  )
}

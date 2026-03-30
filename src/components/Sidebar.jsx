import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Plug, Stethoscope, Wrench, ShieldCheck, Languages, Zap } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import './Sidebar.css'

const navItems = [
  { to: '/', icon: LayoutDashboard, key: 'dashboard' },
  { to: '/connect', icon: Plug, key: 'connect' },
  { to: '/diagnose', icon: Stethoscope, key: 'diagnose' },
  { to: '/remediate', icon: Wrench, key: 'remediate' },
  { to: '/verify', icon: ShieldCheck, key: 'verify' },
]

export default function Sidebar() {
  const { t, lang, toggleLang } = useLanguage()

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">
          <Zap size={22} />
        </div>
        <div className="logo-text">
          <span className="logo-name">VisiMind</span>
          <span className="logo-tag">AI Remediation Layer</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-label">WORKFLOW</div>
        {navItems.map((item, i) => (
          <NavLink
            key={item.key}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <item.icon size={18} />
            <span>{t(item.key)}</span>
            {i > 0 && <span className="nav-step">{i}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="lang-toggle" onClick={toggleLang}>
          <Languages size={16} />
          <span>{lang === 'en' ? 'Français' : 'English'}</span>
        </button>
        <div className="sidebar-version">v1.0 — "The Rush"</div>
      </div>
    </aside>
  )
}

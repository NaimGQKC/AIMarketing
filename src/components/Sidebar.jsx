import { NavLink, useNavigate } from 'react-router-dom'
import { LayoutDashboard, Wrench, Activity, User, LogOut, Zap } from 'lucide-react'
import { clearToken } from '../api/client'
import './Sidebar.css'

const navItems = [
  { to: '/monitor', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/dashboard', icon: Activity, label: 'Audit' },
  { to: '/fixkit', icon: Wrench, label: 'Fix Kit' },
]

export default function Sidebar() {
  const navigate = useNavigate()

  const handleSignOut = () => {
    clearToken()
    navigate('/')
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">
          <Zap size={22} />
        </div>
        <div className="logo-text">
          <span className="logo-name">VisiMind</span>
          <span className="logo-tag">AI Visibility Platform</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <item.icon size={18} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <NavLink to="/setup" className="nav-link" style={{ marginBottom: '8px' }}>
          <User size={16} />
          <span>Brand Profile</span>
        </NavLink>
        <button className="lang-toggle" onClick={handleSignOut}>
          <LogOut size={16} />
          <span>Sign Out</span>
        </button>
        <div className="sidebar-version">v2.0 (Pilot)</div>
      </div>
    </aside>
  )
}

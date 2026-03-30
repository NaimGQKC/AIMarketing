import { Search, Bell } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useLocation } from 'react-router-dom'
import './Header.css'

const routeNames = {
  '/': 'dashboard',
  '/connect': 'connect',
  '/diagnose': 'diagnose',
  '/remediate': 'remediate',
  '/verify': 'verify',
}

export default function Header() {
  const { t } = useLanguage()
  const location = useLocation()
  const currentRoute = routeNames[location.pathname] || 'dashboard'

  return (
    <header className="app-header">
      <div className="header-breadcrumb">
        <span className="breadcrumb-root">VisiMind</span>
        <span className="breadcrumb-sep">/</span>
        <span className="breadcrumb-current">{t(currentRoute)}</span>
      </div>

      <div className="header-actions">
        <div className="header-search">
          <Search size={16} />
          <input type="text" placeholder={t('search')} />
        </div>
        <button className="header-notification" id="notification-bell">
          <Bell size={18} />
          <span className="notification-badge">3</span>
        </button>
        <div className="header-avatar" id="user-avatar">
          <span>AP</span>
        </div>
      </div>
    </header>
  )
}

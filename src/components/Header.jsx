import { Tag } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useBrand } from '../context/BrandContext'
import { useLocation } from 'react-router-dom'
import './Header.css'

const routeNames = {
  '/dashboard': 'dashboard',
  '/connect': 'connect',
  '/diagnose': 'diagnose',
  '/remediate': 'remediate',
  '/fixkit': 'remediate',
  '/verify': 'verify',
  '/monitor': 'monitor',
  '/roadmap': 'roadmap',
  '/outreach': 'outreach',
}

export default function Header() {
  const { t } = useLanguage()
  const location = useLocation()
  const { selectedBrandId, setSelectedBrandId, availableBrands } = useBrand()
  const currentRoute = routeNames[location.pathname] || 'dashboard'

  return (
    <header className="app-header">
      <div className="header-breadcrumb">
        <span className="breadcrumb-root">VisiMind</span>
        <span className="breadcrumb-sep">/</span>
        <span className="breadcrumb-current">{t(currentRoute)}</span>
      </div>

      <div className="header-actions">
        {/* Global Brand Selector */}
        {availableBrands.length > 1 && (
          <div className="header-brand-select">
            <div className="brand-select-icon">
              <Tag size={14} />
            </div>
            <select
              value={selectedBrandId}
              onChange={(e) => setSelectedBrandId(e.target.value)}
              className="brand-select-input"
            >
              <option value="all">{t('allBrands') || 'All Brands'}</option>
              {availableBrands.map((brand) => (
                <option key={brand.id} value={brand.id}>
                  {brand.brand_name || brand.name}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>
    </header>
  )
}

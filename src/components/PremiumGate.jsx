import { Lock } from 'lucide-react'
import './PremiumGate.css'

export default function PremiumGate({ pageName, description, children }) {
  return (
    <div className="premium-gate">
      <div className="premium-gate__content">
        {children}
      </div>
      <div className="premium-gate__overlay">
        <div className="premium-gate__card">
          <div className="premium-gate__icon-wrap">
            <Lock size={24} />
          </div>
          <h2 className="premium-gate__title">Unlock {pageName}</h2>
          <p className="premium-gate__subtitle">
            Get access to {description} with a VisiMind strategy session.
          </p>
          <a href="#book-call" className="premium-gate__cta">
            Book a Strategy Call &rarr;
          </a>
          <p className="premium-gate__contact">
            Contact us: <a href="mailto:alex@visimind.ai">alex@visimind.ai</a>
          </p>
        </div>
      </div>
    </div>
  )
}

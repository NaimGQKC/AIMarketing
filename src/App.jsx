import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import { BrandProvider } from './context/BrandContext'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import Connect from './pages/Connect'
import Diagnose from './pages/Diagnose'
import Remediate from './pages/Remediate'
import Verify from './pages/Verify'
import Roadmap from './pages/Roadmap'
import './App.css'

export default function App() {
  return (
    <BrandProvider>
      <div className="app-layout">
        <Sidebar />
        <div className="app-main">
          <Header />
          <main className="app-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/connect" element={<Connect />} />
              <Route path="/diagnose" element={<Diagnose />} />
              <Route path="/remediate" element={<Remediate />} />
              <Route path="/verify" element={<Verify />} />
              <Route path="/roadmap" element={<Roadmap />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrandProvider>
  )
}

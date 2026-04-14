import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import { BrandProvider } from './context/BrandContext'
import Header from './components/Header'
import ProtectedRoute from './components/ProtectedRoute'

import LandingPage from './pages/LandingPage'
import SignIn from './pages/SignIn'
import SignUp from './pages/SignUp'
import CompanySetup from './pages/CompanySetup'
import Dashboard from './pages/Dashboard'
import Connect from './pages/Connect'
import Diagnose from './pages/Diagnose'
import Remediate from './pages/Remediate'
import Verify from './pages/Verify'
import Roadmap from './pages/Roadmap'
import Outreach from './pages/Outreach'
import './App.css'

function AppLayout({ children }) {
  return (
    <BrandProvider>
      <div className="app-layout">
        <Sidebar />
        <div className="app-main">
          <Header />
          <main className="app-content">{children}</main>
        </div>
      </div>
    </BrandProvider>
  )
}

export default function App() {
  return (
    <Routes>
      {/* Public routes -- no sidebar/header */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/signin" element={<SignIn />} />
      <Route path="/signup" element={<SignUp />} />

      {/* Protected route -- no sidebar/header */}
      <Route
        path="/setup"
        element={
          <ProtectedRoute>
            <CompanySetup />
          </ProtectedRoute>
        }
      />

      {/* Protected app routes -- with sidebar/header */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <AppLayout><Dashboard /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/connect"
        element={
          <ProtectedRoute>
            <AppLayout><Connect /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/diagnose"
        element={
          <ProtectedRoute>
            <AppLayout><Diagnose /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/fixkit"
        element={
          <ProtectedRoute>
            <AppLayout><Remediate /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/remediate"
        element={
          <ProtectedRoute>
            <AppLayout><Remediate /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/monitor"
        element={
          <ProtectedRoute>
            <AppLayout><Verify /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/verify"
        element={
          <ProtectedRoute>
            <AppLayout><Verify /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/roadmap"
        element={
          <ProtectedRoute>
            <AppLayout><Roadmap /></AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/outreach"
        element={
          <ProtectedRoute>
            <AppLayout><Outreach /></AppLayout>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

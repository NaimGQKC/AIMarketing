import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Zap, Eye, EyeOff, Mail, Lock } from 'lucide-react'
import { apiFetch, setToken } from '../api/client'

export default function SignIn() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPwd, setShowPwd] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const data = await apiFetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })
      setToken(data.access_token || data.token)

      // Check if user has a brand
      try {
        const me = await apiFetch('/auth/me')
        if (me.has_brand) {
          navigate('/dashboard')
        } else {
          navigate('/setup')
        }
      } catch {
        navigate('/setup')
      }
    } catch (err) {
      setError(err.message || 'Invalid email or password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#060a14] flex items-center justify-center px-6">
      {/* Background effects */}
      <div className="absolute top-1/3 left-1/3 w-[400px] h-[400px] bg-[#00e5ff]/[0.03] rounded-full blur-[120px]" />
      <div className="absolute bottom-1/3 right-1/3 w-[300px] h-[300px] bg-[#9b8aff]/[0.03] rounded-full blur-[100px]" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex items-center gap-2 text-[#f0f2f8] font-headline font-bold text-lg mb-6">
              <Zap size={22} className="text-[#00e5ff]" />
              VisiMind
            </Link>
            <h1 className="font-headline text-2xl font-bold text-[#f0f2f8]">Welcome back</h1>
            <p className="text-[#8b95b0] text-sm mt-1">Sign in to your VisiMind account</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-[#8b95b0] text-sm font-medium mb-1.5">Email</label>
              <div className="relative">
                <Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[#5a6480]" />
                <input
                  type="email"
                  required
                  placeholder="you@company.com"
                  value={email}
                  onChange={(e) => { setEmail(e.target.value); if (error) setError('') }}
                  className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg pl-11 pr-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                />
              </div>
            </div>

            <div>
              <label className="block text-[#8b95b0] text-sm font-medium mb-1.5">Password</label>
              <div className="relative">
                <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[#5a6480]" />
                <input
                  type={showPwd ? 'text' : 'password'}
                  required
                  placeholder="Your password"
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); if (error) setError('') }}
                  className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg pl-11 pr-11 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                />
                <button
                  type="button"
                  onClick={() => setShowPwd(!showPwd)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-[#5a6480] hover:text-[#8b95b0] transition-colors"
                >
                  {showPwd ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {error && <p className="text-[#ff4c6a] text-sm">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.35)] hover:-translate-y-0.5 transition-all duration-250 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-[#8b95b0] text-sm mt-6">
            Don't have an account?{' '}
            <Link to="/signup" className="text-[#00e5ff] hover:underline">
              Sign up
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Zap, ArrowLeft, ShieldCheck } from 'lucide-react'
import { apiFetch } from '../api/client'

export default function VerifyEmail() {
  const navigate = useNavigate()
  const [code, setCode] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [resending, setResending] = useState(false)
  const [devCode, setDevCode] = useState(null)

  // Check if already verified
  useEffect(() => {
    apiFetch('/auth/me')
      .then(data => {
        if (data.email_verified) navigate('/setup', { replace: true })
      })
      .catch(() => {})
  }, [navigate])

  const handleVerify = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await apiFetch('/auth/verify-email', {
        method: 'POST',
        body: JSON.stringify({ code: code.trim() }),
      })
      navigate('/setup')
    } catch (err) {
      setError(err.message || 'Invalid code. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleResend = async () => {
    setResending(true)
    setError('')
    try {
      const data = await apiFetch('/auth/resend-code', { method: 'POST' })
      if (data._dev_verification_code) {
        setDevCode(data._dev_verification_code)
      }
    } catch (err) {
      setError(err.message || 'Could not resend code.')
    } finally {
      setResending(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#060a14] flex items-center justify-center px-6">
      <div className="absolute top-1/3 left-1/3 w-[400px] h-[400px] bg-[#00e5ff]/[0.03] rounded-full blur-[120px]" />
      <div className="absolute bottom-1/3 right-1/3 w-[300px] h-[300px] bg-[#9b8aff]/[0.03] rounded-full blur-[100px]" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 w-full max-w-md"
      >
        <Link to="/" className="inline-flex items-center gap-2 text-[#8b95b0] hover:text-[#f0f2f8] text-sm font-medium transition-colors mb-6">
          <ArrowLeft size={16} />
          Back to home
        </Link>
        <div className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-8">
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex items-center gap-2 text-[#f0f2f8] font-headline font-bold text-lg mb-6">
              <Zap size={22} className="text-[#00e5ff]" />
              VisiMind
            </Link>
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-[#00e5ff]/10 border border-[#00e5ff]/20 flex items-center justify-center">
              <ShieldCheck size={32} className="text-[#00e5ff]" />
            </div>
            <h1 className="font-headline text-2xl font-bold text-[#f0f2f8]">Verify your email</h1>
            <p className="text-[#8b95b0] text-sm mt-2 leading-relaxed">
              We sent a 6-digit code to your work email.<br />
              Enter it below to start your audit.
            </p>
          </div>

          <form onSubmit={handleVerify} className="space-y-4">
            <div>
              <input
                type="text"
                inputMode="numeric"
                maxLength={6}
                required
                placeholder="000000"
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg px-4 py-4 text-center text-2xl tracking-[0.5em] font-mono focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480] placeholder:tracking-[0.5em]"
                autoFocus
              />
            </div>

            {error && <p className="text-[#ff4c6a] text-sm text-center">{error}</p>}

            {devCode && (
              <div className="bg-[#00e5ff]/5 border border-[#00e5ff]/20 rounded-lg p-3 text-center">
                <p className="text-[10px] text-[#00e5ff] uppercase tracking-widest font-bold mb-1">Dev mode</p>
                <p className="text-[#f0f2f8] font-mono text-lg tracking-widest">{devCode}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || code.length < 6}
              className="w-full py-3 bg-[#00e5ff] text-[#0a0e1a] font-semibold rounded-xl shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.35)] hover:-translate-y-0.5 transition-all duration-250 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Verifying...' : 'Verify Email'}
            </button>
          </form>

          <p className="text-center text-[#8b95b0] text-sm mt-6">
            Didn't get the code?{' '}
            <button
              onClick={handleResend}
              disabled={resending}
              className="text-[#00e5ff] hover:underline disabled:opacity-50 cursor-pointer"
            >
              {resending ? 'Sending...' : 'Resend code'}
            </button>
          </p>
        </div>
      </motion.div>
    </div>
  )
}

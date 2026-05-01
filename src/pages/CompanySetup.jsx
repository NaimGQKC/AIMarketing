import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Zap, Building2, Link as LinkIcon, Tag, Users, ArrowRight, ArrowLeft } from 'lucide-react'
import { apiFetch, getToken, setToken } from '../api/client'
import { useBrand } from '../context/BrandContext'

const CATEGORIES = [
  'Fashion',
  'Beauty',
  'Food & Beverage',
  'Technology',
  'Retail',
  'Other',
]

export default function CompanySetup() {
  const navigate = useNavigate()
  const { refreshBrands } = useBrand()
  const [form, setForm] = useState(() => {
    try {
      const pilot = JSON.parse(localStorage.getItem('visimind_pilot_data') || '{}')
      return {
        brand_name: pilot.brand_name || '',
        primary_url: pilot.primary_url || '',
        product_category: '',
        top_competitor: '',
      }
    } catch { return { brand_name: '', primary_url: '', product_category: '', top_competitor: '' } }
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const update = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // If no token, create a guest account first
      if (!getToken()) {
        const guest = await apiFetch('/auth/guest', { method: 'POST' })
        setToken(guest.token)
      }

      await apiFetch('/brands', {
        method: 'POST',
        body: JSON.stringify({
          ...form,
          language_pair: 'EN/FR',
        }),
      })
      localStorage.removeItem('visimind_pilot_data')
      await refreshBrands()
      navigate('/dashboard?autorun=1')
    } catch (err) {
      setError(err.message || 'Could not create brand. Please try again.')
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
        className="relative z-10 w-full max-w-lg"
      >
        <Link to="/dashboard" className="inline-flex items-center gap-2 text-[#8b95b0] hover:text-[#f0f2f8] text-sm font-medium transition-colors mb-6">
          <ArrowLeft size={16} />
          Back to dashboard
        </Link>
        <div className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <Link to="/dashboard" className="inline-flex items-center gap-2 text-[#f0f2f8] font-['Outfit'] font-bold text-lg mb-6">
              <Zap size={22} className="text-[#00e5ff]" />
              VisiMind
            </Link>
            <h1 className="font-['Outfit'] text-2xl font-bold text-[#f0f2f8]">Let's set up your brand</h1>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Brand Name */}
            <div>
              <label className="block text-[#8b95b0] text-sm font-medium mb-1.5">Brand Name</label>
              <div className="relative">
                <Building2 size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[#5a6480]" />
                <input
                  type="text"
                  required
                  placeholder="Your brand name"
                  value={form.brand_name}
                  onChange={update('brand_name')}
                  className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg pl-11 pr-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                />
              </div>
            </div>

            {/* Primary URL */}
            <div>
              <label className="block text-[#8b95b0] text-sm font-medium mb-1.5">Primary URL</label>
              <div className="relative">
                <LinkIcon size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[#5a6480]" />
                <input
                  type="url"
                  placeholder="https://yourbrand.com"
                  value={form.primary_url}
                  onChange={update('primary_url')}
                  className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg pl-11 pr-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                />
              </div>
            </div>

            {/* Product Category */}
            <div>
              <label className="block text-[#8b95b0] text-sm font-medium mb-1.5">Product Category</label>
              <div className="relative">
                <Tag size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[#5a6480]" />
                <select
                  required
                  value={form.product_category}
                  onChange={update('product_category')}
                  className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg pl-11 pr-10 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors appearance-none cursor-pointer"
                  style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%235a6480' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E")`,
                    backgroundRepeat: 'no-repeat',
                    backgroundPosition: 'right 16px center',
                  }}
                >
                  <option value="" disabled className="bg-[#0f1424] text-[#5a6480]">
                    Select a category
                  </option>
                  {CATEGORIES.map((cat) => (
                    <option key={cat} value={cat} className="bg-[#0f1424] text-[#f0f2f8]">
                      {cat}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Top Competitor */}
            <div>
              <label className="block text-[#8b95b0] text-sm font-medium mb-1.5">Top Competitor</label>
              <div className="relative">
                <Users size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-[#5a6480]" />
                <input
                  type="text"
                  placeholder="Main competitor brand"
                  value={form.top_competitor}
                  onChange={update('top_competitor')}
                  className="w-full bg-white/5 border border-white/10 text-[#f0f2f8] rounded-lg pl-11 pr-4 py-3 focus:border-[#00e5ff] focus:outline-none transition-colors placeholder:text-[#5a6480]"
                />
              </div>
            </div>

            {error && <p className="text-[#ff4c6a] text-sm">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 bg-[#00e5ff] text-[#0a0e1a] font-semibold text-lg rounded-xl shadow-[0_0_20px_rgba(0,229,255,0.3)] hover:shadow-[0_0_30px_rgba(0,229,255,0.35)] hover:-translate-y-0.5 transition-all duration-250 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                'Setting up...'
              ) : (
                <>
                  Run First Audit
                  <ArrowRight size={20} />
                </>
              )}
            </button>
          </form>
        </div>
      </motion.div>
    </div>
  )
}

/**
 * VisiMind — API Client
 * Thin fetch wrapper for all backend API calls.
 * Falls back to null if backend is unreachable (frontend uses local mock data).
 */

const BASE = ''  // Same origin via Vite proxy

async function request(endpoint, options = {}) {
  try {
    const response = await fetch(`${BASE}${endpoint}`, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
    })

    if (!response.ok) {
      console.warn(`API ${endpoint}: ${response.status}`)
      return null
    }

    return await response.json()
  } catch (err) {
    console.warn(`API ${endpoint} unreachable:`, err.message)
    return null
  }
}

// --- Dashboard ---
export const api = {
  dashboard: {
    metrics: (brandId) => request(`/api/dashboard/metrics${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    alerts: (brandId) => request(`/api/dashboard/alerts${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    trend: (brandId) => request(`/api/dashboard/trend${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    protocols: () => request('/api/dashboard/protocols'),
  },

  connect: {
    integrations: () => request('/api/connect/integrations'),
    sync: (provider) => request(`/api/connect/integrations/${provider}/sync`, { method: 'POST' }),
    feeds: () => request('/api/connect/feeds'),
  },

  diagnose: {
    gaps: (brandId) => request(`/api/diagnose/gaps${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    gap: (id) => request(`/api/diagnose/gaps/${id}`),
    gapFixKit: (gapId) => request(`/api/diagnose/gaps/${gapId}/fix-kit`),
    deployKit: (kitId) => request(`/api/remediate/kits/${kitId}/deploy`, { method: 'POST' }),
    parity: (brandId) => request(`/api/diagnose/parity${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    probe: (query, lang = 'EN', iterations = 50) =>
      request('/api/diagnose/probe', {
        method: 'POST',
        body: JSON.stringify({ query, lang, iterations }),
      }),
    fertility: (textEn, textFr) =>
      request('/api/diagnose/fertility', {
        method: 'POST',
        body: JSON.stringify({ text_en: textEn, text_fr: textFr }),
      }),
  },

  remediate: {
    kits: (brandId) => request(`/api/remediate/kits${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    preview: (kitId) => request(`/api/remediate/kits/${kitId}/preview`),
    deploy: (kitId) => request(`/api/remediate/kits/${kitId}/deploy`, { method: 'POST' }),
    compare: () => request('/api/remediate/compare'),
    dpo: (productId) => request(`/api/remediate/dpo/${productId}`),
    graph: (brandId) => request(`/api/remediate/graph/${brandId}`),
  },

  verify: {
    schedule: () => request('/api/verify/schedule'),
    timeline: () => request('/api/verify/timeline'),
    confidence: () => request('/api/verify/confidence'),
    reasoning: () => request('/api/verify/reasoning'),
    efficiency: () => request('/api/verify/efficiency'),
    raft: (brandId) => request(`/api/verify/raft${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    kg: (brandId) => request(`/api/verify/kg${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    runAudit: (auditId) => request(`/api/verify/audit/${auditId}/run`, { method: 'POST' }),
  },

  eee: {
    syndication: (brandId) => request(`/api/eee/syndication${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    freshness: (brandId) => request(`/api/eee/freshness${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    authority: (brandId) => request(`/api/eee/authority${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    priority: (brandId) => request(`/api/eee/priority${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    roadmap: (brandId) => request(`/api/eee/roadmap${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    replies: (brandId) => request(`/api/eee/replies${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    pings: (brandId) => request(`/api/eee/pings${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    drift: (brandId) => request(`/api/eee/drift${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    tax: (brandId) => request(`/api/eee/tax${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
    moat: (brandId) => request(`/api/eee/moat${brandId && brandId !== 'all' ? `?brand_id=${brandId}` : ''}`),
  },

  tasks: {
    status: (taskId) => request(`/api/tasks/${taskId}`),
  },

  ingest: {
    batch: async (files, brandName) => {
      try {
        const formData = new FormData()
        // Append all files under the key 'files' to match the FastAPI List[UploadFile] expecting name 'files'
        Array.from(files).forEach((file) => {
          formData.append('files', file)
        })
        formData.append('brand_name', brandName)
        const response = await fetch(`${BASE}/api/ingest/batch`, {
          method: 'POST',
          body: formData,
        })
        if (!response.ok) return null
        return await response.json()
      } catch (err) {
        console.warn('API /api/ingest/batch unreachable:', err.message)
        return null
      }
    },
    brands: () => request('/api/ingest/brands'),
  },

  health: () => request('/api/health'),
}

export default api

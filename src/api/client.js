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
    metrics: () => request('/api/dashboard/metrics'),
    alerts: () => request('/api/dashboard/alerts'),
    trend: () => request('/api/dashboard/trend'),
    protocols: () => request('/api/dashboard/protocols'),
  },

  connect: {
    integrations: () => request('/api/connect/integrations'),
    sync: (provider) => request(`/api/connect/integrations/${provider}/sync`, { method: 'POST' }),
    feeds: () => request('/api/connect/feeds'),
  },

  diagnose: {
    gaps: () => request('/api/diagnose/gaps'),
    gap: (id) => request(`/api/diagnose/gaps/${id}`),
    parity: () => request('/api/diagnose/parity'),
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
    kits: () => request('/api/remediate/kits'),
    preview: (kitId) => request(`/api/remediate/kits/${kitId}/preview`),
    deploy: (kitId) => request(`/api/remediate/kits/${kitId}/deploy`, { method: 'POST' }),
    compare: () => request('/api/remediate/compare'),
  },

  verify: {
    schedule: () => request('/api/verify/schedule'),
    timeline: () => request('/api/verify/timeline'),
    confidence: () => request('/api/verify/confidence'),
    reasoning: () => request('/api/verify/reasoning'),
    runAudit: (auditId) => request(`/api/verify/audit/${auditId}/run`, { method: 'POST' }),
  },

  tasks: {
    status: (taskId) => request(`/api/tasks/${taskId}`),
  },

  health: () => request('/api/health'),
}

export default api

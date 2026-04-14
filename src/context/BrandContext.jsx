import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { apiFetch, getToken } from '../api/client'
import api from '../api/client'

const BrandContext = createContext()

export function BrandProvider({ children }) {
  const [selectedBrandId, setSelectedBrandId] = useState(null)
  const [availableBrands, setAvailableBrands] = useState([])

  const refreshBrands = useCallback(async () => {
    // Try authenticated v1 brands first (user's brand_profiles)
    if (getToken()) {
      try {
        const brands = await apiFetch('/brands')
        if (brands && Array.isArray(brands) && brands.length > 0) {
          setAvailableBrands(brands)
          // Auto-select first brand if none selected
          setSelectedBrandId((prev) => prev || brands[0].id)
          return
        }
      } catch {
        // Fall through to legacy endpoint
      }
    }
    // Fallback to legacy seeded brands
    const brands = await api.ingest.brands()
    if (brands && Array.isArray(brands)) {
      setAvailableBrands(brands)
      if (brands.length > 0) {
        setSelectedBrandId((prev) => prev || brands[0].id)
      }
    }
  }, [])

  useEffect(() => {
    refreshBrands()
  }, [refreshBrands])

  // Derive the currently selected brand object
  const selectedBrand = availableBrands.find((b) => b.id === selectedBrandId) || null

  const value = {
    selectedBrandId,
    setSelectedBrandId,
    selectedBrand,
    availableBrands,
    refreshBrands,
  }

  return (
    <BrandContext.Provider value={value}>
      {children}
    </BrandContext.Provider>
  )
}

export function useBrand() {
  const context = useContext(BrandContext)
  if (context === undefined) {
    throw new Error('useBrand must be used within a BrandProvider')
  }
  return context
}

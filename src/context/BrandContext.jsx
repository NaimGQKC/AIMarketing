import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api from '../api/client'

const BrandContext = createContext()

export function BrandProvider({ children }) {
  const [selectedBrandId, setSelectedBrandId] = useState('all')
  const [availableBrands, setAvailableBrands] = useState([])

  const refreshBrands = useCallback(async () => {
    const brands = await api.ingest.brands()
    if (brands && Array.isArray(brands)) {
      setAvailableBrands(brands)
    }
  }, [])

  useEffect(() => {
    refreshBrands()
  }, [refreshBrands])

  const value = {
    selectedBrandId,
    setSelectedBrandId,
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

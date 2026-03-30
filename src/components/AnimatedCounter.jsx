import { useEffect, useState, useRef } from 'react'

export default function AnimatedCounter({ value, duration = 1200, prefix = '', suffix = '' }) {
  const [display, setDisplay] = useState(0)
  const ref = useRef(null)
  const startedRef = useRef(false)

  useEffect(() => {
    if (startedRef.current) return
    startedRef.current = true

    const start = 0
    const end = typeof value === 'number' ? value : parseFloat(value) || 0
    const startTime = performance.now()

    function animate(now) {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3) // ease-out cubic
      const current = start + (end - start) * eased

      setDisplay(Number.isInteger(end) ? Math.round(current) : parseFloat(current.toFixed(2)))

      if (progress < 1) {
        ref.current = requestAnimationFrame(animate)
      }
    }

    ref.current = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(ref.current)
  }, [value, duration])

  return <span className="animated-counter">{prefix}{display}{suffix}</span>
}

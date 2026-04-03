import { useState, useRef } from 'react'
import { UploadCloud, FileText, CheckCircle, AlertTriangle } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useBrand } from '../context/BrandContext'
import api from '../api/client'
import GlassCard from './GlassCard'
import './DataIngester.css'

export default function DataIngester() {
  const { t } = useLanguage()
  const { availableBrands, setSelectedBrandId, refreshBrands } = useBrand()
  
  const [files, setFiles] = useState([])
  const [brandName, setBrandName] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  
  const [uploadStatus, setUploadStatus] = useState('idle') // idle, uploading, polling, success, error
  const [progress, setProgress] = useState(0)
  const [errorMsg, setErrorMsg] = useState('')
  
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFiles(prev => [...prev, ...Array.from(e.dataTransfer.files)])
    }
  }

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFiles(prev => [...prev, ...Array.from(e.target.files)])
    }
  }

  const removeFile = (indexToRemove) => {
    setFiles(prev => prev.filter((_, idx) => idx !== indexToRemove))
  }

  const handleUpload = async () => {
    if (files.length === 0 || !brandName.trim()) return

    setUploadStatus('uploading')
    setProgress(10)
    setErrorMsg('')

    try {
      const result = await api.ingest.batch(files, brandName.trim())
      
      if (!result || result.error) {
        setUploadStatus('error')
        setErrorMsg(result?.error || 'Failed to upload to server')
        return
      }

      const { task_id } = result
      setUploadStatus('polling')
      
      // Poll for completion
      const pollInterval = setInterval(async () => {
        const taskStatus = await api.tasks.status(task_id)
        
        if (!taskStatus) return

        if (taskStatus.status === 'completed') {
          clearInterval(pollInterval)
          setUploadStatus('success')
          setProgress(100)
          
          // Switch global brand context to the new brand so they see the result
          if (taskStatus.result && taskStatus.result.brand) {
            // Refresh the brand list so the dropdown picks up the new brand
            await refreshBrands()
            const slug = taskStatus.result.brand.toLowerCase().replace(/ /g, '-').replace(/'/g, '')
            setSelectedBrandId(slug)
          }

          // Reset after a few seconds
          setTimeout(() => {
            setFiles([])
            setUploadStatus('idle')
            setProgress(0)
          }, 3000)
          
        } else if (taskStatus.status === 'failed') {
          clearInterval(pollInterval)
          setUploadStatus('error')
          setErrorMsg(taskStatus.error || 'Processing failed')
        } else {
          // Update progress based on total
          if (taskStatus.total > 0) {
            const currentProgress = Math.max(10, Math.round((taskStatus.progress / taskStatus.total) * 100))
            setProgress(currentProgress)
          } else {
            setProgress(p => Math.min(90, p + 5)) // Fake progress if total unknown
          }
        }
      }, 1000)

    } catch (err) {
      setUploadStatus('error')
      setErrorMsg(err.message)
    }
  }

  return (
    <GlassCard className="data-ingester fade-in-up">
      <div className="ingester-header">
        <UploadCloud size={20} className="icon-cyan" />
        <h3>{t('batchIngestion') || 'Batch Probe Ingestion'}</h3>
      </div>
      
      <div className="ingester-form">
        <div className="form-group">
          <label>Brand Name</label>
          <input 
            type="text" 
            className="brand-input" 
            placeholder="e.g. SSENSE or Mackage"
            list="brands-list"
            value={brandName}
            onChange={(e) => setBrandName(e.target.value)}
            disabled={uploadStatus === 'polling' || uploadStatus === 'uploading'}
          />
          <datalist id="brands-list">
            {availableBrands.map((brand) => (
              <option key={brand.id} value={brand.name} />
            ))}
          </datalist>
        </div>

        <div className="form-group">
          <label>Dataset Files (.txt, .md)</label>
          <div 
            className={`dropzone ${isDragging ? 'active' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              style={{ display: 'none' }} 
              accept=".txt,.md,.json"
              multiple
              onChange={handleFileSelect}
            />
            <UploadCloud size={28} className="dropzone-icon" />
            <span className="dropzone-text">Click or drag files to this area</span>
            <span className="dropzone-sub">Upload multiple files to process as a batch</span>
          </div>

          {files.length > 0 && (
            <div className="file-list">
              {files.map((f, i) => (
                <div key={`${f.name}-${i}`} className="file-item fade-in-up">
                  <div className="file-item-info">
                    <FileText size={16} />
                    <span className="file-item-name">{f.name}</span>
                    <span className="file-item-size">({(f.size / 1024).toFixed(1)} KB)</span>
                  </div>
                  <button 
                    className="file-item-remove"
                    onClick={(e) => { e.stopPropagation(); removeFile(i); }}
                    disabled={uploadStatus === 'polling' || uploadStatus === 'uploading'}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {uploadStatus === 'error' && (
          <div className="alert-error" style={{ color: 'var(--coral)', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={16} />
            {errorMsg}
          </div>
        )}

        <div className="ingester-footer">
          {uploadStatus === 'idle' || uploadStatus === 'error' ? (
            <button 
              className="btn btn-primary" 
              onClick={handleUpload}
              disabled={files.length === 0 || !brandName.trim()}
            >
              Upload & Process ({files.length})
            </button>
          ) : uploadStatus === 'success' ? (
            <div className="ingest-progress">
              <CheckCircle size={20} style={{ color: 'var(--green)' }} />
              <span style={{ color: 'var(--green)' }}>Analysis complete!</span>
            </div>
          ) : (
            <div className="ingest-progress">
              <div className="ingest-bar-container">
                <div className="ingest-bar" style={{ width: `${progress}%` }} />
              </div>
              <span className="ingest-status">
                {uploadStatus === 'uploading' ? 'Uploading...' : `Analyzing ${progress}%`}
              </span>
            </div>
          )}
        </div>
      </div>
    </GlassCard>
  )
}

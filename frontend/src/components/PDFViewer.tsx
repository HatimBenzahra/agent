import { useState, useEffect } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import {
  X,
  ZoomIn,
  ZoomOut,
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Minimize2,
  FileText,
  Loader2,
  Download,
  RotateCw
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import 'react-pdf/dist/Page/AnnotationLayer.css'
import 'react-pdf/dist/Page/TextLayer.css'

// Set up the worker
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`

type PDFViewerProps = {
  projectId: string
  filePath: string
  onClose: () => void
  isFullscreen?: boolean
  onToggleFullscreen?: () => void
}

const API_BASE = 'http://localhost:8000'

export function PDFViewer({
  projectId,
  filePath,
  onClose,
  isFullscreen,
  onToggleFullscreen
}: PDFViewerProps) {
  const [numPages, setNumPages] = useState<number>(0)
  const [pageNumber, setPageNumber] = useState<number>(1)
  const [scale, setScale] = useState<number>(1.0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [pdfUrl, setPdfUrl] = useState<string | null>(null)

  useEffect(() => {
    // Clean the file path - remove leading slash if present
    const cleanPath = filePath.startsWith('/') ? filePath.slice(1) : filePath
    // Construct the URL for the PDF file
    const url = `${API_BASE}/api/projects/${projectId}/files/content?path=${encodeURIComponent(cleanPath)}&raw=true`
    setPdfUrl(url)
  }, [projectId, filePath])

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages)
    setIsLoading(false)
    setError(null)
  }

  const onDocumentLoadError = (error: Error) => {
    console.error('PDF load error:', error)
    setError('Failed to load PDF')
    setIsLoading(false)
  }

  const goToPrevPage = () => {
    setPageNumber(prev => Math.max(prev - 1, 1))
  }

  const goToNextPage = () => {
    setPageNumber(prev => Math.min(prev + 1, numPages))
  }

  const zoomIn = () => {
    setScale(prev => Math.min(prev + 0.25, 3.0))
  }

  const zoomOut = () => {
    setScale(prev => Math.max(prev - 0.25, 0.5))
  }

  const resetZoom = () => {
    setScale(1.0)
  }

  const handleDownload = () => {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank')
    }
  }

  const fileName = filePath.split('/').pop() || 'document.pdf'

  return (
    <div className="h-full flex flex-col bg-zinc-900">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800 bg-zinc-900/95 glass-subtle">
        <div className="flex items-center gap-3 min-w-0">
          <div className="p-1.5 rounded-lg bg-red-500/10">
            <FileText size={16} className="text-red-400" />
          </div>
          <div className="min-w-0">
            <h3 className="text-sm font-medium text-zinc-200 truncate">{fileName}</h3>
            {numPages > 0 && (
              <p className="text-xs text-zinc-500">{numPages} page{numPages > 1 ? 's' : ''}</p>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1">
          {/* Zoom controls */}
          <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-zinc-800/50 mr-2">
            <button
              onClick={zoomOut}
              disabled={scale <= 0.5}
              className="p-1.5 rounded-md hover:bg-zinc-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              title="Zoom out"
            >
              <ZoomOut size={14} className="text-zinc-400" />
            </button>
            <button
              onClick={resetZoom}
              className="px-2 py-1 text-xs text-zinc-400 hover:text-zinc-200 transition-colors min-w-[48px]"
              title="Reset zoom"
            >
              {Math.round(scale * 100)}%
            </button>
            <button
              onClick={zoomIn}
              disabled={scale >= 3.0}
              className="p-1.5 rounded-md hover:bg-zinc-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              title="Zoom in"
            >
              <ZoomIn size={14} className="text-zinc-400" />
            </button>
          </div>

          <button
            onClick={handleDownload}
            className="p-2 rounded-lg hover:bg-zinc-800 transition-colors"
            title="Download"
          >
            <Download size={14} className="text-zinc-400" />
          </button>

          {onToggleFullscreen && (
            <button
              onClick={onToggleFullscreen}
              className="p-2 rounded-lg hover:bg-zinc-800 transition-colors"
              title={isFullscreen ? "Exit fullscreen" : "Fullscreen"}
            >
              {isFullscreen ? (
                <Minimize2 size={14} className="text-zinc-400" />
              ) : (
                <Maximize2 size={14} className="text-zinc-400" />
              )}
            </button>
          )}

          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-zinc-800 transition-colors ml-1"
            title="Close"
          >
            <X size={14} className="text-zinc-400" />
          </button>
        </div>
      </div>

      {/* PDF Content */}
      <div className="flex-1 overflow-auto bg-zinc-950 pdf-viewer">
        {isLoading && (
          <div className="flex items-center justify-center h-full">
            <div className="flex flex-col items-center gap-3">
              <Loader2 size={32} className="text-blue-500 animate-spin" />
              <p className="text-sm text-zinc-500">Loading PDF...</p>
            </div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center h-full">
            <div className="flex flex-col items-center gap-3 text-center px-4">
              <div className="p-3 rounded-full bg-red-500/10">
                <FileText size={32} className="text-red-400" />
              </div>
              <p className="text-sm text-red-400">{error}</p>
              <button
                onClick={() => {
                  setError(null)
                  setIsLoading(true)
                  setPdfUrl(null)
                  setTimeout(() => {
                    const url = `${API_BASE}/api/projects/${projectId}/files/content?path=${encodeURIComponent(filePath)}&raw=true`
                    setPdfUrl(url)
                  }, 100)
                }}
                className="flex items-center gap-2 px-3 py-1.5 text-xs bg-zinc-800 hover:bg-zinc-700 rounded-lg transition-colors"
              >
                <RotateCw size={12} />
                Retry
              </button>
            </div>
          </div>
        )}

        {pdfUrl && !error && (
          <div className="flex justify-center p-6">
            <Document
              file={pdfUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              onLoadError={onDocumentLoadError}
              loading={null}
              className="flex flex-col items-center"
            >
              <AnimatePresence mode="wait">
                <motion.div
                  key={pageNumber}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                >
                  <Page
                    pageNumber={pageNumber}
                    scale={scale}
                    className="shadow-2xl rounded-lg overflow-hidden"
                    renderTextLayer={true}
                    renderAnnotationLayer={true}
                  />
                </motion.div>
              </AnimatePresence>
            </Document>
          </div>
        )}
      </div>

      {/* Footer - Page Navigation */}
      {numPages > 0 && (
        <div className="flex items-center justify-center gap-4 px-4 py-3 border-t border-zinc-800 bg-zinc-900/95 glass-subtle">
          <button
            onClick={goToPrevPage}
            disabled={pageNumber <= 1}
            className="p-2 rounded-lg hover:bg-zinc-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Previous page"
          >
            <ChevronLeft size={18} className="text-zinc-400" />
          </button>

          <div className="flex items-center gap-2">
            <input
              type="number"
              min={1}
              max={numPages}
              value={pageNumber}
              onChange={(e) => {
                const val = parseInt(e.target.value)
                if (val >= 1 && val <= numPages) {
                  setPageNumber(val)
                }
              }}
              className="w-12 px-2 py-1 text-center text-sm bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-200 focus:outline-none focus:border-blue-500"
            />
            <span className="text-sm text-zinc-500">of {numPages}</span>
          </div>

          <button
            onClick={goToNextPage}
            disabled={pageNumber >= numPages}
            className="p-2 rounded-lg hover:bg-zinc-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Next page"
          >
            <ChevronRight size={18} className="text-zinc-400" />
          </button>
        </div>
      )}
    </div>
  )
}

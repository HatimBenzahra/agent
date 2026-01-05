import { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import { motion } from 'framer-motion'
import { Save, X, FileCode, Maximize2, Minimize2, Loader2, AlertCircle, Check } from 'lucide-react'

type CodeEditorProps = {
  projectId: string
  filePath: string | null
  onClose: () => void
  onToggleFullscreen?: () => void
  isFullscreen?: boolean
  readOnly?: boolean
}

const API_BASE = 'http://localhost:8000'

export function CodeEditor({ projectId, filePath, onClose, onToggleFullscreen, isFullscreen, readOnly }: CodeEditorProps) {
  const [content, setContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const isDirty = content !== originalContent

  useEffect(() => {
    if (!filePath) {
      setContent('')
      setOriginalContent('')
      return
    }

    setIsLoading(true)
    setError(null)

    fetch(`${API_BASE}/api/projects/${projectId}/files/content?path=${encodeURIComponent(filePath)}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to load file')
        return res.json()
      })
      .then(data => {
        setContent(data.content)
        setOriginalContent(data.content)
        setIsLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setIsLoading(false)
      })
  }, [projectId, filePath])

  const handleSave = async () => {
    if (!filePath) return

    setIsSaving(true)
    setSaveSuccess(false)
    try {
      const res = await fetch(`${API_BASE}/api/projects/${projectId}/files`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: filePath, content })
      })

      if (!res.ok) throw new Error('Failed to save file')

      setOriginalContent(content)
      setIsSaving(false)
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 2000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Save failed')
      setIsSaving(false)
    }
  }

  const getLanguage = (path: string) => {
    const ext = path.split('.').pop()?.toLowerCase()
    const langMap: Record<string, string> = {
      'js': 'javascript',
      'jsx': 'javascript',
      'ts': 'typescript',
      'tsx': 'typescript',
      'py': 'python',
      'json': 'json',
      'html': 'html',
      'css': 'css',
      'scss': 'scss',
      'less': 'less',
      'md': 'markdown',
      'sh': 'shell',
      'bash': 'shell',
      'yml': 'yaml',
      'yaml': 'yaml',
      'c': 'c',
      'cpp': 'cpp',
      'h': 'c',
      'hpp': 'cpp',
      'rs': 'rust',
      'go': 'go',
      'java': 'java',
      'rb': 'ruby',
      'php': 'php',
      'sql': 'sql',
      'graphql': 'graphql',
      'gql': 'graphql',
      'vue': 'vue',
      'svelte': 'svelte',
    }
    return langMap[ext || ''] || 'plaintext'
  }

  const getFileName = (path: string) => path.split('/').pop() || path

  if (!filePath) {
    return (
      <div className="h-full flex items-center justify-center text-zinc-600 bg-zinc-900/50">
        <div className="text-center">
          <FileCode size={40} className="mx-auto mb-3 opacity-40" />
          <p className="text-sm">Select a file to edit</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col bg-zinc-900">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-zinc-800/50 bg-zinc-900/95">
        <div className="flex items-center gap-2 min-w-0">
          <FileCode size={14} className="text-zinc-500 shrink-0" />
          <span className="text-xs text-zinc-300 truncate font-medium">{getFileName(filePath)}</span>
          {isDirty && (
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="w-2 h-2 bg-orange-400 rounded-full"
              title="Unsaved changes"
            />
          )}
          {saveSuccess && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-1 text-emerald-400 text-[10px]"
            >
              <Check size={10} />
              Saved
            </motion.div>
          )}
        </div>
        <div className="flex items-center gap-1">
          {onToggleFullscreen && (
            <button
              onClick={onToggleFullscreen}
              className="p-1.5 rounded-lg hover:bg-zinc-800 transition-colors"
              title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
            >
              {isFullscreen ? (
                <Minimize2 size={14} className="text-zinc-500" />
              ) : (
                <Maximize2 size={14} className="text-zinc-500" />
              )}
            </button>
          )}
          <button
            onClick={handleSave}
            disabled={!isDirty || isSaving}
            className={`p-1.5 rounded-lg transition-all ${
              isDirty
                ? 'hover:bg-blue-500/20 text-blue-400'
                : 'text-zinc-600'
            } disabled:opacity-40 disabled:cursor-not-allowed`}
            title="Save (Cmd+S)"
          >
            {isSaving ? (
              <Loader2 size={14} className="animate-spin" />
            ) : (
              <Save size={14} />
            )}
          </button>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-zinc-800 transition-colors"
            title="Close"
          >
            <X size={14} className="text-zinc-500" />
          </button>
        </div>
      </div>

      {/* Editor */}
      {isLoading ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="flex flex-col items-center gap-2">
            <Loader2 size={24} className="text-blue-500 animate-spin" />
            <span className="text-xs text-zinc-500">Loading file...</span>
          </div>
        </div>
      ) : error ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="flex flex-col items-center gap-2 text-center px-4">
            <AlertCircle size={24} className="text-red-400" />
            <p className="text-sm text-red-400">{error}</p>
          </div>
        </div>
      ) : (
        <Editor
          height="100%"
          language={getLanguage(filePath)}
          value={content}
          onChange={(value) => setContent(value || '')}
          theme="vs-dark"
          options={{
            minimap: { enabled: false },
            fontSize: 13,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 2,
            readOnly: readOnly,
            padding: { top: 12 },
            smoothScrolling: true,
            cursorBlinking: 'smooth',
            cursorSmoothCaretAnimation: 'on',
            renderLineHighlight: 'line',
            fontFamily: "'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, monospace",
            fontLigatures: true,
          }}
        />
      )}
    </div>
  )
}

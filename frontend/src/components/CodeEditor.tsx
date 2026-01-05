import { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import { Save, X, FileCode } from 'lucide-react'

type CodeEditorProps = {
  projectId: string
  filePath: string | null
  onClose: () => void
}

const API_BASE = 'http://localhost:8000'

export function CodeEditor({ projectId, filePath, onClose }: CodeEditorProps) {
  const [content, setContent] = useState('')
  const [originalContent, setOriginalContent] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
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
    try {
      const res = await fetch(`${API_BASE}/api/projects/${projectId}/files`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: filePath, content })
      })

      if (!res.ok) throw new Error('Failed to save file')

      setOriginalContent(content)
      setIsSaving(false)
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
      'md': 'markdown',
      'sh': 'shell',
      'yml': 'yaml',
      'yaml': 'yaml',
      'c': 'c',
      'cpp': 'cpp',
      'h': 'c',
      'hpp': 'cpp',
    }
    return langMap[ext || ''] || 'plaintext'
  }

  if (!filePath) {
    return (
      <div className="h-full flex items-center justify-center text-neutral-500">
        <div className="text-center">
          <FileCode size={48} className="mx-auto mb-3 opacity-50" />
          <p className="text-sm">Select a file to edit</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col bg-neutral-900">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-neutral-800">
        <div className="flex items-center gap-2 min-w-0">
          <FileCode size={14} className="text-neutral-500 shrink-0" />
          <span className="text-xs text-neutral-300 truncate">{filePath}</span>
          {isDirty && <span className="text-xs text-orange-400">●</span>}
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={handleSave}
            disabled={!isDirty || isSaving}
            className="p-1.5 rounded hover:bg-neutral-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Save (Cmd+S)"
          >
            <Save size={14} className={isDirty ? 'text-blue-400' : 'text-neutral-500'} />
          </button>
          <button
            onClick={onClose}
            className="p-1.5 rounded hover:bg-neutral-800 transition-colors"
            title="Close"
          >
            <X size={14} className="text-neutral-500" />
          </button>
        </div>
      </div>

      {/* Editor */}
      {isLoading ? (
        <div className="flex-1 flex items-center justify-center text-neutral-500">
          <div className="animate-spin rounded-full h-6 w-6 border-2 border-neutral-700 border-t-neutral-400" />
        </div>
      ) : error ? (
        <div className="flex-1 flex items-center justify-center text-red-400">
          <p className="text-sm">{error}</p>
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
          }}
        />
      )}
    </div>
  )
}

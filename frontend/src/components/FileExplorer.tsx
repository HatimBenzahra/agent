import { useState, useEffect } from 'react'
import { Folder, File, ChevronRight, ChevronDown, RefreshCw } from 'lucide-react'

export type FileInfo = {
  name: string
  path: string
  is_dir: boolean
  size: number
  modified: string
}

type FileExplorerProps = {
  projectId: string | null
  files: FileInfo[]
  onRefresh: () => void
  onSelectFile?: (file: FileInfo) => void
}

export function FileExplorer({ projectId, files, onRefresh, onSelectFile }: FileExplorerProps) {
  const [expandedDirs, setExpandedDirs] = useState<Set<string>>(new Set())

  const toggleDir = (path: string) => {
    setExpandedDirs(prev => {
      const next = new Set(prev)
      if (next.has(path)) {
        next.delete(path)
      } else {
        next.add(path)
      }
      return next
    })
  }

  const formatSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes}B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`
  }

  if (!projectId) {
    return (
      <div className="p-4 text-neutral-500 text-sm">
        Select a project to view files.
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-neutral-900 border-b border-neutral-800">
        <span className="text-neutral-400 text-xs font-medium uppercase tracking-wide">Files</span>
        <button
          onClick={onRefresh}
          className="p-1 text-neutral-500 hover:text-neutral-300 transition-colors"
          title="Refresh"
        >
          <RefreshCw size={12} />
        </button>
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto p-2">
        {files.length === 0 ? (
          <div className="text-neutral-500 text-xs p-2">
            No files yet. The agent will create files here.
          </div>
        ) : (
          <div className="space-y-0.5">
            {files.map((file) => (
              <div
                key={file.path}
                className="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-neutral-800 cursor-pointer group"
                onClick={() => file.is_dir ? toggleDir(file.path) : onSelectFile?.(file)}
              >
                {file.is_dir ? (
                  <>
                    {expandedDirs.has(file.path) ? (
                      <ChevronDown size={12} className="text-neutral-500" />
                    ) : (
                      <ChevronRight size={12} className="text-neutral-500" />
                    )}
                    <Folder size={14} className="text-blue-400" />
                  </>
                ) : (
                  <>
                    <span className="w-3" />
                    <File size={14} className="text-neutral-400" />
                  </>
                )}
                <span className="flex-1 text-sm text-neutral-200 truncate">
                  {file.name}
                </span>
                {!file.is_dir && (
                  <span className="text-[10px] text-neutral-500 opacity-0 group-hover:opacity-100">
                    {formatSize(file.size)}
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

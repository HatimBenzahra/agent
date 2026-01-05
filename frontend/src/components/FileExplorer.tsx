import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Folder,
  FolderOpen,
  File,
  ChevronRight,
  RefreshCw,
  FileText,
  FileCode,
  FileJson,
  FileImage,
  FileVideo,
  FileAudio
} from 'lucide-react'

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

// File type icons
const getFileIcon = (fileName: string) => {
  const ext = fileName.split('.').pop()?.toLowerCase()
  const iconClass = "w-4 h-4"

  // Code files
  if (['js', 'jsx', 'ts', 'tsx', 'py', 'rb', 'go', 'rs', 'java', 'c', 'cpp', 'h', 'hpp', 'cs', 'php', 'swift', 'kt'].includes(ext || '')) {
    return <FileCode className={`${iconClass} text-blue-400`} />
  }

  // Config/data files
  if (['json', 'yaml', 'yml', 'toml', 'xml', 'env'].includes(ext || '')) {
    return <FileJson className={`${iconClass} text-yellow-400`} />
  }

  // Document files
  if (['md', 'txt', 'doc', 'docx', 'rtf'].includes(ext || '')) {
    return <FileText className={`${iconClass} text-zinc-400`} />
  }

  // PDF files
  if (ext === 'pdf') {
    return <FileText className={`${iconClass} text-red-400`} />
  }

  // Image files
  if (['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'ico', 'bmp'].includes(ext || '')) {
    return <FileImage className={`${iconClass} text-emerald-400`} />
  }

  // Video files
  if (['mp4', 'mov', 'avi', 'mkv', 'webm'].includes(ext || '')) {
    return <FileVideo className={`${iconClass} text-purple-400`} />
  }

  // Audio files
  if (['mp3', 'wav', 'ogg', 'flac', 'm4a'].includes(ext || '')) {
    return <FileAudio className={`${iconClass} text-pink-400`} />
  }

  // Default
  return <File className={`${iconClass} text-zinc-500`} />
}

export function FileExplorer({ projectId, files, onRefresh, onSelectFile }: FileExplorerProps) {
  const [expandedDirs, setExpandedDirs] = useState<Set<string>>(new Set())
  const [isRefreshing, setIsRefreshing] = useState(false)

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

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await onRefresh()
    setTimeout(() => setIsRefreshing(false), 500)
  }

  const formatSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes}B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`
  }

  if (!projectId) {
    return (
      <div className="flex-1 flex items-center justify-center p-4">
        <p className="text-zinc-600 text-sm text-center">
          Select a project to view files
        </p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-zinc-900/50">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-zinc-800/50">
        <span className="text-zinc-500 text-xs font-medium uppercase tracking-wider">Files</span>
        <button
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="p-1.5 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded-lg transition-all disabled:opacity-50"
          title="Refresh"
        >
          <RefreshCw size={12} className={isRefreshing ? 'animate-spin' : ''} />
        </button>
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto p-2">
        {files.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Folder size={32} className="text-zinc-700 mb-2" />
            <p className="text-zinc-600 text-xs">
              No files yet
            </p>
            <p className="text-zinc-700 text-[10px] mt-1">
              Files will appear here as the agent creates them
            </p>
          </div>
        ) : (
          <div className="space-y-0.5">
            {files.map((file, index) => (
              <motion.div
                key={file.path}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.02 }}
              >
                <div
                  className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-zinc-800/70 cursor-pointer group transition-colors"
                  onClick={() => file.is_dir ? toggleDir(file.path) : onSelectFile?.(file)}
                >
                  {file.is_dir ? (
                    <>
                      <motion.div
                        animate={{ rotate: expandedDirs.has(file.path) ? 90 : 0 }}
                        transition={{ duration: 0.15 }}
                        className="text-zinc-500"
                      >
                        <ChevronRight size={12} />
                      </motion.div>
                      {expandedDirs.has(file.path) ? (
                        <FolderOpen size={16} className="text-blue-400" />
                      ) : (
                        <Folder size={16} className="text-blue-400" />
                      )}
                    </>
                  ) : (
                    <>
                      <span className="w-3" />
                      {getFileIcon(file.name)}
                    </>
                  )}
                  <span className="flex-1 text-sm text-zinc-300 truncate group-hover:text-zinc-100 transition-colors">
                    {file.name}
                  </span>
                  {!file.is_dir && (
                    <span className="text-[10px] text-zinc-600 opacity-0 group-hover:opacity-100 transition-opacity">
                      {formatSize(file.size)}
                    </span>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

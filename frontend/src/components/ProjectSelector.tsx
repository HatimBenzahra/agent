import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, Trash2, X, Folder, MessageSquare } from 'lucide-react'

type Project = {
  id: string
  name: string
  description: string
  created_at: string
  updated_at: string
  status: string
}

type ProjectSelectorProps = {
  projects: Project[]
  currentProject: Project | null
  onSelect: (project: Project) => void
  onCreate: (name: string, description: string) => void
  onDelete: (projectId: string) => void
}

export function ProjectSelector({
  projects,
  currentProject,
  onSelect,
  onCreate,
  onDelete
}: ProjectSelectorProps) {
  const [isCreating, setIsCreating] = useState(false)
  const [newName, setNewName] = useState('')
  const [newDescription, setNewDescription] = useState('')

  const handleCreate = () => {
    if (!newName.trim()) return
    onCreate(newName.trim(), newDescription.trim())
    setNewName('')
    setNewDescription('')
    setIsCreating(false)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    return date.toLocaleDateString()
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800/50">
        <span className="text-zinc-400 text-xs font-medium uppercase tracking-wider">Projects</span>
        <button
          onClick={() => setIsCreating(true)}
          className="p-1.5 text-zinc-500 hover:text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all"
          title="New Project"
        >
          <Plus size={14} />
        </button>
      </div>

      {/* Create form */}
      <AnimatePresence>
        {isCreating && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="p-4 border-b border-zinc-800/50 bg-zinc-900/50">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-medium text-zinc-300">New Project</span>
                <button
                  onClick={() => setIsCreating(false)}
                  className="p-1 text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800 rounded-lg transition-colors"
                >
                  <X size={12} />
                </button>
              </div>
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="Project name"
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-100 placeholder-zinc-600 mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
                autoFocus
                onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
              />
              <input
                type="text"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                placeholder="Description (optional)"
                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-100 placeholder-zinc-600 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
                onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
              />
              <button
                onClick={handleCreate}
                disabled={!newName.trim()}
                className="w-full bg-blue-600 text-white text-sm py-2 rounded-lg hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all font-medium"
              >
                Create Project
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Project list */}
      <div className="flex-1 overflow-y-auto p-2">
        {projects.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center px-4">
            <div className="p-3 rounded-xl bg-zinc-800/50 mb-3">
              <Folder size={24} className="text-zinc-600" />
            </div>
            <p className="text-zinc-500 text-sm mb-1">No projects yet</p>
            <p className="text-zinc-600 text-xs">
              Create your first project to get started
            </p>
          </div>
        ) : (
          <div className="space-y-1">
            {projects.map((project, index) => (
              <motion.div
                key={project.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.03 }}
              >
                <div
                  className={`relative flex items-start gap-3 p-3 rounded-xl cursor-pointer group transition-all ${
                    currentProject?.id === project.id
                      ? 'bg-blue-500/10 ring-1 ring-blue-500/30'
                      : 'hover:bg-zinc-800/50'
                  }`}
                  onClick={() => onSelect(project)}
                >
                  <div className={`p-2 rounded-lg shrink-0 ${
                    currentProject?.id === project.id
                      ? 'bg-blue-500/20'
                      : 'bg-zinc-800'
                  }`}>
                    <MessageSquare size={14} className={
                      currentProject?.id === project.id ? 'text-blue-400' : 'text-zinc-500'
                    } />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className={`text-sm font-medium truncate ${
                      currentProject?.id === project.id ? 'text-blue-300' : 'text-zinc-200'
                    }`}>
                      {project.name}
                    </div>
                    {project.description && (
                      <div className="text-[11px] text-zinc-500 truncate mt-0.5">
                        {project.description}
                      </div>
                    )}
                    <div className="text-[10px] text-zinc-600 mt-1">
                      {formatDate(project.updated_at)}
                    </div>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      if (confirm(`Delete "${project.name}"?`)) {
                        onDelete(project.id)
                      }
                    }}
                    className="p-1.5 text-zinc-600 hover:text-red-400 hover:bg-red-500/10 rounded-lg opacity-0 group-hover:opacity-100 transition-all absolute right-2 top-2"
                    title="Delete project"
                  >
                    <Trash2 size={12} />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

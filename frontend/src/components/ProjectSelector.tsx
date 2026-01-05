import { useState } from 'react'
import { Plus, FolderOpen, Trash2, X } from 'lucide-react'

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

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-neutral-900 border-b border-neutral-800">
        <span className="text-neutral-400 text-xs font-medium uppercase tracking-wide">Projects</span>
        <button
          onClick={() => setIsCreating(true)}
          className="p-1 text-neutral-500 hover:text-neutral-300 transition-colors"
          title="New Project"
        >
          <Plus size={14} />
        </button>
      </div>

      {/* Create form */}
      {isCreating && (
        <div className="p-3 border-b border-neutral-800 bg-neutral-900/50">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-neutral-400">New Project</span>
            <button
              onClick={() => setIsCreating(false)}
              className="text-neutral-500 hover:text-neutral-300"
            >
              <X size={12} />
            </button>
          </div>
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            placeholder="Project name"
            className="w-full bg-neutral-800 border border-neutral-700 rounded px-2 py-1.5 text-sm text-neutral-100 placeholder-neutral-500 mb-2 focus:outline-none focus:border-neutral-600"
            autoFocus
            onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
          />
          <input
            type="text"
            value={newDescription}
            onChange={(e) => setNewDescription(e.target.value)}
            placeholder="Description (optional)"
            className="w-full bg-neutral-800 border border-neutral-700 rounded px-2 py-1.5 text-sm text-neutral-100 placeholder-neutral-500 mb-2 focus:outline-none focus:border-neutral-600"
            onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
          />
          <button
            onClick={handleCreate}
            disabled={!newName.trim()}
            className="w-full bg-blue-600 text-white text-sm py-1.5 rounded hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Create
          </button>
        </div>
      )}

      {/* Project list */}
      <div className="flex-1 overflow-y-auto p-2">
        {projects.length === 0 ? (
          <div className="text-neutral-500 text-xs p-2 text-center">
            No projects yet.<br />Create one to get started.
          </div>
        ) : (
          <div className="space-y-1">
            {projects.map((project) => (
              <div
                key={project.id}
                className={`flex items-center gap-2 px-2 py-2 rounded cursor-pointer group transition-colors ${
                  currentProject?.id === project.id
                    ? 'bg-blue-600/20 border border-blue-500/30'
                    : 'hover:bg-neutral-800 border border-transparent'
                }`}
                onClick={() => onSelect(project)}
              >
                <FolderOpen size={14} className={
                  currentProject?.id === project.id ? 'text-blue-400' : 'text-neutral-500'
                } />
                <div className="flex-1 min-w-0">
                  <div className="text-sm text-neutral-200 truncate">{project.name}</div>
                  {project.description && (
                    <div className="text-[10px] text-neutral-500 truncate">{project.description}</div>
                  )}
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    if (confirm(`Delete project "${project.name}"?`)) {
                      onDelete(project.id)
                    }
                  }}
                  className="p-1 text-neutral-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all"
                  title="Delete project"
                >
                  <Trash2 size={12} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

import { useState, useRef, useEffect } from 'react'
import {
  Send,
  Bot,
  User,
  Loader2,
  AlertCircle,
  Terminal as TerminalIcon,
  FolderKanban,
  Menu,
  X,
  FileCode,
  Sparkles,
  Wifi,
  WifiOff,
  ChevronDown,
  StopCircle,
  CheckCircle2,
  Circle,
  XCircle,
  Zap,
  ChevronRight,
  FileEdit,
  FileSearch,
  Check,
  AlertTriangle
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import { Terminal } from './components/Terminal'
import type { TerminalEntry } from './components/Terminal'
import { FileExplorer } from './components/FileExplorer'
import type { FileInfo } from './components/FileExplorer'
import { ProjectSelector } from './components/ProjectSelector'
import { CodeEditor } from './components/CodeEditor'
import { PDFViewer } from './components/PDFViewer'

// Types for inline plan display
type PlanStep = {
  id: string
  objective: string
  status: 'pending' | 'executing' | 'validating' | 'completed' | 'failed'
}

type Validation = {
  success: boolean
  feedback: string
}

type StepEvent = {
  type: 'tool' | 'log'
  tool?: string
  message: string
  status?: 'running' | 'success' | 'error'
  timestamp: number
}

// Types
type Project = {
  id: string
  name: string
  description: string
  created_at: string
  updated_at: string
  status: string
}

type ToolCall = {
  tool: string
  arguments: Record<string, unknown>
  status: 'executing' | 'done'
  output?: string
  success?: boolean
}

type Message = {
  role: 'user' | 'agent'
  content: string
  toolCalls?: ToolCall[]
  isError?: boolean
}

const API_BASE = 'http://localhost:8000'

// Helper to check if file is PDF
const isPdfFile = (path: string) => path.toLowerCase().endsWith('.pdf')

function App() {
  // Project state
  const [projects, setProjects] = useState<Project[]>([])
  const [currentProject, setCurrentProject] = useState<Project | null>(null)
  const [files, setFiles] = useState<FileInfo[]>([])

  // Chat state
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentToolCalls, setCurrentToolCalls] = useState<ToolCall[]>([])

  // Terminal state
  const [terminalEntries, setTerminalEntries] = useState<TerminalEntry[]>([])

  // Multi-agent plan state
  const [currentPlan, setCurrentPlan] = useState<any[]>([])
  const [currentStepId, setCurrentStepId] = useState<string | undefined>()
  const [validations, setValidations] = useState<Record<string, any>>({})
  const [stepEvents, setStepEvents] = useState<Record<string, StepEvent[]>>({})

  // UI state
  const [isConnected, setIsConnected] = useState(false)
  const [selectedFile, setSelectedFile] = useState<string | null>(null)

  // Responsive & Layout state
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isEditorFullscreen, setIsEditorFullscreen] = useState(false)
  const [isTerminalVisible, setIsTerminalVisible] = useState(false)
  const [isWorkspaceOpen, setIsWorkspaceOpen] = useState(false)

  // Live activity indicator
  const [lastActivity, setLastActivity] = useState<string | null>(null)

  const ws = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Fetch projects on mount
  useEffect(() => {
    fetchProjects()
  }, [])

  // Auto-show terminal when entries arrive
  useEffect(() => {
    if (terminalEntries.length > 0) {
      setIsTerminalVisible(true)
    }
  }, [terminalEntries])

  // Auto-open workspace when file selected
  useEffect(() => {
    if (selectedFile) {
      setIsWorkspaceOpen(true)
    }
  }, [selectedFile])

  // Connect to WebSocket when project changes
  useEffect(() => {
    if (!currentProject) {
      setIsConnected(false)
      return
    }

    // Close existing connection
    if (ws.current) {
      ws.current.close()
    }

    // Reset state for new project
    setMessages([])
    setCurrentToolCalls([])
    setTerminalEntries([])
    setCurrentPlan([])
    setValidations({})
    setStepEvents({})
    setLastActivity(null)

    // Connect to project chat
    const socket = new WebSocket(`ws://localhost:8000/ws/chat/${currentProject.id}`)
    ws.current = socket

    // Ping interval to keep connection alive
    let pingInterval: ReturnType<typeof setInterval> | null = null

    socket.onopen = () => {
      setIsConnected(true)
      // Send ping every 30 seconds to keep connection alive
      pingInterval = setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
          socket.send('ping')
        }
      }, 30000)
    }

    socket.onclose = () => {
      setIsConnected(false)
      if (pingInterval) {
        clearInterval(pingInterval)
        pingInterval = null
      }
    }

    socket.onmessage = (event) => {
      // Ignore pong responses
      if (event.data === 'pong') return

      const data = JSON.parse(event.data)

      if (data.type === 'status') {
        setLastActivity(data.message || 'Processing...')
      } else if (data.type === 'plan_created') {
        setCurrentPlan(data.plan || [])
        setValidations({})
        setStepEvents({})
        setLastActivity('Plan created')
      } else if (data.type === 'step_started') {
        setCurrentStepId(data.step_id)
        setCurrentPlan(prev => prev.map(step =>
          step.id === data.step_id ? { ...step, status: 'executing' } : step
        ))
        const step = currentPlan.find(s => s.id === data.step_id)
        setLastActivity(step ? `Executing: ${step.objective}` : 'Executing step...')
      } else if (data.type === 'step_validating') {
        setCurrentPlan(prev => prev.map(step =>
          step.id === data.step_id ? { ...step, status: 'validating' } : step
        ))
        setLastActivity('Validating step...')
      } else if (data.type === 'step_completed') {
        setCurrentPlan(prev => prev.map(step =>
          step.id === data.step_id ? { ...step, status: 'completed' } : step
        ))
        if (data.validation) {
          setValidations(prev => ({ ...prev, [data.step_id]: data.validation }))
        }
        setLastActivity('Step completed')
      } else if (data.type === 'step_failed') {
        setCurrentPlan(prev => prev.map(step =>
          step.id === data.step_id ? { ...step, status: 'failed' } : step
        ))
        if (data.validation) {
          setValidations(prev => ({ ...prev, [data.step_id]: data.validation }))
        }
        setLastActivity('Step failed')
      } else if (data.type === 'tool_call') {
        setCurrentToolCalls(prev => [...prev, {
          tool: data.tool,
          arguments: data.arguments,
          status: 'executing'
        }])
        setLastActivity(`Using tool: ${data.tool}`)

        if (data.tool === 'terminal' && data.arguments?.command) {
          setTerminalEntries(prev => [...prev, {
            type: 'command',
            content: data.arguments.command as string,
            timestamp: new Date()
          }])
        }
      } else if (data.type === 'tool_result') {
        setCurrentToolCalls(prev =>
          prev.map((tc, idx) =>
            idx === prev.length - 1
              ? { ...tc, status: 'done', output: data.output, success: data.success }
              : tc
          )
        )

        if (data.tool === 'terminal' && data.output) {
          setTerminalEntries(prev => [...prev, {
            type: data.success ? 'output' : 'error',
            content: data.output,
            timestamp: new Date()
          }])
        }

        if (['write_file', 'delete_file'].includes(data.tool)) {
          fetchFiles()
        }
      } else if (data.type === 'sub_agent_tool') {
        const args = data.arguments || {}

        // Update Terminal
        if (data.tool === 'terminal' && args.command) {
          setTerminalEntries(prev => [...prev, {
            type: 'command',
            content: args.command,
            timestamp: new Date()
          }])

          if (data.output) {
            setTerminalEntries(prev => [...prev, {
              type: data.success ? 'output' : 'error',
              content: data.output,
              timestamp: new Date()
            }])
          }
        }

        // Update Files
        if (['write_file', 'delete_file'].includes(data.tool) && data.success) {
          fetchFiles()
        }

        // Update Plan Visualizer
        if (data.task_id && data.tool) {
          let message = `Using tool: ${data.tool}`

          if (data.tool === 'terminal') {
            message = `Executing: ${args.command || 'script'}`
          } else if (data.tool === 'write_file') {
            message = `Writing: ${args.target_file || args.path || 'file'}`
          } else if (data.tool === 'read_file') {
            message = `Reading: ${args.path || 'file'}`
          } else if (data.tool === 'list_files') {
            message = `Listing: ${args.path || '.'}`
          }

          setLastActivity(message)

          const newEvent: StepEvent = {
            type: 'tool',
            tool: data.tool,
            message: message,
            status: data.success ? 'success' : 'error',
            timestamp: Date.now()
          }

          setStepEvents(prev => {
            const current = prev[data.task_id] || []
            const exists = current.some(e =>
              e.tool === data.tool &&
              e.message === message &&
              Math.abs(e.timestamp - newEvent.timestamp) < 100
            )
            if (exists) return prev
            return { ...prev, [data.task_id]: [...current, newEvent] }
          })
        }
      } else if (data.type === 'result') {
        setMessages(prev => [...prev, {
          role: 'agent',
          content: data.content,
          toolCalls: currentToolCalls.length > 0 ? [...currentToolCalls] : undefined
        }])
        setCurrentToolCalls([])
        setIsProcessing(false)
        setLastActivity(null)
        fetchFiles()
      } else if (data.type === 'files_updated') {
        setFiles(data.files)
      } else if (data.type === 'error') {
        setMessages(prev => [...prev, {
          role: 'agent',
          content: data.content,
          isError: true
        }])
        setCurrentToolCalls([])
        setIsProcessing(false)
        setLastActivity(null)
      } else if (data.type === 'stop_acknowledged') {
        setLastActivity(data.message || 'Stopping...')
      } else if (data.type === 'execution_interrupted') {
        // Mark remaining steps as interrupted
        setCurrentPlan(prev => prev.map(step =>
          step.status === 'pending' || step.status === 'executing'
            ? { ...step, status: 'pending' }
            : step
        ))
        setLastActivity(`Interrupted: ${data.message || 'Stopped by user'}`)
      }
    }

    fetchFiles()
    fetchChatHistory()

    return () => {
      // Clean up ping interval
      if (pingInterval) {
        clearInterval(pingInterval)
      }
      if (socket.readyState === WebSocket.OPEN) {
        socket.close()
      }
    }
  }, [currentProject?.id])

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, currentToolCalls])

  // API functions
  const fetchProjects = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/projects`)
      const data = await res.json()
      setProjects(data.projects || [])
    } catch (e) {
      console.error('Failed to fetch projects:', e)
      setProjects([])
    }
  }

  const fetchFiles = async () => {
    if (!currentProject) return
    try {
      const res = await fetch(`${API_BASE}/api/projects/${currentProject.id}/files`)
      const data = await res.json()
      setFiles(data.files || [])
    } catch (e) {
      console.error('Failed to fetch files:', e)
    }
  }

  const fetchChatHistory = async () => {
    if (!currentProject) return
    try {
      const res = await fetch(`${API_BASE}/api/projects/${currentProject.id}/chat/history`)
      const data = await res.json()
      const formattedMessages = (data.messages || []).map((msg: any) => ({
        role: msg.role === 'user' ? 'user' : 'agent',
        content: msg.content,
        toolCalls: undefined,
        isError: false
      }))
      setMessages(formattedMessages)
    } catch (e) {
      console.error('Failed to fetch chat history:', e)
      setMessages([])
    }
  }

  const handleCreateProject = async (name: string, description: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description })
      })
      const data = await res.json()
      setProjects(prev => [data.project, ...prev])
      setCurrentProject(data.project)
    } catch (e) {
      console.error('Failed to create project:', e)
    }
  }

  const deleteProject = async (projectId: string) => {
    try {
      await fetch(`${API_BASE}/api/projects/${projectId}`, { method: 'DELETE' })
      setProjects(prev => prev.filter(p => p.id !== projectId))
      if (currentProject?.id === projectId) {
        setCurrentProject(null)
      }
    } catch (e) {
      console.error('Failed to delete project:', e)
    }
  }

  const sendMessage = () => {
    if (!input.trim() || isProcessing || !isConnected) return
    const msg = input
    setInput('')
    setIsProcessing(true)
    setMessages(prev => [...prev, { role: 'user', content: msg }])
    ws.current?.send(msg)
  }

  const handleStop = () => {
    if (!isConnected || !ws.current) return
    ws.current.send('__STOP__')
    setLastActivity('Stopping...')
  }

  const handleStopWithMessage = () => {
    if (!isConnected || !ws.current || !input.trim()) return
    const msg = input
    setInput('')
    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: msg }])
    // Send stop with message
    ws.current.send(JSON.stringify({ type: 'stop', message: msg }))
    setLastActivity('Interrupting with new instructions...')
  }

  const handleToggleFullscreen = () => {
    setIsEditorFullscreen(!isEditorFullscreen)
  }

  const toggleWorkspace = () => {
    setIsWorkspaceOpen(!isWorkspaceOpen)
  }

  const handleFileSelect = (file: FileInfo) => {
    setSelectedFile(file.path)
  }

  // Render file viewer based on file type
  const renderFileViewer = () => {
    if (!selectedFile || !currentProject) {
      return (
        <div className="flex-1 flex items-center justify-center text-zinc-600">
          <div className="text-center">
            <FileCode size={40} className="mx-auto mb-3 opacity-50" />
            <p className="text-sm">Select a file to view</p>
          </div>
        </div>
      )
    }

    if (isPdfFile(selectedFile)) {
      return (
        <PDFViewer
          projectId={currentProject.id}
          filePath={selectedFile}
          onClose={() => setSelectedFile(null)}
          isFullscreen={isEditorFullscreen}
          onToggleFullscreen={handleToggleFullscreen}
        />
      )
    }

    return (
      <CodeEditor
        projectId={currentProject.id}
        filePath={selectedFile}
        onClose={() => setSelectedFile(null)}
        readOnly={false}
        isFullscreen={isEditorFullscreen}
        onToggleFullscreen={handleToggleFullscreen}
      />
    )
  }

  return (
    <div className="flex h-screen bg-zinc-950 text-zinc-200 font-sans overflow-hidden">
      {/* Left Sidebar - Projects */}
      <div className={`w-72 border-r border-zinc-800/50 bg-zinc-900/50 flex flex-col shrink-0 ${isMobileMenuOpen ? 'fixed inset-y-0 left-0 z-50' : 'hidden md:flex'}`}>
        <div className="p-4 border-b border-zinc-800/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="p-1.5 rounded-lg bg-gradient-to-br from-blue-500/20 to-violet-500/20">
                <Bot size={18} className="text-blue-400" />
              </div>
              <span className="font-semibold text-zinc-100">Agent Studio</span>
            </div>
            <button className="md:hidden p-1.5 hover:bg-zinc-800 rounded-lg" onClick={() => setIsMobileMenuOpen(false)}>
              <X size={16} className="text-zinc-400" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto">
          <ProjectSelector
            currentProject={currentProject}
            onSelect={setCurrentProject}
            projects={projects}
            onCreate={handleCreateProject}
            onDelete={deleteProject}
          />
        </div>
      </div>

      {/* Main Content - Chat Interface */}
      <div className="flex-1 flex flex-col min-w-0 bg-zinc-950 relative">
        {/* Header */}
        <header className="flex items-center justify-between px-4 py-3 border-b border-zinc-800/50 bg-zinc-900/30 glass-subtle">
          <div className="flex items-center gap-3">
            <button className="md:hidden p-1.5 hover:bg-zinc-800 rounded-lg text-zinc-400" onClick={() => setIsMobileMenuOpen(true)}>
              <Menu size={18} />
            </button>

            <div className="flex items-center gap-3">
              <h1 className="font-medium text-zinc-100">
                {currentProject ? currentProject.name : 'Select a Project'}
              </h1>

              {currentProject && (
                <div className={`flex items-center gap-1.5 px-2 py-1 rounded-full text-xs ${
                  isConnected
                    ? 'bg-emerald-500/10 text-emerald-400'
                    : 'bg-red-500/10 text-red-400'
                }`}>
                  {isConnected ? <Wifi size={12} /> : <WifiOff size={12} />}
                  <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
                </div>
              )}
            </div>
          </div>

          {currentProject && (
            <div className="flex items-center gap-2">
              {/* Live Activity Indicator */}
              {lastActivity && (
                <motion.div
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-400 text-xs"
                >
                  <Loader2 size={12} className="animate-spin" />
                  <span className="max-w-48 truncate">{lastActivity}</span>
                </motion.div>
              )}

              <button
                onClick={toggleWorkspace}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-all ${
                  isWorkspaceOpen
                    ? 'bg-blue-500/20 text-blue-400 ring-1 ring-blue-500/30'
                    : 'hover:bg-zinc-800 text-zinc-400'
                }`}
              >
                <FolderKanban size={16} />
                <span className="hidden sm:inline">Workspace</span>
              </button>

              <button
                onClick={() => setIsTerminalVisible(!isTerminalVisible)}
                className={`p-2 rounded-lg transition-all ${
                  isTerminalVisible
                    ? 'bg-zinc-800 text-zinc-100 ring-1 ring-zinc-700'
                    : 'text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/50'
                }`}
                title="Toggle Terminal"
              >
                <TerminalIcon size={16} />
                {terminalEntries.length > 0 && (
                  <span className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full" />
                )}
              </button>
            </div>
          )}
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto p-4 space-y-6">
            {messages.length === 0 && !isProcessing && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col items-center justify-center py-20 text-center"
              >
                <div className="p-4 rounded-2xl bg-gradient-to-br from-blue-500/10 to-violet-500/10 mb-4">
                  <Sparkles size={32} className="text-blue-400" />
                </div>
                <h2 className="text-xl font-medium text-zinc-200 mb-2">
                  {currentProject ? 'Start a conversation' : 'Welcome to Agent Studio'}
                </h2>
                <p className="text-zinc-500 max-w-md">
                  {currentProject
                    ? 'Describe what you want to build and the agent will help you create it.'
                    : 'Select or create a project to get started with your AI assistant.'}
                </p>
              </motion.div>
            )}

            {messages.map((msg, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex items-start gap-4 ${
                  msg.role === 'user' ? 'flex-row-reverse' : ''
                }`}
              >
                <div className={`shrink-0 p-2 rounded-xl ${
                  msg.role === 'agent'
                    ? 'bg-gradient-to-br from-blue-500/20 to-violet-500/20'
                    : 'bg-zinc-800'
                }`}>
                  {msg.role === 'agent' ? (
                    <Bot size={18} className="text-blue-400" />
                  ) : (
                    <User size={18} className="text-zinc-400" />
                  )}
                </div>

                <div className={`flex-1 min-w-0 space-y-3 ${
                  msg.role === 'user' ? 'text-right' : ''
                }`}>
                  <div className={`inline-block text-left ${
                    msg.role === 'user'
                      ? 'bg-blue-600/20 border border-blue-500/20 rounded-2xl rounded-tr-sm px-4 py-3'
                      : 'bg-zinc-900/50 border border-zinc-800/50 rounded-2xl rounded-tl-sm px-4 py-3'
                  }`}>
                    <div className="prose prose-invert prose-sm max-w-none prose-custom">
                      <ReactMarkdown
                        components={{
                          code: ({ node, inline, className, children, ...props }: any) => {
                            const match = /language-(\w+)/.exec(className || '')
                            return !inline && match ? (
                              <div className="relative group my-3">
                                <div className="absolute right-3 top-3 opacity-0 group-hover:opacity-100 transition-opacity">
                                  <span className="text-[10px] text-zinc-500 font-mono uppercase">{match[1]}</span>
                                </div>
                                <pre className="bg-zinc-950 rounded-xl p-4 overflow-x-auto border border-zinc-800">
                                  <code className={className} {...props}>
                                    {children}
                                  </code>
                                </pre>
                              </div>
                            ) : (
                              <code className="bg-zinc-800 rounded px-1.5 py-0.5 text-zinc-200 text-sm" {...props}>
                                {children}
                              </code>
                            )
                          }
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  </div>

                  {/* Tool Calls Display */}
                  {msg.toolCalls && msg.toolCalls.length > 0 && (
                    <div className="space-y-2 mt-3">
                      {msg.toolCalls.map((tc, tcIdx) => (
                        <motion.div
                          key={tcIdx}
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden text-xs font-mono"
                        >
                          <div className="px-3 py-2 bg-zinc-800/50 flex items-center justify-between border-b border-zinc-800">
                            <div className="flex items-center gap-2">
                              <TerminalIcon size={12} className="text-zinc-500" />
                              <span className="text-zinc-300 font-semibold">{tc.tool}</span>
                            </div>
                            <span className={`px-2 py-0.5 rounded-full text-[10px] ${
                              tc.status === 'done'
                                ? tc.success
                                  ? 'bg-emerald-500/10 text-emerald-400'
                                  : 'bg-red-500/10 text-red-400'
                                : 'bg-blue-500/10 text-blue-400'
                            }`}>
                              {tc.status === 'done' ? (tc.success ? 'Success' : 'Failed') : 'Running...'}
                            </span>
                          </div>
                          {tc.output && (
                            <div className="p-3 max-h-40 overflow-y-auto whitespace-pre-wrap text-zinc-400 text-xs">
                              {tc.output}
                            </div>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  )}

                  {msg.isError && (
                    <div className="flex items-center gap-2 text-red-400 text-sm mt-2">
                      <AlertCircle size={14} />
                      <span>An error occurred processing this request.</span>
                    </div>
                  )}
                </div>
              </motion.div>
            ))}

            {/* Processing indicator with inline plan */}
            {isProcessing && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-start gap-4"
              >
                <div className="shrink-0 p-2 rounded-xl bg-gradient-to-br from-blue-500/20 to-violet-500/20">
                  <Bot size={18} className="text-blue-400" />
                </div>
                <div className="flex-1 bg-zinc-900/50 border border-zinc-800/50 rounded-2xl rounded-tl-sm px-4 py-3 space-y-3">
                  {/* Show plan if available, otherwise show thinking */}
                  {currentPlan.length > 0 ? (
                    <>
                      {/* Plan header with progress */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Sparkles size={14} className="text-violet-400" />
                          <span className="text-sm font-medium text-zinc-300">Execution Plan</span>
                          <span className="text-xs text-zinc-500">
                            {currentPlan.filter(s => s.status === 'completed').length}/{currentPlan.length} steps
                          </span>
                        </div>
                        {/* Progress bar */}
                        <div className="w-20 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                          <motion.div
                            className="h-full bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full"
                            initial={{ width: 0 }}
                            animate={{ width: `${(currentPlan.filter(s => s.status === 'completed').length / currentPlan.length) * 100}%` }}
                            transition={{ duration: 0.3 }}
                          />
                        </div>
                      </div>

                      {/* Plan steps */}
                      <div className="space-y-2">
                        {currentPlan.map((step, index) => {
                          const events = stepEvents[step.id] || []
                          const validation = validations[step.id]
                          const isExpanded = step.status === 'executing' || step.status === 'validating'

                          return (
                            <motion.div
                              key={step.id}
                              initial={{ opacity: 0, x: -10 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.05 }}
                              className={`relative border rounded-xl transition-all duration-300 ${
                                step.status === 'completed' ? 'border-emerald-500/20 bg-emerald-500/5' :
                                step.status === 'failed' ? 'border-red-500/20 bg-red-500/5' :
                                step.status === 'executing' ? 'border-blue-500/50 bg-blue-500/5' :
                                step.status === 'validating' ? 'border-violet-500/50 bg-violet-500/5' :
                                'border-zinc-800 bg-zinc-900/50'
                              }`}
                            >
                              {/* Step header */}
                              <div className="flex items-start gap-3 p-3">
                                {/* Icon */}
                                <div className="relative flex flex-col items-center">
                                  {step.status === 'completed' ? (
                                    <motion.div
                                      initial={{ scale: 0 }}
                                      animate={{ scale: 1 }}
                                      className="p-1 rounded-full bg-emerald-500/20"
                                    >
                                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                                    </motion.div>
                                  ) : step.status === 'failed' ? (
                                    <motion.div
                                      initial={{ scale: 0 }}
                                      animate={{ scale: 1 }}
                                      className="p-1 rounded-full bg-red-500/20"
                                    >
                                      <XCircle className="w-4 h-4 text-red-400" />
                                    </motion.div>
                                  ) : step.status === 'executing' ? (
                                    <motion.div
                                      animate={{ rotate: 360 }}
                                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                      className="p-1 rounded-full bg-blue-500/20"
                                    >
                                      <Zap className="w-4 h-4 text-blue-400" />
                                    </motion.div>
                                  ) : step.status === 'validating' ? (
                                    <motion.div
                                      animate={{ scale: [1, 1.1, 1] }}
                                      transition={{ duration: 1, repeat: Infinity }}
                                      className="p-1 rounded-full bg-violet-500/20"
                                    >
                                      <Sparkles className="w-4 h-4 text-violet-400" />
                                    </motion.div>
                                  ) : (
                                    <div className="p-1 rounded-full bg-zinc-800">
                                      <Circle className="w-4 h-4 text-zinc-500" />
                                    </div>
                                  )}
                                  {/* Connector line */}
                                  {index < currentPlan.length - 1 && (
                                    <div className={`w-0.5 flex-1 mt-1 ${
                                      step.status === 'completed' ? 'bg-emerald-500/30' : 'bg-zinc-700'
                                    }`} style={{ minHeight: '12px' }} />
                                  )}
                                </div>

                                {/* Content */}
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center justify-between gap-2 mb-1">
                                    <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">
                                      Step {index + 1}
                                    </span>
                                    {/* Status badge */}
                                    {step.status === 'completed' && (
                                      <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-400">Done</span>
                                    )}
                                    {step.status === 'failed' && (
                                      <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-red-500/10 text-red-400">Failed</span>
                                    )}
                                    {step.status === 'executing' && (
                                      <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-blue-500/10 text-blue-400 flex items-center gap-1">
                                        <Loader2 size={10} className="animate-spin" />
                                        Running
                                      </span>
                                    )}
                                    {step.status === 'validating' && (
                                      <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-violet-500/10 text-violet-400 flex items-center gap-1">
                                        <Loader2 size={10} className="animate-spin" />
                                        Validating
                                      </span>
                                    )}
                                  </div>
                                  <p className={`text-sm leading-relaxed ${
                                    step.status === 'completed' ? 'text-zinc-400' :
                                    step.status === 'failed' ? 'text-red-300' :
                                    step.status === 'executing' || step.status === 'validating' ? 'text-zinc-100' :
                                    'text-zinc-400'
                                  }`}>
                                    {step.objective}
                                  </p>

                                  {/* Expanded details for active step */}
                                  <AnimatePresence>
                                    {isExpanded && events.length > 0 && (
                                      <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        className="mt-2 pt-2 border-t border-zinc-800/50"
                                      >
                                        <div className="space-y-1">
                                          {events.slice(-5).map((event, idx) => (
                                            <motion.div
                                              key={idx}
                                              initial={{ opacity: 0, x: -5 }}
                                              animate={{ opacity: 1, x: 0 }}
                                              className="flex items-center gap-2 text-xs"
                                            >
                                              <div className={`p-0.5 rounded ${
                                                event.status === 'success' ? 'bg-emerald-500/20 text-emerald-400' :
                                                event.status === 'error' ? 'bg-red-500/20 text-red-400' :
                                                'bg-blue-500/20 text-blue-400'
                                              }`}>
                                                {event.tool === 'terminal' ? <TerminalIcon size={10} /> :
                                                 event.tool === 'write_file' ? <FileEdit size={10} /> :
                                                 event.tool === 'read_file' ? <FileSearch size={10} /> :
                                                 <ChevronRight size={10} />}
                                              </div>
                                              <span className="text-zinc-400 truncate">{event.message}</span>
                                            </motion.div>
                                          ))}
                                        </div>
                                      </motion.div>
                                    )}
                                  </AnimatePresence>

                                  {/* Validation feedback */}
                                  {validation && (
                                    <motion.div
                                      initial={{ opacity: 0, y: 5 }}
                                      animate={{ opacity: 1, y: 0 }}
                                      className={`mt-2 p-2 rounded-lg flex items-start gap-2 ${
                                        validation.success
                                          ? 'bg-emerald-500/10 border border-emerald-500/20'
                                          : 'bg-red-500/10 border border-red-500/20'
                                      }`}
                                    >
                                      {validation.success ? (
                                        <Check size={12} className="text-emerald-400 mt-0.5" />
                                      ) : (
                                        <AlertTriangle size={12} className="text-red-400 mt-0.5" />
                                      )}
                                      <span className={`text-xs ${
                                        validation.success ? 'text-emerald-400/80' : 'text-red-400/80'
                                      }`}>
                                        {validation.feedback}
                                      </span>
                                    </motion.div>
                                  )}
                                </div>
                              </div>
                            </motion.div>
                          )
                        })}
                      </div>
                    </>
                  ) : (
                    /* No plan yet - show thinking indicator */
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-blue-400 rounded-full typing-dot" />
                        <span className="w-2 h-2 bg-blue-400 rounded-full typing-dot" />
                        <span className="w-2 h-2 bg-blue-400 rounded-full typing-dot" />
                      </div>
                      <span className="text-sm text-zinc-500">
                        {lastActivity || 'Agent is thinking...'}
                      </span>
                    </div>
                  )}
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4 bg-zinc-900/50 border-t border-zinc-800/50 glass-subtle">
          <div className="max-w-4xl mx-auto">
            <div className="relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    if (isProcessing && input.trim()) {
                      // Send interrupt with message
                      handleStopWithMessage()
                    } else {
                      sendMessage()
                    }
                  }
                }}
                placeholder={
                  !isConnected
                    ? "Connect to a project to start chatting"
                    : isProcessing
                      ? "Type to interrupt and redirect the agent..."
                      : "Ask me anything... (Shift+Enter for new line)"
                }
                disabled={!isConnected}
                rows={1}
                className={`w-full bg-zinc-950 border rounded-xl px-4 py-3 pr-24 text-zinc-200 placeholder-zinc-600 focus:outline-none focus:ring-2 focus:border-blue-500/50 resize-none transition-all ${
                  isProcessing
                    ? 'border-orange-500/50 focus:ring-orange-500/50'
                    : 'border-zinc-800 focus:ring-blue-500/50'
                }`}
                style={{ minHeight: '48px', maxHeight: '200px' }}
              />
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                {/* Stop button - shown during processing */}
                {isProcessing && (
                  <motion.button
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    onClick={handleStop}
                    className="p-2 rounded-lg bg-red-600 text-white hover:bg-red-500 transition-all"
                    title="Stop execution"
                  >
                    <StopCircle size={16} />
                  </motion.button>
                )}
                {/* Send button */}
                <button
                  onClick={() => {
                    if (isProcessing && input.trim()) {
                      handleStopWithMessage()
                    } else {
                      sendMessage()
                    }
                  }}
                  disabled={!isConnected || (!isProcessing && !input.trim())}
                  className={`p-2 rounded-lg text-white transition-all ${
                    isProcessing && input.trim()
                      ? 'bg-orange-600 hover:bg-orange-500'
                      : 'bg-blue-600 hover:bg-blue-500 disabled:opacity-30 disabled:cursor-not-allowed'
                  }`}
                  title={isProcessing && input.trim() ? "Send and interrupt" : "Send message"}
                >
                  <Send size={16} />
                </button>
              </div>
            </div>
            {/* Helper text during processing */}
            {isProcessing && (
              <motion.p
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-xs text-zinc-500 mt-2 text-center"
              >
                Press <span className="text-orange-400">Stop</span> to cancel, or type a message to interrupt and redirect
              </motion.p>
            )}
          </div>
        </div>
      </div>

      {/* Right Sidebar - Workspace */}
      <AnimatePresence>
        {isWorkspaceOpen && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 480, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="border-l border-zinc-800/50 bg-zinc-900/50 flex flex-col shrink-0 overflow-hidden"
          >
            {/* Workspace Header */}
            <div className="flex items-center justify-between p-3 border-b border-zinc-800/50 bg-zinc-900/30">
              <div className="flex items-center gap-2">
                <FolderKanban size={14} className="text-zinc-500" />
                <span className="text-xs font-medium text-zinc-400 uppercase tracking-wider">Workspace</span>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={handleToggleFullscreen}
                  className="p-1.5 hover:bg-zinc-800 rounded-lg text-zinc-500 hover:text-zinc-300 transition-colors"
                  title="Fullscreen"
                >
                  <FileCode size={14} />
                </button>
                <button
                  onClick={toggleWorkspace}
                  className="p-1.5 hover:bg-zinc-800 rounded-lg text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                  <X size={14} />
                </button>
              </div>
            </div>

            <div className="flex-1 flex flex-col min-h-0">
              {/* File Explorer */}
              <div className="h-1/3 border-b border-zinc-800/50 flex flex-col min-h-0">
                <FileExplorer
                  projectId={currentProject?.id || null}
                  files={files}
                  onRefresh={fetchFiles}
                  onSelectFile={handleFileSelect}
                />
              </div>

              {/* File Viewer (Code Editor or PDF Viewer) */}
              <div className="flex-1 flex flex-col min-h-0">
                {renderFileViewer()}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Fullscreen Viewer Overlay */}
      <AnimatePresence>
        {isEditorFullscreen && selectedFile && currentProject && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed inset-0 z-50 bg-zinc-950 flex flex-col"
          >
            {renderFileViewer()}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Terminal Overlay */}
      <AnimatePresence>
        {isTerminalVisible && !isEditorFullscreen && (
          <motion.div
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed bottom-0 z-40 bg-zinc-900 border-t border-zinc-800/50 shadow-2xl"
            style={{
              left: '288px', // 72 * 4 = 288px (left sidebar width)
              right: isWorkspaceOpen ? '480px' : '0',
              height: '35vh'
            }}
          >
            <div className="flex items-center justify-between px-4 py-2 bg-zinc-800/50 border-b border-zinc-800 h-10">
              <div className="flex items-center gap-2 text-xs text-zinc-400">
                <TerminalIcon size={12} />
                <span className="font-medium uppercase tracking-wider">Terminal</span>
                <span className="text-zinc-600">read-only</span>
              </div>
              <button
                onClick={() => setIsTerminalVisible(false)}
                className="p-1 hover:bg-zinc-700 rounded-lg text-zinc-500 hover:text-zinc-300 transition-colors"
              >
                <ChevronDown size={14} />
              </button>
            </div>
            <div className="h-[calc(35vh-40px)]">
              <Terminal entries={terminalEntries} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App

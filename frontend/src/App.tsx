import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, AlertCircle, Terminal as TerminalIcon, FolderKanban } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import { Terminal } from './components/Terminal'
import type { TerminalEntry } from './components/Terminal'
import { FileExplorer } from './components/FileExplorer'
import { ProjectSelector } from './components/ProjectSelector'
import { CodeEditor } from './components/CodeEditor'

// Types
type Project = {
  id: string
  name: string
  description: string
  created_at: string
  updated_at: string
  status: string
}

type FileInfo = {
  name: string
  path: string
  is_dir: boolean
  size: number
  modified: string
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

type RightPanel = 'terminal' | 'files' | null

const API_BASE = 'http://localhost:8000'

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

  // Terminal state - populated by agent's tool calls
  const [terminalEntries, setTerminalEntries] = useState<TerminalEntry[]>([])

  // UI state
  const [rightPanel, setRightPanel] = useState<RightPanel>('terminal')
  const [isConnected, setIsConnected] = useState(false)
  const [selectedFile, setSelectedFile] = useState<string | null>(null)

  const ws = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Fetch projects on mount
  useEffect(() => {
    fetchProjects()
  }, [])

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

    // Connect to project chat
    const socket = new WebSocket(`ws://localhost:8000/ws/chat/${currentProject.id}`)
    ws.current = socket

    socket.onopen = () => {
      setIsConnected(true)
    }

    socket.onclose = () => {
      setIsConnected(false)
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'status') {
        // Status update (thinking, etc.)
      } else if (data.type === 'tool_call') {
        // Tool is being executed
        setCurrentToolCalls(prev => [...prev, {
          tool: data.tool,
          arguments: data.arguments,
          status: 'executing'
        }])

        // If it's a terminal command, add to terminal entries
        if (data.tool === 'terminal' && data.arguments?.command) {
          setTerminalEntries(prev => [...prev, {
            type: 'command',
            content: data.arguments.command as string,
            timestamp: new Date()
          }])
        }
      } else if (data.type === 'tool_result') {
        // Tool finished
        setCurrentToolCalls(prev =>
          prev.map((tc, idx) =>
            idx === prev.length - 1
              ? { ...tc, status: 'done', output: data.output, success: data.success }
              : tc
          )
        )

        // If it was a terminal command, add output to terminal
        if (data.tool === 'terminal' && data.output) {
          setTerminalEntries(prev => [...prev, {
            type: data.success ? 'output' : 'error',
            content: data.output,
            timestamp: new Date()
          }])
        }

        // If it was a file operation, refresh files
        if (['write_file', 'delete_file'].includes(data.tool)) {
          fetchFiles()
        }
      } else if (data.type === 'result') {
        // Final response
        setMessages(prev => [...prev, {
          role: 'agent',
          content: data.content,
          toolCalls: currentToolCalls.length > 0 ? [...currentToolCalls] : undefined
        }])
        setCurrentToolCalls([])
        setIsProcessing(false)
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
      }
    }

    // Fetch files for the project
    fetchFiles()
    fetchChatHistory()

    return () => {
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
      // Convert backend message format to frontend format
      const formattedMessages = (data.messages || []).map((msg: any) => ({
        role: msg.role === 'user' ? 'user' : 'agent',
        content: msg.content,
        toolCalls: undefined, // Tool calls are not persisted
        isError: false
      }))
      setMessages(formattedMessages)
    } catch (e) {
      console.error('Failed to fetch chat history:', e)
      setMessages([])
    }
  }

  const createProject = async (name: string, description: string) => {
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

  return (
    <div className="flex h-screen bg-neutral-950 text-neutral-100">
      {/* Left Sidebar - Projects */}
      <div className="w-56 border-r border-neutral-800 flex flex-col">
        <ProjectSelector
          projects={projects}
          currentProject={currentProject}
          onSelect={setCurrentProject}
          onCreate={createProject}
          onDelete={deleteProject}
        />
      </div>

      {/* Main Workspace - 3 Column Layout */}
      <div className="flex-1 flex min-w-0">
        {/* Left: File Explorer */}
        {currentProject && (
          <div className="w-64 border-r border-neutral-800">
            <FileExplorer
              projectId={currentProject.id}
              files={files}
              onRefresh={fetchFiles}
              onFileSelect={(file) => !file.is_dir && setSelectedFile(file.path)}
            />
          </div>
        )}

        {/* Center: Code Editor */}
        {currentProject && selectedFile && (
          <div className="w-96 border-r border-neutral-800">
            <CodeEditor
              projectId={currentProject.id}
              filePath={selectedFile}
              onClose={() => setSelectedFile(null)}
            />
          </div>
        )}

        {/* Right: Chat Area */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Header */}
          <header className="flex items-center justify-between px-4 py-3 border-b border-neutral-800">
            <div className="flex items-center gap-3">
              <h1 className="text-base font-medium text-neutral-100">
                {currentProject ? currentProject.name : 'Agent'}
              </h1>
              {currentProject && (
                <div className="flex items-center gap-1.5">
                  <div className={`w-1.5 h-1.5 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                  <span className="text-[10px] text-neutral-500">{isConnected ? 'Connected' : 'Disconnected'}</span>
                </div>
              )}
            </div>
            {currentProject && (
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setRightPanel(rightPanel === 'terminal' ? null : 'terminal')}
                  className={`p-2 rounded transition-colors ${rightPanel === 'terminal' ? 'bg-neutral-800 text-neutral-100' : 'text-neutral-500 hover:text-neutral-300'}`}
                  title="Terminal"
                >
                  <TerminalIcon size={16} />
                </button>
              </div>
            )}
          </header>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto">
            <div className="max-w-3xl mx-auto px-4 py-6 space-y-4">
              {!currentProject ? (
                <div className="text-center py-20">
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-neutral-800 mb-4">
                    <FolderKanban size={24} className="text-neutral-400" />
                  </div>
                  <h2 className="text-lg font-medium text-neutral-300 mb-2">
                    Select or create a project
                  </h2>
                  <p className="text-sm text-neutral-500 max-w-sm mx-auto">
                    Each project has its own workspace where the agent can create files and run code.
                  </p>
                </div>
              ) : messages.length === 0 ? (
                <div className="text-center py-20">
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-neutral-800 mb-4">
                    <Bot size={24} className="text-neutral-400" />
                  </div>
                  <h2 className="text-lg font-medium text-neutral-300 mb-2">
                    Ready to help
                  </h2>
                  <p className="text-sm text-neutral-500 max-w-sm mx-auto">
                    Ask me to create files, write code, or run commands. I'll work in this project's workspace.
                  </p>
                </div>
              ) : (
                messages.map((msg, idx) => (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    key={idx}
                    className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                  >
                    <div className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 ${
                      msg.role === 'user' ? 'bg-blue-600' :
                      msg.isError ? 'bg-red-600' : 'bg-neutral-700'
                    }`}>
                      {msg.role === 'user' ? <User size={14} /> :
                       msg.isError ? <AlertCircle size={14} /> : <Bot size={14} />}
                    </div>

                    <div className={`max-w-[85%] space-y-2 ${msg.role === 'user' ? 'text-right' : ''}`}>
                      {/* Tool calls summary */}
                      {msg.toolCalls && msg.toolCalls.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          {msg.toolCalls.map((tc, tcIdx) => (
                            <span
                              key={tcIdx}
                              className={`inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full ${
                                tc.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                              }`}
                            >
                              {tc.tool}
                              {tc.success ? ' ✓' : ' ✗'}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Message content */}
                      <div className={`inline-block px-3 py-2 rounded-2xl text-sm ${
                        msg.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : msg.isError
                            ? 'bg-red-500/10 border border-red-500/30 text-red-300'
                            : 'bg-neutral-800 text-neutral-100'
                      }`}>
                        {msg.role === 'agent' && !msg.isError ? (
                          <div className="prose prose-invert prose-sm max-w-none prose-p:my-1 prose-pre:bg-neutral-900 prose-pre:border prose-pre:border-neutral-700 prose-code:text-blue-300">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                          </div>
                        ) : (
                          <p className="whitespace-pre-wrap">{msg.content}</p>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))
              )}

              {/* Current tool calls (in progress) */}
              {currentToolCalls.length > 0 && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
                  <div className="w-7 h-7 rounded-full bg-neutral-700 flex items-center justify-center">
                    <Bot size={14} />
                  </div>
                  <div className="space-y-1">
                    {currentToolCalls.map((tc, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-xs text-neutral-400">
                        {tc.status === 'executing' ? (
                          <Loader2 size={12} className="animate-spin" />
                        ) : tc.success ? (
                          <span className="text-green-500">✓</span>
                        ) : (
                          <span className="text-red-500">✗</span>
                        )}
                        <span className="font-medium">{tc.tool}</span>
                        {tc.tool === 'terminal' && tc.arguments?.command && (
                          <code className="text-neutral-500">
                            {String(tc.arguments.command).slice(0, 30)}
                            {String(tc.arguments.command).length > 30 ? '...' : ''}
                          </code>
                        )}
                        {tc.tool === 'write_file' && tc.arguments?.path && (
                          <code className="text-neutral-500">{String(tc.arguments.path)}</code>
                        )}
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* Thinking indicator */}
              {isProcessing && currentToolCalls.length === 0 && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
                  <div className="w-7 h-7 rounded-full bg-neutral-700 flex items-center justify-center">
                    <Bot size={14} />
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-2">
                    <span className="w-1.5 h-1.5 bg-neutral-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-1.5 h-1.5 bg-neutral-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-1.5 h-1.5 bg-neutral-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input */}
          <div className="border-t border-neutral-800 p-3">
            <div className="max-w-3xl mx-auto flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                placeholder={currentProject ? "Ask me to create something..." : "Select a project first"}
                disabled={!currentProject || !isConnected}
                className="flex-1 bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-2.5 text-sm text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-600 disabled:opacity-50"
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || isProcessing || !isConnected}
                className="px-4 bg-blue-600 rounded-xl hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Right Panel - Terminal */}
      <AnimatePresence>
        {currentProject && rightPanel === 'terminal' && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 400, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="border-l border-neutral-800 overflow-hidden"
          >
            <Terminal entries={terminalEntries} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App

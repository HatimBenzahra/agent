import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, AlertCircle, Terminal as TerminalIcon, FolderKanban, Menu, X, FileCode } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import { Terminal } from './components/Terminal'
import type { TerminalEntry } from './components/Terminal'
import { FileExplorer } from './components/FileExplorer'
import type { FileInfo } from './components/FileExplorer'
import { ProjectSelector } from './components/ProjectSelector'
import { CodeEditor } from './components/CodeEditor'
import { PlanVisualizer } from './components/PlanVisualizer'
import type { StepEvent } from './components/PlanVisualizer'

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

  const ws = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Fetch projects on mount
  useEffect(() => {
    fetchProjects()
  }, [])

  // Auto-hide/show terminal logic
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
      } else if (data.type === 'plan_created') {
        setCurrentPlan(data.plan || [])
        setValidations({})
        setStepEvents({})
      } else if (data.type === 'step_started') {
        setCurrentStepId(data.step_id)
        setCurrentPlan(prev => prev.map(step => 
          step.id === data.step_id ? { ...step, status: 'executing' } : step
        ))
      } else if (data.type === 'step_validating') {
        setCurrentPlan(prev => prev.map(step => 
          step.id === data.step_id ? { ...step, status: 'validating' } : step
        ))
      } else if (data.type === 'step_completed') {
        setCurrentPlan(prev => prev.map(step => 
          step.id === data.step_id ? { ...step, status: 'completed' } : step
        ))
        if (data.validation) {
          setValidations(prev => ({ ...prev, [data.step_id]: data.validation }))
        }
      } else if (data.type === 'step_failed') {
        setCurrentPlan(prev => prev.map(step => 
          step.id === data.step_id ? { ...step, status: 'failed' } : step
        ))
        if (data.validation) {
          setValidations(prev => ({ ...prev, [data.step_id]: data.validation }))
        }
      } else if (data.type === 'tool_call') {
        setCurrentToolCalls(prev => [...prev, {
          tool: data.tool,
          arguments: data.arguments,
          status: 'executing'
        }])

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
          fetchFiles() // Refresh files list
        }
      } else if (data.type === 'sub_agent_tool') {
        const args = data.arguments || {}
        
        // 1. Update Terminal (Real-time)
        if (data.tool === 'terminal' && args.command) {
          // Add command entry
          setTerminalEntries(prev => [...prev, {
            type: 'command',
            content: args.command,
            timestamp: new Date()
          }])
          
          // Add output entry if present
          if (data.output) {
             setTerminalEntries(prev => [...prev, {
               type: data.success ? 'output' : 'error',
               content: data.output,
               timestamp: new Date()
             }])
          }
        }

        // 2. Update Files (Real-time)
        if (['write_file', 'delete_file'].includes(data.tool) && data.success) {
          fetchFiles() 
        }

        // 3. Update Plan Visualizer
        if (data.task_id && data.tool) {
          let message = `Using tool: ${data.tool}`
          
          if (data.tool === 'terminal') {
            message = `Executing: ${args.command || 'script'}`
          } else if (data.tool === 'write_file') {
            message = `Writing file: ${args.target_file || args.path || 'unknown'}`
          } else if (data.tool === 'read_file') {
            message = `Reading file: ${args.path || 'unknown'}`
          } else if (data.tool === 'list_files') {
            message = `Listing files in: ${args.path || '.'}`
          }

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

  const handleToggleFullscreen = () => {
    setIsEditorFullscreen(!isEditorFullscreen)
  }

  const toggleWorkspace = () => {
    setIsWorkspaceOpen(!isWorkspaceOpen)
  }

  return (
    <div className="flex h-screen bg-neutral-950 text-neutral-200 font-sans overflow-hidden">
      {/* 1. Left Sidebar - Projects (Conversations) */}
      <div className={`w-64 border-r border-neutral-800 bg-neutral-900 flex flex-col shrink-0 ${isMobileMenuOpen ? 'fixed inset-y-0 left-0 z-50' : 'hidden md:flex'}`}>
        <div className="p-4 border-b border-neutral-800 flex items-center justify-between">
          <div className="flex items-center gap-2 font-medium">
            <Bot size={20} className="text-blue-500" />
            <span>Agent Chat</span>
          </div>
          <button className="md:hidden" onClick={() => setIsMobileMenuOpen(false)}>
            <X size={16} />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2">
            <ProjectSelector 
              currentProject={currentProject}
              onSelect={setCurrentProject}
              projects={projects}
              onCreate={handleCreateProject}
              onDelete={deleteProject}
            />
        </div>
      </div>

      {/* 2. Main Content - Chat Interface (Central Focus) */}
      <div className="flex-1 flex flex-col min-w-0 bg-neutral-950 relative">
        {/* Header */}
        <header className="flex items-center justify-between px-4 py-3 border-b border-neutral-800 bg-neutral-900/50 backdrop-blur">
          <div className="flex items-center gap-3">
             <button className="md:hidden text-neutral-400" onClick={() => setIsMobileMenuOpen(true)}>
               <Menu size={20} />
             </button>
             <h1 className="font-medium text-neutral-100">
               {currentProject ? currentProject.name : 'Select a Conversation'}
             </h1>
             {currentProject && (
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} title={isConnected ? "Connected" : "Disconnected"} />
             )}
          </div>
          
          {currentProject && (
            <div className="flex items-center gap-2">
              <button 
                onClick={toggleWorkspace}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm transition-colors ${isWorkspaceOpen ? 'bg-blue-600/20 text-blue-400' : 'hover:bg-neutral-800 text-neutral-400'}`}
              >
                <FolderKanban size={16} />
                <span className="hidden sm:inline">Workspace</span>
              </button>
              <button
                onClick={() => setIsTerminalVisible(!isTerminalVisible)}
                className={`p-2 rounded-md transition-colors ${isTerminalVisible ? 'bg-neutral-800 text-neutral-100' : 'text-neutral-500 hover:text-neutral-300'}`}
                title="Toggle Terminal"
              >
                <TerminalIcon size={16} />
              </button>
            </div>
          )}
        </header>

        {/* Plan Visualizer (Top of Chat) */}
        {currentPlan.length > 0 && (
          <div className="border-b border-neutral-800">
            <PlanVisualizer 
              plan={currentPlan}
              currentStepId={currentStepId}
              validations={validations}
              stepEvents={stepEvents}
            />
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {messages.map((msg, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex items-start gap-4 ${msg.role === 'agent' ? 'bg-neutral-900/50 -mx-4 px-4 py-4 border-y border-neutral-800/50' : 'max-w-3xl ml-auto'}`}
            >
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${msg.role === 'agent' ? 'bg-blue-500/10 text-blue-400' : 'bg-neutral-800 text-neutral-400'}`}>
                {msg.role === 'agent' ? <Bot size={18} /> : <User size={18} />}
              </div>
              
              <div className="flex-1 min-w-0 space-y-2">
                <div className="prose prose-invert prose-sm max-w-none">
                  <ReactMarkdown 
                    components={{
                      code: ({node, inline, className, children, ...props}: any) => {
                        const match = /language-(\w+)/.exec(className || '')
                        return !inline && match ? (
                          <div className="relative group">
                            <div className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity">
                              <span className="text-xs text-neutral-500 font-mono">{match[1]}</span>
                            </div>
                            <pre className="bg-neutral-950 rounded-lg p-3 overflow-x-auto border border-neutral-800">
                              <code className={className} {...props}>
                                {children}
                              </code>
                            </pre>
                          </div>
                        ) : (
                          <code className="bg-neutral-800 rounded px-1 py-0.5 text-neutral-200" {...props}>
                            {children}
                          </code>
                        )
                      }
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                </div>

                {/* Tool Calls Display (Inline) */}
                {msg.toolCalls && msg.toolCalls.map((tc, tcIdx) => (
                  <div key={tcIdx} className="bg-neutral-900 border border-neutral-800 rounded-md overflow-hidden text-xs font-mono">
                    <div className="px-3 py-2 bg-neutral-800/50 flex items-center justify-between border-b border-neutral-800">
                      <div className="flex items-center gap-2">
                        <TerminalIcon size={12} className="text-neutral-500" />
                        <span className="text-neutral-300 font-semibold">{tc.tool}</span>
                      </div>
                      <span className={tc.status === 'done' ? (tc.success ? 'text-green-400' : 'text-red-400') : 'text-blue-400'}>
                         {tc.status === 'done' ? (tc.success ? 'Success' : 'Failed') : 'Executing...'}
                      </span>
                    </div>
                    {tc.output && (
                      <div className="p-3 max-h-40 overflow-y-auto whitespace-pre-wrap text-neutral-400">
                        {tc.output}
                      </div>
                    )}
                  </div>
                ))}
                
                {msg.isError && (
                  <div className="flex items-center gap-2 text-red-400 text-sm mt-2">
                    <AlertCircle size={16} />
                    <span>An error occurred processing this request.</span>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
          
          {isProcessing && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-2 text-neutral-500 text-sm px-4"
            >
              <Loader2 size={16} className="animate-spin" />
              <span>Agent is thinking...</span>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-neutral-900 border-t border-neutral-800">
          <div className="max-w-4xl mx-auto relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask me anything..."
              disabled={isProcessing || !isConnected}
              className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-4 py-3 pr-12 text-neutral-200 placeholder-neutral-600 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
            />
            <button
              onClick={sendMessage}
              disabled={isProcessing || !isConnected || !input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-blue-500 hover:text-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
      
      {/* 3. Right Sidebar - Collapsible Workspace (Explorer + Editor) */}
      <AnimatePresence>
        {isWorkspaceOpen && (
           <motion.div 
             initial={{ width: 0, opacity: 0 }}
             animate={{ width: 450, opacity: 1 }} // Fixed width for workspace
             exit={{ width: 0, opacity: 0 }}
             transition={{ type: "spring", stiffness: 300, damping: 30 }}
             className="border-l border-neutral-800 bg-neutral-900 flex flex-col shrink-0 overflow-hidden relative"
           >
              {/* Workspace Header & Fullscreen Toggle */}
              <div className="flex items-center justify-between p-2 border-b border-neutral-800 bg-neutral-800/50">
                <span className="text-xs font-medium text-neutral-400 px-2">WORKSPACE</span>
                <div className="flex items-center gap-1">
                   <button onClick={handleToggleFullscreen} className="p-1 hover:bg-neutral-700 rounded text-neutral-400" title="Fullscreen Editor">
                     <FileCode size={14} />
                   </button>
                   <button onClick={toggleWorkspace} className="p-1 hover:bg-neutral-700 rounded text-neutral-400">
                     <X size={14} />
                   </button>
                </div>
              </div>

             <div className="flex-1 flex flex-col min-h-0">
               {/* File Explorer (Top Half) */}
               <div className="h-1/3 border-b border-neutral-800 flex flex-col min-h-0">
                 <FileExplorer 
                   projectId={currentProject?.id || null}
                   files={files}
                   onRefresh={fetchFiles}
                   onSelectFile={(file) => setSelectedFile(file.path)}
                 />
               </div>
               
               {/* Code Editor (Bottom Half) */}
               <div className="flex-1 flex flex-col min-h-0">
                 {selectedFile && currentProject ? (
                   <CodeEditor 
                     projectId={currentProject.id}
                     filePath={selectedFile} 
                     onClose={() => setSelectedFile(null)}
                     readOnly={false}
                     isFullscreen={isEditorFullscreen} 
                     onToggleFullscreen={handleToggleFullscreen} 
                   />
                 ) : (
                   <div className="flex-1 flex items-center justify-center text-neutral-600 text-sm">
                     Select a file to edit
                   </div>
                 )}
               </div>
             </div>
           </motion.div>
        )}
      </AnimatePresence>

      {/* Fullscreen Editor Overlay */}
      <AnimatePresence>
        {isEditorFullscreen && selectedFile && currentProject && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed inset-0 z-50 bg-neutral-950 flex flex-col"
          >
             <CodeEditor 
               projectId={currentProject.id}
               filePath={selectedFile} 
               onClose={() => setIsEditorFullscreen(false)}
               readOnly={false}
               isFullscreen={true} 
               onToggleFullscreen={handleToggleFullscreen} 
             />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Auto-Hiding Terminal Overlay */}
      <AnimatePresence>
        {isTerminalVisible && !isEditorFullscreen && (
          <motion.div
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed bottom-0 left-64 right-0 z-40 bg-neutral-900 border-t border-neutral-800 shadow-2xl"
            style={{ height: '30vh', right: isWorkspaceOpen ? '450px' : '0' }} // Adjust right based on workspace
          >
             <div className="flex items-center justify-between px-4 py-2 bg-neutral-800 border-b border-neutral-700 h-10">
               <span className="text-xs font-medium text-neutral-400 flex items-center gap-2">
                 <TerminalIcon size={12} />
                 TERMINAL
               </span>
               <button 
                 onClick={() => setIsTerminalVisible(false)}
                 className="text-neutral-500 hover:text-neutral-300"
               >
                 <X size={14} />
               </button>
             </div>
             <div className="h-[calc(30vh-40px)]">
               <Terminal entries={terminalEntries} />
             </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App

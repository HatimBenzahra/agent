import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, CheckCircle2, Circle, Loader2, Zap, AlertCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'

type Step = {
  instruction: string
  complexity: string
}

type Message = {
  role: 'user' | 'agent'
  content: string
  plan?: Step[]
  isPlanning?: boolean
  isError?: boolean
}

type ConnectionStatus = 'connecting' | 'connected' | 'disconnected'

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentPlan, setCurrentPlan] = useState<Step[] | null>(null)
  const [activeStep, setActiveStep] = useState<number>(0)
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('connecting')
  const ws = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (ws.current && ws.current.readyState !== WebSocket.CLOSED) return

    const socket = new WebSocket('ws://localhost:8000/ws/chat')
    ws.current = socket

    socket.onopen = () => {
      console.log('Connected to backend')
      setConnectionStatus('connected')
    }

    socket.onclose = () => {
      setConnectionStatus('disconnected')
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'plan') {
        setCurrentPlan(data.data)
        setActiveStep(0)
        setMessages(prev => [...prev, {
          role: 'agent',
          content: `Planning ${data.data.length} steps...`,
          plan: data.data,
          isPlanning: true
        }])
      }
      else if (data.type === 'log') {
        if (data.status === 'started') {
          setActiveStep(data.step || 0)
        }
      }
      else if (data.type === 'result') {
        setMessages(prev => [...prev, { role: 'agent', content: data.content }])
        setIsProcessing(false)
        setCurrentPlan(null)
        setActiveStep(0)
      }
      else if (data.type === 'error') {
        setMessages(prev => [...prev, {
          role: 'agent',
          content: data.content,
          isError: true
        }])
        setIsProcessing(false)
        setCurrentPlan(null)
      }
    }

    return () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close()
      }
    }
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, currentPlan, activeStep])

  const sendMessage = () => {
    if (!input.trim() || isProcessing || connectionStatus !== 'connected') return
    const msg = input
    setInput('')
    setIsProcessing(true)
    setMessages(prev => [...prev, { role: 'user', content: msg }])
    ws.current?.send(msg)
  }

  return (
    <div className="flex h-screen bg-neutral-950 text-neutral-100">
      {/* Sidebar - Plan Visualizer */}
      <AnimatePresence>
        {currentPlan && (
          <motion.aside
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 320, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="border-r border-neutral-800 bg-neutral-900 overflow-hidden"
          >
            <div className="p-5 h-full overflow-y-auto">
              <div className="flex items-center gap-2 mb-5 text-neutral-400 text-sm font-medium uppercase tracking-wide">
                <Zap size={14} />
                <span>Execution Plan</span>
              </div>

              <div className="space-y-1">
                {currentPlan.map((step, idx) => {
                  const stepNum = idx + 1
                  const isActive = activeStep === stepNum
                  const isDone = activeStep > stepNum

                  return (
                    <div
                      key={idx}
                      className={`flex items-start gap-3 p-3 rounded-lg transition-colors ${
                        isActive ? 'bg-neutral-800' : ''
                      }`}
                    >
                      <div className={`mt-0.5 ${
                        isDone ? 'text-green-500' :
                        isActive ? 'text-blue-500' :
                        'text-neutral-600'
                      }`}>
                        {isDone ? (
                          <CheckCircle2 size={16} />
                        ) : isActive ? (
                          <Loader2 size={16} className="animate-spin" />
                        ) : (
                          <Circle size={16} />
                        )}
                      </div>

                      <div className="flex-1 min-w-0">
                        <p className={`text-sm leading-snug ${
                          isDone ? 'text-neutral-400' :
                          isActive ? 'text-neutral-100' :
                          'text-neutral-500'
                        }`}>
                          {step.instruction}
                        </p>
                        {step.complexity === 'COMPLEX' && (
                          <span className="inline-block mt-1.5 text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400">
                            Complex
                          </span>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-4 border-b border-neutral-800">
          <h1 className="text-lg font-semibold text-neutral-100">
            Agent
          </h1>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              connectionStatus === 'connected' ? 'bg-green-500' :
              connectionStatus === 'connecting' ? 'bg-yellow-500 animate-pulse' :
              'bg-red-500'
            }`} />
            <span className="text-xs text-neutral-500 capitalize">
              {connectionStatus}
            </span>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
            {messages.length === 0 && (
              <div className="text-center py-20">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-neutral-800 mb-4">
                  <Bot size={24} className="text-neutral-400" />
                </div>
                <h2 className="text-lg font-medium text-neutral-300 mb-2">
                  How can I help you?
                </h2>
                <p className="text-sm text-neutral-500 max-w-sm mx-auto">
                  Ask me anything. For complex tasks, I'll create a plan and execute it step by step.
                </p>
              </div>
            )}

            {messages.map((msg, idx) => (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.15 }}
                key={idx}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                  msg.role === 'user' ? 'bg-blue-600' :
                  msg.isError ? 'bg-red-600' :
                  'bg-neutral-700'
                }`}>
                  {msg.role === 'user' ? (
                    <User size={14} />
                  ) : msg.isError ? (
                    <AlertCircle size={14} />
                  ) : (
                    <Bot size={14} />
                  )}
                </div>

                <div className={`max-w-[85%] ${msg.role === 'user' ? 'text-right' : ''}`}>
                  {msg.isPlanning ? (
                    <div className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-neutral-800 text-neutral-400 text-sm">
                      <Loader2 size={14} className="animate-spin" />
                      <span>Executing {msg.plan?.length} steps...</span>
                    </div>
                  ) : (
                    <div className={`inline-block px-4 py-3 rounded-2xl text-sm ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : msg.isError
                          ? 'bg-red-500/10 border border-red-500/30 text-red-300'
                          : 'bg-neutral-800 text-neutral-100'
                    }`}>
                      {msg.role === 'agent' && !msg.isError ? (
                        <div className="prose prose-invert prose-sm max-w-none prose-p:my-1 prose-pre:bg-neutral-900 prose-pre:border prose-pre:border-neutral-700">
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                      ) : (
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                      )}
                    </div>
                  )}
                </div>
              </motion.div>
            ))}

            {isProcessing && !currentPlan && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex gap-3"
              >
                <div className="w-8 h-8 rounded-full bg-neutral-700 flex items-center justify-center">
                  <Bot size={14} />
                </div>
                <div className="flex items-center gap-1.5 px-4 py-3">
                  <span className="w-2 h-2 bg-neutral-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-neutral-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-neutral-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <div className="border-t border-neutral-800 p-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                placeholder="Message..."
                disabled={connectionStatus !== 'connected'}
                className="flex-1 bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-3 text-sm text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-600 disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || isProcessing || connectionStatus !== 'connected'}
                className="px-4 bg-blue-600 rounded-xl hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

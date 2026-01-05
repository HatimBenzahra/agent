import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, CheckCircle2, Circle, Loader2, BrainCircuit } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

type Step = {
  instruction: string
  complexity: string
}

type Log = {
  step?: number
  total?: number
  instruction?: string
  status?: 'started' | 'completed'
  duration?: string
  content?: string
}

type Message = {
  role: 'user' | 'agent'
  content: string
  plan?: Step[]
  logs?: Log[]
  type?: 'text' | 'plan_start' | 'result'
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentPlan, setCurrentPlan] = useState<Step[] | null>(null)
  const [activeStep, setActiveStep] = useState<number>(0)
  const ws = useRef<WebSocket | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Prevent double connection in StrictMode
    if (ws.current && ws.current.readyState !== WebSocket.CLOSED) return;

    const socket = new WebSocket('ws://localhost:8000/ws/chat')
    ws.current = socket
    
    socket.onopen = () => console.log('Connected to backend')
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'plan') {
        setCurrentPlan(data.data)
        setActiveStep(0)
        setMessages(prev => [...prev, { role: 'agent', content: '', plan: data.data, type: 'plan_start' }])
      } 
      else if (data.type === 'log') {
        if (data.status === 'started') {
          setActiveStep(data.step || 0)
        }
      } 
      else if (data.type === 'result') {
        setMessages(prev => [...prev, { role: 'agent', content: data.content, type: 'result' }])
        setIsProcessing(false)
        setCurrentPlan(null)
      }
      else if (data.type === 'error') {
         setMessages(prev => [...prev, { role: 'agent', content: `Error: ${data.content}`, type: 'result' }])
         setIsProcessing(false)
      }
    }

    return () => {
        // Cleanup on unmount
        if (socket.readyState === WebSocket.OPEN) {
            socket.close()
        }
    }
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, currentPlan])

  const sendMessage = () => {
    if (!input.trim()) return
    const msg = input
    setInput('')
    setIsProcessing(true)
    setMessages(prev => [...prev, { role: 'user', content: msg }])
    ws.current?.send(msg)
  }

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 font-sans overflow-hidden">
      {/* Sidebar / Plan Visualizer */}
      <AnimatePresence>
        {currentPlan && (
          <motion.div 
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 400, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            className="border-r border-gray-800 bg-gray-950 p-6 overflow-y-auto"
          >
            <div className="flex items-center gap-2 mb-6 text-purple-400">
               <BrainCircuit size={24} />
               <h2 className="text-xl font-bold">Active Plan</h2>
            </div>
            
            <div className="space-y-6">
              {currentPlan.map((step, idx) => {
                const stepNum = idx + 1
                const isActive = activeStep === stepNum
                const isDone = activeStep > stepNum
                
                return (
                  <div key={idx} className={`relative pl-8 border-l-2 ${isActive ? 'border-purple-500' : isDone ? 'border-green-500' : 'border-gray-800'} transition-all duration-300`}>
                    <div className={`absolute -left-[9px] top-0 rounded-full p-1 ${isActive ? 'bg-purple-500' : isDone ? 'bg-green-500' : 'bg-gray-800'}`}>
                      {isDone ? <CheckCircle2 size={12} /> : isActive ? <Loader2 size={12} className="animate-spin" /> : <Circle size={12} />}
                    </div>
                    
                    <h3 className={`text-sm font-semibold mb-1 ${isActive ? 'text-purple-300' : isDone ? 'text-green-300' : 'text-gray-500'}`}>
                      Step {stepNum}
                    </h3>
                    <p className={`text-sm ${isActive || isDone ? 'text-gray-200' : 'text-gray-600'}`}>
                      {step.instruction}
                    </p>
                    <span className={`text-[10px] mt-2 inline-block px-2 py-0.5 rounded ${step.complexity === 'COMPLEX' ? 'bg-yellow-900 text-yellow-200' : 'bg-blue-900 text-blue-200'}`}>
                      {step.complexity}
                    </span>
                  </div>
                )
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full">
        {/* Header */}
        <header className="p-6 border-b border-gray-800 flex justify-between items-center bg-gray-900/50 backdrop-blur">
           <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
             Orchestrator Agent
           </h1>
           <div className="text-xs text-gray-500">v2.0 (Full Stack)</div>
        </header>

        {/* Message List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-gray-800">
          {messages.map((msg, idx) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={idx} 
              className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-blue-600' : 'bg-purple-600'}`}>
                {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              
              <div className={`max-w-[80%] rounded-2xl p-4 ${
                msg.role === 'user' 
                  ? 'bg-blue-600/20 border border-blue-500/30' 
                  : msg.type === 'plan_start' 
                    ? 'bg-transparent border border-gray-700/50 italic text-gray-400'
                    : 'bg-gray-800/50 border border-gray-700'
              }`}>
                 {msg.type === 'plan_start' ? (
                   <span>Generating a plan with {msg.plan?.length} steps... (See visualizer)</span>
                 ) : (
                    <div className="prose prose-invert max-w-none text-sm whitespace-pre-wrap">
                      {msg.content}
                    </div>
                 )}
              </div>
            </motion.div>
          ))}
          {isProcessing && !currentPlan && (
            <div className="flex gap-4">
              <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center shrink-0 animate-pulse">
                <Bot size={16} />
              </div>
              <div className="flex items-center text-gray-500 text-sm">
                Thinking...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-800 bg-gray-900">
          <div className="relative max-w-3xl mx-auto">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask me anything... (e.g. 'Create a snake game')"
              className="w-full bg-gray-800 border border-gray-700 rounded-xl py-3 px-5 pr-12 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
            />
            <button 
              onClick={sendMessage}
              disabled={!input.trim() || isProcessing}
              className="absolute right-2 top-2 p-1.5 bg-purple-600 rounded-lg hover:bg-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

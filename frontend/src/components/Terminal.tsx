import { useState, useRef, useEffect, KeyboardEvent } from 'react'
import { TerminalIcon } from 'lucide-react'

type TerminalLine = {
  type: 'input' | 'output' | 'error' | 'prompt'
  content: string
  cwd?: string
}

type TerminalProps = {
  projectId: string | null
}

export function Terminal({ projectId }: TerminalProps) {
  const [lines, setLines] = useState<TerminalLine[]>([])
  const [input, setInput] = useState('')
  const [cwd, setCwd] = useState('/')
  const [isConnected, setIsConnected] = useState(false)
  const [history, setHistory] = useState<string[]>([])
  const [historyIndex, setHistoryIndex] = useState(-1)

  const ws = useRef<WebSocket | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!projectId) {
      setLines([{ type: 'output', content: 'Select a project to use the terminal.' }])
      return
    }

    // Connect to terminal WebSocket
    const socket = new WebSocket(`ws://localhost:8000/ws/terminal/${projectId}`)
    ws.current = socket

    socket.onopen = () => {
      setIsConnected(true)
      setLines([{ type: 'output', content: `Connected to project workspace.` }])
    }

    socket.onclose = () => {
      setIsConnected(false)
      setLines(prev => [...prev, { type: 'error', content: 'Disconnected from terminal.' }])
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'prompt') {
        setCwd(data.cwd)
      } else if (data.type === 'output') {
        const newLines: TerminalLine[] = []

        if (data.stdout) {
          newLines.push({ type: 'output', content: data.stdout })
        }
        if (data.stderr) {
          newLines.push({ type: 'error', content: data.stderr })
        }

        setLines(prev => [...prev, ...newLines])
      }
    }

    return () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close()
      }
    }
  }, [projectId])

  // Auto-scroll to bottom
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [lines])

  const executeCommand = () => {
    if (!input.trim() || !ws.current || !isConnected) return

    const command = input.trim()

    // Add to history
    setHistory(prev => [...prev, command])
    setHistoryIndex(-1)

    // Add input line to display
    setLines(prev => [...prev, { type: 'input', content: `${cwd} $ ${command}` }])

    // Send command
    ws.current.send(JSON.stringify({ type: 'command', command }))

    // Clear input
    setInput('')
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      executeCommand()
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      if (history.length > 0) {
        const newIndex = historyIndex < history.length - 1 ? historyIndex + 1 : historyIndex
        setHistoryIndex(newIndex)
        setInput(history[history.length - 1 - newIndex] || '')
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault()
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1
        setHistoryIndex(newIndex)
        setInput(history[history.length - 1 - newIndex] || '')
      } else {
        setHistoryIndex(-1)
        setInput('')
      }
    }
  }

  const focusInput = () => {
    inputRef.current?.focus()
  }

  return (
    <div className="flex flex-col h-full bg-neutral-950 font-mono text-sm">
      {/* Header */}
      <div className="flex items-center gap-2 px-3 py-2 bg-neutral-900 border-b border-neutral-800">
        <TerminalIcon size={14} className="text-neutral-500" />
        <span className="text-neutral-400 text-xs">Terminal</span>
        <div className={`ml-auto w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
      </div>

      {/* Output */}
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto p-3 space-y-1 cursor-text"
        onClick={focusInput}
      >
        {lines.map((line, idx) => (
          <div
            key={idx}
            className={`whitespace-pre-wrap break-all ${
              line.type === 'input' ? 'text-blue-400' :
              line.type === 'error' ? 'text-red-400' :
              'text-neutral-300'
            }`}
          >
            {line.content}
          </div>
        ))}

        {/* Current prompt */}
        {isConnected && (
          <div className="flex items-center gap-2">
            <span className="text-green-400">{cwd} $</span>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1 bg-transparent outline-none text-neutral-100 caret-neutral-100"
              autoFocus
              spellCheck={false}
            />
          </div>
        )}
      </div>
    </div>
  )
}

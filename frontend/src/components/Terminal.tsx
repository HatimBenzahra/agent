import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Terminal as TerminalIcon } from 'lucide-react'

export type TerminalEntry = {
  type: 'command' | 'output' | 'error'
  content: string
  timestamp: Date
}

type TerminalProps = {
  entries: TerminalEntry[]
}

export function Terminal({ entries }: TerminalProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new entries arrive
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [entries])

  return (
    <div className="flex flex-col h-full bg-zinc-950 font-mono text-xs">
      {/* Output */}
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto p-4 space-y-3"
      >
        {entries.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <TerminalIcon size={28} className="text-zinc-800 mb-2" />
            <p className="text-zinc-600 text-xs">Terminal output will appear here</p>
          </div>
        ) : (
          entries.map((entry, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.15 }}
              className="space-y-1"
            >
              {entry.type === 'command' && (
                <div className="flex items-start gap-2">
                  <span className="text-emerald-500 select-none">$</span>
                  <span className="text-blue-400 break-all">{entry.content}</span>
                </div>
              )}
              {entry.type === 'output' && (
                <pre className="text-zinc-400 whitespace-pre-wrap pl-4 leading-relaxed break-all">
                  {entry.content}
                </pre>
              )}
              {entry.type === 'error' && (
                <pre className="text-red-400 whitespace-pre-wrap pl-4 leading-relaxed break-all">
                  {entry.content}
                </pre>
              )}
            </motion.div>
          ))
        )}
      </div>
    </div>
  )
}

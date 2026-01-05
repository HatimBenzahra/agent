import { useEffect, useRef } from 'react'
import { TerminalIcon } from 'lucide-react'

type TerminalEntry = {
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
    <div className="flex flex-col h-full bg-neutral-950 font-mono text-xs">
      {/* Header */}
      <div className="flex items-center gap-2 px-3 py-2 bg-neutral-900 border-b border-neutral-800">
        <TerminalIcon size={14} className="text-neutral-500" />
        <span className="text-neutral-400 text-xs">Agent Terminal</span>
        <span className="ml-auto text-[10px] text-neutral-600">read-only</span>
      </div>

      {/* Output - Read Only */}
      <div
        ref={containerRef}
        className="flex-1 overflow-y-auto p-3 space-y-2"
      >
        {entries.length === 0 ? (
          <div className="text-neutral-600 text-center py-8">
            The agent's terminal activity will appear here.
          </div>
        ) : (
          entries.map((entry, idx) => (
            <div key={idx} className="space-y-0.5">
              {entry.type === 'command' && (
                <div className="flex items-center gap-2">
                  <span className="text-green-500">$</span>
                  <span className="text-blue-400">{entry.content}</span>
                </div>
              )}
              {entry.type === 'output' && (
                <pre className="text-neutral-300 whitespace-pre-wrap pl-4">
                  {entry.content}
                </pre>
              )}
              {entry.type === 'error' && (
                <pre className="text-red-400 whitespace-pre-wrap pl-4">
                  {entry.content}
                </pre>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export type { TerminalEntry }

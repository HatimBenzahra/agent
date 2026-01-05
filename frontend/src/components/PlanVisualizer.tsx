import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  CheckCircle2,
  Circle,
  Loader2,
  XCircle,
  ChevronDown,
  ChevronRight,
  Terminal,
  FileEdit,
  FileSearch,
  Check,
  Zap,
  Clock,
  AlertTriangle,
  Sparkles,
  List
} from 'lucide-react'

type PlanStep = {
  id: string
  objective: string
  status: 'pending' | 'executing' | 'validating' | 'completed' | 'failed'
}

type Validation = {
  success: boolean
  feedback: string
}

export type StepEvent = {
  type: 'tool' | 'log'
  tool?: string
  message: string
  status?: 'running' | 'success' | 'error'
  timestamp: number
}

type PlanVisualizerProps = {
  plan: PlanStep[]
  currentStepId?: string
  validations?: Record<string, Validation>
  stepEvents?: Record<string, StepEvent[]>
}

export function PlanVisualizer({ plan, currentStepId, validations = {}, stepEvents = {} }: PlanVisualizerProps) {
  const [expandedSteps, setExpandedSteps] = useState<Set<string>>(new Set())
  const [isCollapsed, setIsCollapsed] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  // Auto-expand current step
  useEffect(() => {
    if (currentStepId && !expandedSteps.has(currentStepId)) {
      setExpandedSteps(prev => new Set(prev).add(currentStepId))
    }
  }, [currentStepId])

  // Scroll to current step
  useEffect(() => {
    if (currentStepId && containerRef.current) {
      const stepElement = containerRef.current.querySelector(`[data-step-id="${currentStepId}"]`)
      if (stepElement) {
        stepElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
      }
    }
  }, [currentStepId])

  if (plan.length === 0) return null

  const toggleStep = (id: string) => {
    setExpandedSteps(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const completedCount = plan.filter(s => s.status === 'completed').length
  const progress = (completedCount / plan.length) * 100

  const getStepIcon = (step: PlanStep) => {
    const iconClass = "w-5 h-5"
    switch (step.status) {
      case 'completed':
        return (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="p-1 rounded-full bg-emerald-500/20"
          >
            <CheckCircle2 className={`${iconClass} text-emerald-400`} />
          </motion.div>
        )
      case 'failed':
        return (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="p-1 rounded-full bg-red-500/20"
          >
            <XCircle className={`${iconClass} text-red-400`} />
          </motion.div>
        )
      case 'executing':
        return (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="p-1 rounded-full bg-blue-500/20"
          >
            <Zap className={`${iconClass} text-blue-400`} />
          </motion.div>
        )
      case 'validating':
        return (
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 1, repeat: Infinity }}
            className="p-1 rounded-full bg-violet-500/20"
          >
            <Sparkles className={`${iconClass} text-violet-400`} />
          </motion.div>
        )
      default:
        return (
          <div className="p-1 rounded-full bg-zinc-800">
            <Circle className={`${iconClass} text-zinc-500`} />
          </div>
        )
    }
  }

  const getStatusBadge = (step: PlanStep) => {
    const baseClass = "px-2 py-0.5 rounded-full text-[10px] font-medium uppercase tracking-wide"
    switch (step.status) {
      case 'completed':
        return <span className={`${baseClass} bg-emerald-500/10 text-emerald-400`}>Done</span>
      case 'failed':
        return <span className={`${baseClass} bg-red-500/10 text-red-400`}>Failed</span>
      case 'executing':
        return (
          <span className={`${baseClass} bg-blue-500/10 text-blue-400 flex items-center gap-1`}>
            <Loader2 size={10} className="animate-spin" />
            Running
          </span>
        )
      case 'validating':
        return (
          <span className={`${baseClass} bg-violet-500/10 text-violet-400 flex items-center gap-1`}>
            <Loader2 size={10} className="animate-spin" />
            Validating
          </span>
        )
      default:
        return <span className={`${baseClass} bg-zinc-800 text-zinc-500`}>Pending</span>
    }
  }

  const getEventIcon = (event: StepEvent) => {
    const iconClass = "w-3 h-3"
    if (event.tool === 'terminal') return <Terminal className={iconClass} />
    if (event.tool === 'write_file') return <FileEdit className={iconClass} />
    if (event.tool === 'read_file') return <FileSearch className={iconClass} />
    return <Circle className={iconClass} />
  }

  const getStepBorderColor = (step: PlanStep, isCurrent: boolean) => {
    if (isCurrent) {
      switch (step.status) {
        case 'executing': return 'border-blue-500/50 bg-blue-500/5'
        case 'validating': return 'border-violet-500/50 bg-violet-500/5'
        default: return 'border-zinc-700 bg-zinc-800/50'
      }
    }
    switch (step.status) {
      case 'completed': return 'border-emerald-500/20 bg-emerald-500/5'
      case 'failed': return 'border-red-500/20 bg-red-500/5'
      default: return 'border-zinc-800 bg-zinc-900/50'
    }
  }

  return (
    <div className="bg-zinc-900/80 glass-subtle">
      {/* Header with Progress */}
      <div
        className="flex items-center justify-between px-4 py-3 cursor-pointer hover:bg-zinc-800/30 transition-colors"
        onClick={() => setIsCollapsed(!isCollapsed)}
      >
        <div className="flex items-center gap-3">
          <div className="p-1.5 rounded-lg bg-gradient-to-br from-blue-500/20 to-violet-500/20">
            <List size={16} className="text-blue-400" />
          </div>
          <div>
            <h3 className="text-sm font-medium text-zinc-200 flex items-center gap-2">
              Execution Plan
              <span className="text-xs text-zinc-500 font-normal">
                {completedCount}/{plan.length} steps
              </span>
            </h3>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Mini progress bar */}
          <div className="w-24 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-blue-500 to-emerald-500 rounded-full relative progress-shine"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5, ease: "easeOut" }}
            />
          </div>
          <motion.div
            animate={{ rotate: isCollapsed ? 0 : 180 }}
            transition={{ duration: 0.2 }}
          >
            <ChevronDown size={16} className="text-zinc-500" />
          </motion.div>
        </div>
      </div>

      {/* Plan Steps */}
      <AnimatePresence>
        {!isCollapsed && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div
              ref={containerRef}
              className="px-4 pb-4 max-h-80 overflow-y-auto space-y-2"
            >
              {plan.map((step, index) => {
                const isExpanded = expandedSteps.has(step.id)
                const isCurrent = step.id === currentStepId
                const events = stepEvents[step.id] || []
                const validation = validations[step.id]

                return (
                  <motion.div
                    key={step.id}
                    data-step-id={step.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className={`relative border rounded-xl transition-all duration-300 ${getStepBorderColor(step, isCurrent)} ${
                      isCurrent ? 'animate-pulse-glow' : ''
                    }`}
                  >
                    {/* Step Header */}
                    <div
                      className="flex items-start gap-3 p-3 cursor-pointer select-none"
                      onClick={() => toggleStep(step.id)}
                    >
                      {/* Timeline connector */}
                      <div className="relative flex flex-col items-center">
                        {getStepIcon(step)}
                        {index < plan.length - 1 && (
                          <div className={`w-0.5 h-full absolute top-8 ${
                            step.status === 'completed' ? 'bg-emerald-500/30' : 'bg-zinc-700'
                          }`} style={{ height: '100%', minHeight: '20px' }} />
                        )}
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2 mb-1">
                          <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider">
                            Step {index + 1}
                          </span>
                          {getStatusBadge(step)}
                        </div>
                        <p className={`text-sm font-medium leading-relaxed ${
                          step.status === 'completed' ? 'text-zinc-400' :
                          step.status === 'failed' ? 'text-red-300' :
                          isCurrent ? 'text-zinc-100' : 'text-zinc-300'
                        }`}>
                          {step.objective}
                        </p>

                        {/* Quick event preview */}
                        {events.length > 0 && !isExpanded && (
                          <div className="flex items-center gap-2 mt-2 text-[11px] text-zinc-500">
                            <span>{events.length} action{events.length > 1 ? 's' : ''}</span>
                            <ChevronRight size={12} />
                          </div>
                        )}
                      </div>

                      {/* Expand indicator */}
                      <motion.div
                        animate={{ rotate: isExpanded ? 90 : 0 }}
                        className="text-zinc-500 mt-1"
                      >
                        <ChevronRight size={14} />
                      </motion.div>
                    </div>

                    {/* Expanded Details */}
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.2 }}
                          className="overflow-hidden border-t border-zinc-800/50"
                        >
                          <div className="px-4 py-3 pl-12 space-y-3">
                            {/* Events Timeline */}
                            {events.length > 0 && (
                              <div className="space-y-2">
                                <span className="text-[10px] font-medium text-zinc-500 uppercase tracking-wider">
                                  Activity
                                </span>
                                <div className="space-y-1.5 relative">
                                  <div className="absolute left-1.5 top-2 bottom-2 w-px bg-zinc-800" />
                                  {events.map((event, idx) => (
                                    <motion.div
                                      key={idx}
                                      initial={{ opacity: 0, x: -10 }}
                                      animate={{ opacity: 1, x: 0 }}
                                      transition={{ delay: idx * 0.05 }}
                                      className="flex items-start gap-3 pl-5 relative"
                                    >
                                      <div className={`absolute left-0 top-1 p-0.5 rounded-full ${
                                        event.status === 'success' ? 'bg-emerald-500/20 text-emerald-400' :
                                        event.status === 'error' ? 'bg-red-500/20 text-red-400' :
                                        'bg-blue-500/20 text-blue-400'
                                      }`}>
                                        {getEventIcon(event)}
                                      </div>
                                      <span className={`text-xs leading-relaxed ${
                                        event.status === 'success' ? 'text-zinc-400' :
                                        event.status === 'error' ? 'text-red-300' :
                                        'text-zinc-300'
                                      }`}>
                                        {event.message}
                                      </span>
                                    </motion.div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Validation Result */}
                            {validation && (
                              <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`p-3 rounded-lg flex items-start gap-3 ${
                                  validation.success
                                    ? 'bg-emerald-500/10 border border-emerald-500/20'
                                    : 'bg-red-500/10 border border-red-500/20'
                                }`}
                              >
                                <div className={`p-1 rounded-full ${
                                  validation.success ? 'bg-emerald-500/20' : 'bg-red-500/20'
                                }`}>
                                  {validation.success ? (
                                    <Check size={12} className="text-emerald-400" />
                                  ) : (
                                    <AlertTriangle size={12} className="text-red-400" />
                                  )}
                                </div>
                                <div className="flex-1 min-w-0">
                                  <span className={`text-xs font-medium ${
                                    validation.success ? 'text-emerald-300' : 'text-red-300'
                                  }`}>
                                    {validation.success ? 'Validation Passed' : 'Validation Failed'}
                                  </span>
                                  <p className={`text-xs mt-1 leading-relaxed ${
                                    validation.success ? 'text-emerald-400/80' : 'text-red-400/80'
                                  }`}>
                                    {validation.feedback}
                                  </p>
                                </div>
                              </motion.div>
                            )}

                            {/* Pending state */}
                            {step.status === 'pending' && events.length === 0 && (
                              <div className="flex items-center gap-2 text-xs text-zinc-600">
                                <Clock size={12} />
                                <span>Waiting to start...</span>
                              </div>
                            )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

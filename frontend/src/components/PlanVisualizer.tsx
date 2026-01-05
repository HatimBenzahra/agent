import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle2, Circle, Loader2, XCircle, AlertCircle, ChevronDown, ChevronRight, Terminal, FileEdit, FileSearch, Check } from 'lucide-react'

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

  if (plan.length === 0) return null

  // Auto-expand current step
  if (currentStepId && !expandedSteps.has(currentStepId)) {
    setExpandedSteps(prev => new Set(prev).add(currentStepId))
  }

  const toggleStep = (id: string) => {
    setExpandedSteps(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const getStepIcon = (step: PlanStep) => {
    switch (step.status) {
      case 'completed': return <CheckCircle2 size={18} className="text-green-400" />
      case 'failed': return <XCircle size={18} className="text-red-400" />
      case 'executing':
      case 'validating': return <Loader2 size={18} className="text-blue-400 animate-spin" />
      default: return <Circle size={18} className="text-neutral-500" />
    }
  }

  const getStepColor = (step: PlanStep) => {
    switch (step.status) {
      case 'completed': return 'border-green-500/30 bg-green-500/5'
      case 'failed': return 'border-red-500/30 bg-red-500/5'
      case 'executing':
      case 'validating': return 'border-blue-500/30 bg-blue-500/5'
      default: return 'border-neutral-700 bg-neutral-800/30'
    }
  }

  const getEventIcon = (event: StepEvent) => {
    if (event.tool === 'terminal') return <Terminal size={12} />
    if (event.tool === 'write_file') return <FileEdit size={12} />
    if (event.tool === 'read_file') return <FileSearch size={12} />
    return <Circle size={10} />
  }

  return (
    <div className="bg-neutral-900 border-b border-neutral-800 p-4">
      <div className="max-w-4xl mx-auto">
        <h3 className="text-sm font-medium text-neutral-300 mb-3 flex items-center gap-2">
          <AlertCircle size={14} />
          Execution Plan
        </h3>
        
        <div className="space-y-2">
          {plan.map((step, index) => {
            const isExpanded = expandedSteps.has(step.id)
            const events = stepEvents[step.id] || []
            const validation = validations[step.id]

            return (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`relative border rounded-lg transition-all ${getStepColor(step)} ${
                  step.id === currentStepId ? 'ring-1 ring-blue-400' : ''
                }`}
              >
                {/* Header Row */}
                <div 
                  className="flex items-start gap-3 p-3 cursor-pointer select-none"
                  onClick={() => toggleStep(step.id)}
                >
                  <div className="shrink-0 mt-0.5">
                    {getStepIcon(step)}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-neutral-500">
                        Step {index + 1}
                      </span>
                      {step.status === 'validating' && (
                        <span className="text-xs text-blue-400">Validating...</span>
                      )}
                    </div>
                    <p className="text-sm text-neutral-200 mt-1 font-medium">
                      {step.objective}
                    </p>
                  </div>

                  <div className="text-neutral-500">
                    {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                  </div>
                </div>

                {/* Expanded Details */}
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="px-4 pb-3 pl-10 space-y-2">
                        {/* Events Timeline */}
                        {events.length > 0 && (
                          <div className="space-y-1.5 relative border-l border-neutral-700 pl-4 py-1">
                             {events.map((event, idx) => (
                               <div key={idx} className="flex items-center gap-2 text-xs text-neutral-400">
                                  <span className={`shrink-0 ${
                                     event.status === 'success' ? 'text-green-400' :
                                     event.status === 'error' ? 'text-red-400' : 'text-blue-400'
                                  }`}>
                                    {getEventIcon(event)}
                                  </span>
                                  <span className="truncate">{event.message}</span>
                               </div>
                             ))}
                          </div>
                        )}

                        {/* Validation Result */}
                        {validation && (
                          <div className={`mt-2 text-xs p-2 rounded flex items-start gap-2 ${
                            validation.success 
                              ? 'bg-green-500/10 text-green-300' 
                              : 'bg-red-500/10 text-red-300'
                          }`}>
                            <div className="mt-0.5">
                              {validation.success ? <Check size={12} /> : <XCircle size={12} />}
                            </div>
                            <div className="flex-1">
                              <span className="font-bold">{validation.success ? 'Validated' : 'Failed'}</span>
                              <div className="opacity-90 mt-0.5">{validation.feedback}</div>
                            </div>
                          </div>
                        )}
                        
                        {step.status === 'pending' && events.length === 0 && (
                           <div className="text-xs text-neutral-600 italic">Waiting to start...</div>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
                
                {/* Connection line to next step */}
                {index < plan.length - 1 && (
                  <div className="absolute left-6 top-full h-2 w-px bg-neutral-700" />
                )}
              </motion.div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

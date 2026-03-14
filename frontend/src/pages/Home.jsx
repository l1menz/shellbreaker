import { useState } from 'react'
import { useApp } from '../context/AppContext'
import SquadCard from '../components/SquadCard'

const CATEGORIES = ['Life', 'Gym', 'Career']

const CATEGORY_ICONS = { Life: '🌱', Gym: '💪', Career: '💼' }

export default function Home() {
  const { tasks, toggleTask, squad } = useApp()
  const [activeTab, setActiveTab] = useState('Life')

  const completedCount = Object.values(tasks).flat().filter(t => t.done).length
  const totalCount = Object.values(tasks).flat().length

  return (
    <div className="px-4 pb-6 pt-2 space-y-5 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="pixel-text text-lg text-white">My Tasks</h1>
        <p className="text-white/40 text-xs mt-1.5">{completedCount}/{totalCount} completed</p>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-purple-600 to-purple-400 rounded-full transition-all duration-700"
          style={{ width: `${(completedCount / totalCount) * 100}%` }}
        />
      </div>

      {/* Category tabs */}
      <div className="flex gap-2">
        {CATEGORIES.map((cat) => {
          const done = tasks[cat].filter(t => t.done).length
          const total = tasks[cat].length
          const active = activeTab === cat
          return (
            <button
              key={cat}
              onClick={() => setActiveTab(cat)}
              className={`flex-1 py-2.5 rounded-xl text-xs font-semibold border transition-all duration-200 ${
                active
                  ? 'bg-purple-600/30 border-purple-500/60 text-purple-300 shadow-glow-sm'
                  : 'bg-white/5 border-white/10 text-white/50'
              }`}
            >
              <div>{CATEGORY_ICONS[cat]} {cat}</div>
              <div className={`text-[9px] mt-0.5 ${active ? 'text-purple-400/70' : 'text-white/30'}`}>
                {done}/{total}
              </div>
            </button>
          )
        })}
      </div>

      {/* Task list */}
      <div className="space-y-2">
        {tasks[activeTab].map((task) => (
          <button
            key={task.id}
            onClick={() => toggleTask(activeTab, task.id)}
            className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl border transition-all duration-200 active:scale-[0.98] ${
              task.done
                ? 'bg-purple-600/10 border-purple-500/30'
                : 'bg-white/5 border-white/10'
            }`}
          >
            {/* Checkbox */}
            <div className={`w-5 h-5 rounded-md border-2 flex items-center justify-center shrink-0 transition-all duration-200 ${
              task.done
                ? 'bg-purple-600 border-purple-500 shadow-glow-sm'
                : 'border-white/30'
            }`}>
              {task.done && (
                <svg className="w-3 h-3 text-white" viewBox="0 0 12 12" fill="none">
                  <path d="M2 6l3 3 5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
            </div>
            <span className={`text-sm transition-all ${task.done ? 'text-white/40 line-through' : 'text-white/90 font-medium'}`}>
              {task.text}
            </span>
          </button>
        ))}
      </div>

      {/* My Squad */}
      <div>
        <h2 className="pixel-text text-xs text-white/60 mb-4">My Squad</h2>
        <div className="flex gap-4 justify-center">
          {squad.map((member) => (
            <SquadCard key={member.id} member={member} />
          ))}
        </div>
      </div>
    </div>
  )
}

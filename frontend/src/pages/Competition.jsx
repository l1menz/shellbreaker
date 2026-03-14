import { useApp } from '../context/AppContext'
import ChallengeCard from '../components/ChallengeCard'
import Leaderboard from '../components/Leaderboard'
import { useState } from 'react'

export default function Competition() {
  const { competitions } = useApp()
  const [view, setView] = useState('battles')

  return (
    <div className="px-4 pb-6 pt-2 space-y-5 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="pixel-text text-lg text-white">My Competition</h1>
        <p className="text-white/40 text-xs mt-1.5">{competitions.length} active battles</p>
      </div>

      {/* Toggle */}
      <div className="flex bg-white/5 border border-white/10 rounded-xl p-1 gap-1">
        {['battles', 'leaderboard'].map((v) => (
          <button
            key={v}
            onClick={() => setView(v)}
            className={`flex-1 py-2 rounded-lg text-xs font-semibold capitalize transition-all duration-200 ${
              view === v
                ? 'bg-purple-600 text-white shadow-glow-sm'
                : 'text-white/40 hover:text-white/60'
            }`}
          >
            {v === 'battles' ? '⚔️ Battles' : '🏆 Leaderboard'}
          </button>
        ))}
      </div>

      {view === 'battles' ? (
        <div className="space-y-3">
          {competitions.length === 0 ? (
            <div className="flex flex-col items-center gap-3 py-12 text-center">
              <span className="text-5xl opacity-30">⚔️</span>
              <p className="text-white/30 text-sm">No active battles</p>
              <p className="text-white/20 text-xs">Go to Compete to challenge someone</p>
            </div>
          ) : (
            competitions.map((comp, i) => (
              <div key={comp.id} className="animate-slide-up" style={{ animationDelay: `${i * 0.05}s` }}>
                <div className="flex items-center gap-2 mb-1 px-1">
                  <span className="pixel-text text-[10px] text-white/30">{i + 1}</span>
                </div>
                <ChallengeCard
                  challenge={comp.challenge}
                  opponent={comp.opponent}
                  wager={comp.wager}
                  timeLeft={comp.timeLeft}
                  status={comp.status}
                />
              </div>
            ))
          )}
        </div>
      ) : (
        <Leaderboard />
      )}
    </div>
  )
}

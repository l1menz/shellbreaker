import { useEffect, useState } from 'react'
import { getLeaderboard } from '../api'

const mockLeaderboard = [
  { rank: 1, name: 'Blat', score: 320, emoji: '🦁' },
  { rank: 2, name: 'Gyat', score: 280, emoji: '🐉' },
  { rank: 3, name: 'Splat', score: 210, emoji: '🐯' },
  { rank: 4, name: 'You', score: 80, emoji: '🔥', isUser: true },
]

export default function Leaderboard() {
  const [entries, setEntries] = useState(mockLeaderboard)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    getLeaderboard()
      .then(data => {
        if (cancelled) return
        const mapped = data.map((user, index) => ({
          rank: index + 1,
          name: user.username,
          score: user.xp,
          emoji: '🔥',
          isUser: user.is_self || false,
        }))
        setEntries(mapped)
      })
      .catch(() => {
        if (cancelled) return
        // keep mock data on error
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="space-y-2">
      {loading && (
        <div className="text-xs text-white/40 px-1 pb-1">
          Loading leaderboard...
        </div>
      )}
      {entries.map((entry) => (
        <div
          key={entry.rank}
          className={`flex items-center gap-3 px-4 py-3 rounded-xl border transition-all ${
            entry.isUser
              ? 'bg-purple-600/15 border-purple-500/40 shadow-glow-sm'
              : 'bg-white/5 border-white/10'
          }`}
        >
          <span className={`pixel-text text-xs w-6 text-center ${
            entry.rank === 1 ? 'text-yellow-400' :
            entry.rank === 2 ? 'text-gray-300' :
            entry.rank === 3 ? 'text-amber-600' : 'text-white/40'
          }`}>
            {entry.rank}
          </span>
          <span className="text-xl">{entry.emoji}</span>
          <span className={`flex-1 text-sm font-semibold ${entry.isUser ? 'text-purple-300' : 'text-white/80'}`}>
            {entry.name}
          </span>
          <div className="flex items-center gap-1">
            <span className="text-yellow-400 text-xs">◆</span>
            <span className="text-white/60 text-xs font-medium">{entry.score}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

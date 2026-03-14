const mockLeaderboard = [
  { rank: 1, name: 'Blat', score: 320, emoji: '🦁' },
  { rank: 2, name: 'Gyat', score: 280, emoji: '🐉' },
  { rank: 3, name: 'Splat', score: 210, emoji: '🐯' },
  { rank: 4, name: 'You', score: 80, emoji: '🔥', isUser: true },
]

export default function Leaderboard() {
  return (
    <div className="space-y-2">
      {mockLeaderboard.map((entry) => (
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

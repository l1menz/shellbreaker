export default function ChallengeCard({ challenge, opponent, wager, timeLeft, status = 'active' }) {
  return (
    <div className="glass-card p-4 border-purple-500/20">
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="text-white font-semibold text-sm">{challenge}</p>
          <p className="text-white/40 text-xs mt-0.5">vs {opponent}</p>
        </div>
        <span className="text-xs bg-purple-600/30 text-purple-300 border border-purple-500/30 rounded-lg px-2 py-1 font-medium">
          {timeLeft} left
        </span>
      </div>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-yellow-400 text-xs">◆</span>
          <span className="text-white/70 text-xs font-medium">{wager} wagered</span>
        </div>
        <div className={`w-2 h-2 rounded-full ${status === 'active' ? 'bg-green-400 animate-pulse' : 'bg-gray-500'}`} />
      </div>
    </div>
  )
}

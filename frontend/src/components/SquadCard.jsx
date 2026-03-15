const statusColors = {
  online: 'bg-green-400',
  away: 'bg-yellow-400',
  offline: 'bg-gray-500',
}

export default function SquadCard({ member }) {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative">
        <div className="w-16 h-16 rounded-2xl bg-purple-900/50 border-2 border-purple-500/40 flex items-center justify-center text-3xl shadow-glow-sm">
          {member.emoji}
        </div>
        <span
          className={`absolute bottom-0.5 right-0.5 w-3 h-3 rounded-full border-2 border-[#0a0a0a] ${statusColors[member.status] || 'bg-gray-500'}`}
        />
      </div>
      <span className="text-white/70 text-xs font-semibold tracking-wide">{member.name}</span>
    </div>
  )
}

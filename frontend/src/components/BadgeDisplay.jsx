const badges = [
  { id: 'first_tap', label: 'First Tap', icon: '📡', desc: 'Made your first NFC connection' },
  { id: 'challenger', label: 'Challenger', icon: '⚔️', desc: 'Won your first wager' },
  { id: 'social', label: 'Social', icon: '🤝', desc: 'Met 5 people' },
  { id: 'streak', label: 'Streak', icon: '🔥', desc: 'Completed 7 tasks in a row' },
]

export default function BadgeDisplay({ earned = [] }) {
  return (
    <div className="grid grid-cols-4 gap-3">
      {badges.map((badge) => {
        const isEarned = earned.includes(badge.id)
        return (
          <div key={badge.id} className="flex flex-col items-center gap-1.5">
            <div className={`
              w-14 h-14 rounded-xl flex items-center justify-center text-2xl
              border transition-all
              ${isEarned
                ? 'bg-purple-600/20 border-purple-500/50 shadow-glow-sm'
                : 'bg-white/5 border-white/10 grayscale opacity-40'
              }
            `}>
              {badge.icon}
            </div>
            <span className={`text-[9px] text-center leading-tight ${isEarned ? 'text-purple-300' : 'text-white/30'}`}>
              {badge.label}
            </span>
          </div>
        )
      })}
    </div>
  )
}

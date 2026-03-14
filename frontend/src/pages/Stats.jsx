import { useApp } from '../context/AppContext'
import StatCard from '../components/StatCard'
import BadgeDisplay from '../components/BadgeDisplay'
import ProgressBar from '../components/ProgressBar'

const STAT_CONFIG = [
  { key: 'challengesComplete', label: 'Challenges Complete', icon: '🎯', accent: true },
  { key: 'wagersWon', label: 'Wagers Won', icon: '⚔️', accent: false },
  { key: 'peopleMet', label: 'People Met', icon: '🤝', accent: false },
  { key: 'friendsSecured', label: 'Friends Secured', icon: '🔥', accent: false },
]

export default function Stats() {
  const { stats, currency } = useApp()

  const nextLevelXp = 100
  const currentXp = (stats.challengesComplete * 15) + (stats.wagersWon * 25) + (stats.peopleMet * 5)

  return (
    <div className="px-4 pb-6 pt-2 space-y-5 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="pixel-text text-lg text-white">My Stats</h1>
        <p className="text-white/40 text-xs mt-1.5">Your shell-breaking progress</p>
      </div>

      {/* XP card */}
      <div className="glass-card p-5 border-purple-500/30 shadow-glow-sm">
        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="pixel-text text-purple-300 text-[10px]">Shell Breaker Lv.1</p>
            <p className="text-white/40 text-xs mt-1">{currentXp} / {nextLevelXp} XP</p>
          </div>
          <div className="text-4xl">🐚</div>
        </div>
        <ProgressBar value={currentXp} max={nextLevelXp} showPercent />
      </div>

      {/* Stats list */}
      <div className="space-y-2">
        {STAT_CONFIG.map((s) => (
          <StatCard
            key={s.key}
            label={s.label}
            value={stats[s.key]}
            icon={s.icon}
            accent={s.accent}
          />
        ))}
      </div>

      {/* Badges */}
      <div>
        <h2 className="pixel-text text-xs text-white/60 mb-4">Badges</h2>
        <BadgeDisplay earned={stats.challengesComplete > 0 ? ['first_tap'] : []} />
      </div>
    </div>
  )
}

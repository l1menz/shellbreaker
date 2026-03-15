import { useApp } from '../context/AppContext'
import ProgressBar from '../components/ProgressBar'

export default function Profile() {
  const { user, stats, currency, squad, logout } = useApp()

  return (
    <div className="px-4 pb-6 pt-2 space-y-5 animate-fade-in">
      {/* Profile header */}
      <div className="glass-card p-5 flex flex-col items-center gap-3 border-purple-500/20 shadow-glow-sm text-center">
        {/* Avatar */}
        <div className="relative">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-700 to-purple-950 border-2 border-purple-500/50 flex items-center justify-center text-4xl shadow-glow">
            {user.emoji}
          </div>
          <span className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-green-400 border-2 border-[#0a0a0a] flex items-center justify-center text-[10px]">
            ●
          </span>
        </div>

        <div>
          <h2 className="pixel-text text-sm text-white">{user.name}</h2>
          <p className="text-white/40 text-xs mt-1.5 max-w-[200px] leading-relaxed">{user.bio}</p>
        </div>

        {/* Currency display */}
        <div className="flex items-center gap-2 bg-purple-900/40 border border-purple-500/30 rounded-xl px-4 py-2">
          <span className="text-yellow-400">◆</span>
          <span className="pixel-text text-purple-300 text-xs">{currency}</span>
          <span className="text-white/30 text-xs">credits</span>
        </div>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 gap-3">
        {[
          { label: 'Challenges', value: stats.challengesComplete, icon: '🎯' },
          { label: 'Wagers Won', value: stats.wagersWon, icon: '⚔️' },
          { label: 'People Met', value: stats.peopleMet, icon: '🤝' },
          { label: 'Friends', value: stats.friendsSecured, icon: '🔥' },
        ].map((s) => (
          <div key={s.label} className="glass-card p-4 flex flex-col items-center gap-1.5 text-center">
            <span className="text-2xl">{s.icon}</span>
            <span className="pixel-text text-white text-sm">{s.value}</span>
            <span className="text-white/40 text-[10px]">{s.label}</span>
          </div>
        ))}
      </div>

      <button
        onClick={logout}
        className="btn-ghost w-full text-red-400/80 hover:text-red-400 text-sm py-2"
      >
        Sign out
      </button>

      {/* Social links placeholder */}
      <div className="glass-card p-4">
        <h3 className="text-white/60 text-xs font-semibold uppercase tracking-wider mb-3">Social Links</h3>
        <div className="space-y-2">
          {[
            { icon: '📸', label: 'Instagram', handle: '@your_handle' },
            { icon: '🐦', label: 'Twitter', handle: '@your_handle' },
          ].map((link) => (
            <div key={link.label} className="flex items-center gap-3 py-2">
              <span className="text-xl">{link.icon}</span>
              <div>
                <p className="text-white/70 text-xs font-medium">{link.label}</p>
                <p className="text-purple-400/60 text-xs">{link.handle}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Squad */}
      <div className="glass-card p-4">
        <h3 className="text-white/60 text-xs font-semibold uppercase tracking-wider mb-4">My Squad</h3>
        <div className="flex gap-4">
          {squad.map((m) => (
            <div key={m.id} className="flex flex-col items-center gap-2">
              <div className="w-12 h-12 rounded-xl bg-purple-900/50 border border-purple-500/30 flex items-center justify-center text-2xl">
                {m.emoji}
              </div>
              <span className="text-white/50 text-[10px]">{m.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

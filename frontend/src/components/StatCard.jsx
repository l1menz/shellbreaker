export default function StatCard({ label, value, icon, accent = false }) {
  return (
    <div className={`
      flex items-center justify-between px-4 py-3.5
      rounded-xl border transition-all duration-200
      ${accent
        ? 'bg-purple-600/10 border-purple-500/40 shadow-glow-sm'
        : 'bg-white/5 border-white/10'
      }
    `}>
      <div className="flex items-center gap-3">
        {icon && <span className="text-xl">{icon}</span>}
        <span className="text-white/60 text-sm font-medium">{label}</span>
      </div>
      <span className={`pixel-text text-sm ${accent ? 'text-purple-300' : 'text-white'}`}>
        {value}
      </span>
    </div>
  )
}

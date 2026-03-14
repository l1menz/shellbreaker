export default function ProgressBar({ value = 0, max = 100, label, showPercent = false }) {
  const pct = Math.min(100, Math.round((value / max) * 100))

  return (
    <div className="w-full">
      {(label || showPercent) && (
        <div className="flex justify-between mb-1.5">
          {label && <span className="text-white/50 text-xs">{label}</span>}
          {showPercent && <span className="text-purple-400 text-xs font-semibold">{pct}%</span>}
        </div>
      )}
      <div className="h-2 bg-white/10 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-purple-600 to-purple-400 rounded-full transition-all duration-500 shadow-glow-sm"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

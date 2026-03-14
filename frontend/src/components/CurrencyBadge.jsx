export default function CurrencyBadge({ amount }) {
  return (
    <div className="flex items-center gap-1.5 bg-purple-950/60 border border-purple-500/30 rounded-lg px-3 py-1.5 shadow-glow-sm">
      <span className="text-yellow-400 text-sm">◆</span>
      <span className="pixel-text text-purple-300 text-[10px]">{amount}</span>
    </div>
  )
}

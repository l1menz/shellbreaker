export default function PixelCard({ children, className = '', glow = false, onClick }) {
  return (
    <div
      onClick={onClick}
      className={`
        glass-card p-4
        ${glow ? 'shadow-glow border-purple-500/40' : ''}
        ${onClick ? 'cursor-pointer active:scale-[0.98] transition-transform duration-100' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  )
}

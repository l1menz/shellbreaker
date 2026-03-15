import { useNavigate } from 'react-router-dom'

export default function Onboarding() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col items-center justify-between h-full px-8 py-16 bg-[#0a0a0a] animate-fade-in">
      {/* Top decorative dots */}
      <div className="flex gap-2">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="w-1.5 h-1.5 rounded-full bg-purple-500/40"
            style={{ animationDelay: `${i * 0.1}s` }}
          />
        ))}
      </div>

      {/* Center content */}
      <div className="flex flex-col items-center gap-8 text-center">
        {/* Logo */}
        <div className="relative">
          <div className="w-28 h-28 rounded-3xl bg-gradient-to-br from-purple-700 to-purple-950 border-2 border-purple-500/50 flex items-center justify-center animate-float shadow-glow-lg">
            <span className="text-5xl">🐚</span>
          </div>
          {/* Glow rings */}
          <div className="absolute inset-0 rounded-3xl animate-ping-slow opacity-20 border-2 border-purple-400 scale-110" />
          <div className="absolute inset-0 rounded-3xl animate-ping-slow opacity-10 border border-purple-400 scale-125" style={{ animationDelay: '0.5s' }} />
        </div>

        {/* App name */}
        <div className="space-y-3">
          <h1 className="pixel-text text-2xl text-white tracking-wider" style={{ lineHeight: 1.6 }}>
            Shell<span className="text-purple-400 text-glow">Breaker</span>
          </h1>
          <p className="text-white/50 text-sm leading-relaxed max-w-xs">
            Break out of your shell. Tap. Challenge. Compete.
          </p>
        </div>

        {/* Feature pills */}
        <div className="flex flex-wrap gap-2 justify-center">
          {['📡 NFC Tap', '⚔️ Wager', '🔥 Streaks', '👥 Squad'].map((f) => (
            <span key={f} className="text-xs text-purple-300/70 bg-purple-900/30 border border-purple-500/20 rounded-full px-3 py-1">
              {f}
            </span>
          ))}
        </div>
      </div>

      {/* Bottom CTAs */}
      <div className="w-full space-y-3">
        <button
          onClick={() => navigate('/register')}
          className="btn-primary w-full text-sm py-4 animate-glow-pulse"
        >
          Get Started
        </button>
        <button
          onClick={() => navigate('/login')}
          className="btn-ghost w-full text-sm py-3"
        >
          I already have an account
        </button>
        <p className="text-center text-white/20 text-xs mt-2">
          By continuing you accept the rules
        </p>
      </div>
    </div>
  )
}

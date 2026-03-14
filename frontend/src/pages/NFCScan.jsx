import { useNavigate, useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { useApp } from '../context/AppContext'

export default function NFCScan() {
  const navigate = useNavigate()
  const location = useLocation()
  const { addCompetition } = useApp()
  const [phase, setPhase] = useState('scanning') // scanning | found | success

  const config = location.state || { wager: 100, timeLimit: '2 weeks', challenge: 'Run 5km' }

  // Simulate NFC scan success after 3 seconds (for demo)
  useEffect(() => {
    const t1 = setTimeout(() => setPhase('found'), 3000)
    return () => clearTimeout(t1)
  }, [])

  const handleAccept = () => {
    addCompetition({
      opponent: 'New Friend',
      challenge: config.challenge,
      wager: config.wager,
      timeLeft: config.timeLimit,
      status: 'active',
    })
    setPhase('success')
    setTimeout(() => navigate('/competition'), 1500)
  }

  return (
    <div className="flex flex-col items-center justify-between h-full px-8 py-12 bg-[#0a0a0a]">
      {/* Top */}
      <div className="w-full flex justify-between items-center">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-white/40 hover:text-white/70 transition-colors text-sm"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Cancel
        </button>
        <div className="flex items-center gap-1.5 bg-purple-950/60 border border-purple-500/30 rounded-lg px-3 py-1.5">
          <span className="text-yellow-400 text-xs">◆</span>
          <span className="pixel-text text-purple-300 text-[10px]">{config.wager}</span>
        </div>
      </div>

      {/* Center animation */}
      <div className="flex flex-col items-center gap-8">
        {phase === 'scanning' && (
          <>
            <div className="relative flex items-center justify-center">
              {[...Array(4)].map((_, i) => (
                <div
                  key={i}
                  className="absolute rounded-full border border-purple-500/30 animate-ping-slow"
                  style={{
                    width: `${(i + 2) * 50}px`,
                    height: `${(i + 2) * 50}px`,
                    animationDelay: `${i * 0.4}s`,
                    opacity: 1 - i * 0.2,
                  }}
                />
              ))}
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-700 to-purple-900 border-2 border-purple-400/50 flex items-center justify-center shadow-glow-lg animate-pulse-slow">
                <span className="text-4xl">📡</span>
              </div>
            </div>
            <div className="text-center space-y-2">
              <p className="pixel-text text-sm text-white" style={{ lineHeight: 1.8 }}>Scanning...</p>
              <p className="text-white/40 text-sm">Hold your phone close to<br />your friend's device</p>
            </div>
          </>
        )}

        {phase === 'found' && (
          <div className="flex flex-col items-center gap-6 animate-slide-up">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-green-700 to-green-900 border-2 border-green-400/50 flex items-center justify-center shadow-[0_0_30px_rgba(74,222,128,0.4)] animate-bounce">
              <span className="text-4xl">🤝</span>
            </div>
            <div className="text-center space-y-1.5">
              <p className="pixel-text text-sm text-white" style={{ lineHeight: 1.8 }}>Friend Found!</p>
              <p className="text-white/50 text-sm">Ready to accept the challenge?</p>
            </div>
            {/* Challenge summary */}
            <div className="glass-card p-4 w-full border-purple-500/30 space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-white/40">Challenge</span>
                <span className="text-white font-medium">{config.challenge}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-white/40">Wager</span>
                <span className="text-yellow-400 font-medium">◆ {config.wager}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-white/40">Time limit</span>
                <span className="text-white font-medium">{config.timeLimit}</span>
              </div>
            </div>
            <button onClick={handleAccept} className="btn-primary w-full">
              Accept Challenge
            </button>
          </div>
        )}

        {phase === 'success' && (
          <div className="flex flex-col items-center gap-4 animate-slide-up">
            <div className="w-24 h-24 rounded-full bg-purple-600/20 border-2 border-purple-400 flex items-center justify-center shadow-glow-lg">
              <span className="text-5xl">⚔️</span>
            </div>
            <p className="pixel-text text-sm text-purple-300 text-center" style={{ lineHeight: 1.8 }}>
              Battle Started!
            </p>
          </div>
        )}
      </div>

      {/* Bottom instruction */}
      {phase === 'scanning' && (
        <p className="text-white/20 text-xs text-center">
          NFC scanning active · Keep screen on
        </p>
      )}
      {phase !== 'scanning' && <div />}
    </div>
  )
}

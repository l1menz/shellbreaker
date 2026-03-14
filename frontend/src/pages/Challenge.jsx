import { useNavigate } from 'react-router-dom'

export default function Challenge() {
  const navigate = useNavigate()

  return (
    <div className="px-4 pb-6 pt-2 animate-fade-in">
      <div className="mb-6">
        <h1 className="pixel-text text-lg text-white">Daily Challenge</h1>
        <p className="text-white/40 text-xs mt-1.5">Today's shell-breaking mission</p>
      </div>

      <div className="glass-card p-6 border-purple-500/30 shadow-glow text-center space-y-4">
        <span className="text-5xl">🎯</span>
        <div>
          <h2 className="text-white font-bold text-lg">Talk to a stranger</h2>
          <p className="text-white/40 text-sm mt-2 leading-relaxed">
            Start a conversation with someone you've never met. Ask them their name and one interesting fact about them.
          </p>
        </div>
        <div className="flex items-center justify-center gap-2 text-yellow-400">
          <span>◆</span>
          <span className="font-bold text-white">+50 XP</span>
          <span className="text-white/30 text-xs">reward</span>
        </div>
        <button
          onClick={() => navigate('/compete')}
          className="btn-primary w-full"
        >
          Accept Challenge
        </button>
      </div>
    </div>
  )
}

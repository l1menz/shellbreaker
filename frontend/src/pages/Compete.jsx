import { useState, useMemo, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'

const TIME_LIMITS = ['1 day', '3 days', '1 week', '2 weeks', '1 month']

export default function Compete() {
  const navigate = useNavigate()
  const { addCompetition, currency, challenges } = useApp()
  const challengeOptions = useMemo(() => challenges.map((c) => ({ id: c.id, title: c.title })), [challenges])
  const [wager, setWager] = useState(200)
  const [timeLimit, setTimeLimit] = useState('2 weeks')
  const [challenge, setChallenge] = useState('')
  const [tapping, setTapping] = useState(false)
  useEffect(() => {
    if (challengeOptions.length && !challenge) setChallenge(challengeOptions[0].title)
  }, [challengeOptions, challenge])

  const handleTap = () => {
    if (wager > currency) return
    setTapping(true)
    setTimeout(() => {
      navigate('/scan', { state: { wager, timeLimit, challenge: challenge || challengeOptions[0]?.title } })
    }, 600)
  }

  return (
    <div className="px-4 pb-6 pt-2 space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="pixel-text text-lg text-white">Compete</h1>
        <p className="text-white/40 text-xs mt-1.5">Challenge a friend via NFC</p>
      </div>

      {/* NFC tap button */}
      <div className="flex flex-col items-center gap-4 py-4">
        <div className="relative flex items-center justify-center">
          {/* Outer ping rings */}
          {tapping && (
            <>
              <div className="absolute w-48 h-48 rounded-full border border-purple-400/30 animate-ping" />
              <div className="absolute w-40 h-40 rounded-full border border-purple-400/40 animate-ping" style={{ animationDelay: '0.3s' }} />
            </>
          )}
          {!tapping && (
            <>
              <div className="absolute w-40 h-40 rounded-full border border-purple-500/20 animate-pulse-slow" />
              <div className="absolute w-32 h-32 rounded-full border border-purple-500/15 animate-pulse-slow" style={{ animationDelay: '0.5s' }} />
            </>
          )}

          {/* Main button */}
          <button
            onClick={handleTap}
            className={`relative w-28 h-28 rounded-full flex flex-col items-center justify-center gap-2 transition-all duration-300 active:scale-95 ${
              tapping
                ? 'bg-purple-600 shadow-glow-lg scale-105'
                : 'bg-gradient-to-br from-purple-700 to-purple-900 shadow-glow border-2 border-purple-400/40'
            }`}
          >
            <svg className="w-10 h-10 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 8.25H7.5a2.25 2.25 0 00-2.25 2.25v9a2.25 2.25 0 002.25 2.25h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25H15M9 12l3 3m0 0l3-3m-3 3V2.25" />
            </svg>
          </button>
        </div>

        <div className="text-center">
          <p className="text-white/70 text-sm font-medium">Tap to share challenge</p>
          <p className="text-white/30 text-xs mt-1">Hold your phone to your friend's</p>
        </div>
      </div>

      {/* Config form */}
      <div className="space-y-3">
        {/* Wager */}
        <div className="glass-card p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="text-white/60 text-xs font-semibold uppercase tracking-wider">Wager amount</label>
            <div className="flex items-center gap-1">
              <span className="text-yellow-400 text-xs">◆</span>
              <span className="text-white font-bold text-sm">{wager}</span>
            </div>
          </div>
          <input
            type="range"
            min={10}
            max={Math.min(500, currency)}
            step={10}
            value={wager}
            onChange={(e) => setWager(Number(e.target.value))}
            className="w-full accent-purple-500"
          />
          <div className="flex justify-between text-white/30 text-[10px] mt-1">
            <span>10</span>
            <span className="text-purple-400/60">Your balance: ◆{currency}</span>
            <span>{Math.min(500, currency)}</span>
          </div>
        </div>

        {/* Time limit */}
        <div className="glass-card p-4">
          <label className="text-white/60 text-xs font-semibold uppercase tracking-wider block mb-3">
            Time limit
          </label>
          <div className="flex flex-wrap gap-2">
            {TIME_LIMITS.map((t) => (
              <button
                key={t}
                onClick={() => setTimeLimit(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                  timeLimit === t
                    ? 'bg-purple-600/30 border-purple-500/60 text-purple-300'
                    : 'bg-white/5 border-white/10 text-white/50'
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Challenge */}
        <div className="glass-card p-4">
          <label className="text-white/60 text-xs font-semibold uppercase tracking-wider block mb-3">
            Challenge
          </label>
          <select
            value={challenge}
            onChange={(e) => setChallenge(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2.5 text-white text-sm outline-none focus:border-purple-500/50 transition-colors"
            style={{ colorScheme: 'dark' }}
          >
            {challengeOptions.map((c) => (
              <option key={c.id} value={c.title} className="bg-[#111]">{c.title}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Confirm button */}
      <button
        onClick={handleTap}
        disabled={wager > currency}
        className="btn-primary w-full disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {wager > currency ? 'Insufficient balance' : 'Tap & Challenge'}
      </button>
    </div>
  )
}

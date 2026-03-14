import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

export default function Login() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  return (
    <div className="flex flex-col justify-center h-full px-8 py-12 bg-[#0a0a0a] animate-fade-in">
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-3">
          <div className="w-16 h-16 rounded-2xl bg-purple-700/30 border border-purple-500/40 flex items-center justify-center text-3xl mx-auto shadow-glow-sm">
            🐚
          </div>
          <h1 className="pixel-text text-lg text-white" style={{ lineHeight: 1.7 }}>Welcome Back</h1>
          <p className="text-white/40 text-sm">Sign in to continue</p>
        </div>

        {/* Form */}
        <div className="space-y-3">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full bg-white/5 border border-white/10 focus:border-purple-500/60 rounded-xl px-4 py-3.5 text-white text-sm outline-none transition-colors placeholder:text-white/20"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-white/5 border border-white/10 focus:border-purple-500/60 rounded-xl px-4 py-3.5 text-white text-sm outline-none transition-colors placeholder:text-white/20"
          />
        </div>

        <div className="space-y-3">
          <button
            onClick={() => navigate('/home')}
            className="btn-primary w-full"
          >
            Sign In
          </button>
          <button
            onClick={() => navigate('/')}
            className="btn-ghost w-full"
          >
            Back
          </button>
        </div>
      </div>
    </div>
  )
}

import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useApp } from '../context/AppContext'

export default function Register() {
  const navigate = useNavigate()
  const { registerUser, loading } = useApp()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!username.trim() || !email.trim() || !password) {
      setError('Username, email and password required')
      return
    }
    try {
      await registerUser({ username: username.trim(), email: email.trim(), password })
      navigate('/home', { replace: true })
    } catch (err) {
      try {
        const parsed = JSON.parse(err.message)
        setError(Array.isArray(parsed.detail) ? parsed.detail[0]?.msg : parsed.detail || err.message)
      } catch {
        setError(err.message || 'Registration failed')
      }
    }
  }

  return (
    <div className="flex flex-col justify-center h-full px-8 py-12 bg-[#0a0a0a] animate-fade-in">
      <div className="space-y-8">
        <div className="text-center space-y-3">
          <div className="w-16 h-16 rounded-2xl bg-purple-700/30 border border-purple-500/40 flex items-center justify-center text-3xl mx-auto shadow-glow-sm">
            🐚
          </div>
          <h1 className="pixel-text text-lg text-white" style={{ lineHeight: 1.7 }}>Create account</h1>
          <p className="text-white/40 text-sm">Join ShellBreaker</p>
        </div>

        {error && (
          <div className="text-red-400 text-sm text-center bg-red-900/20 border border-red-500/30 rounded-xl px-4 py-2">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full bg-white/5 border border-white/10 focus:border-purple-500/60 rounded-xl px-4 py-3.5 text-white text-sm outline-none transition-colors placeholder:text-white/20"
            autoComplete="username"
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-white/5 border border-white/10 focus:border-purple-500/60 rounded-xl px-4 py-3.5 text-white text-sm outline-none transition-colors placeholder:text-white/20"
            autoComplete="email"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-white/5 border border-white/10 focus:border-purple-500/60 rounded-xl px-4 py-3.5 text-white text-sm outline-none transition-colors placeholder:text-white/20"
            autoComplete="new-password"
          />
          <div className="space-y-3">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full disabled:opacity-50"
            >
              {loading ? 'Creating account...' : 'Sign Up'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/login')}
              className="btn-ghost w-full"
            >
              I already have an account
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

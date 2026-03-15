import { useNavigate, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { useApp } from '../context/AppContext'

export default function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login, authError, loading } = useApp()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!username.trim() || !password) {
      setError('Username and password required')
      return
    }
    try {
      await login(username.trim(), password)
      const from = location.state?.from
      const redirectTo = from ? `${from.pathname}${from.search || ''}` : '/home'
      navigate(redirectTo, { replace: true })
    } catch (err) {
      try {
        const parsed = JSON.parse(err.message)
        setError(parsed.detail || err.message)
      } catch {
        setError(err.message || 'Login failed')
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
          <h1 className="pixel-text text-lg text-white" style={{ lineHeight: 1.7 }}>Welcome Back</h1>
          <p className="text-white/40 text-sm">Sign in to continue</p>
          <p className="text-white/30 text-xs mt-1">Demo: demo / demo123</p>
        </div>

        {(error || authError) && (
          <div className="text-red-400 text-sm text-center bg-red-900/20 border border-red-500/30 rounded-xl px-4 py-2">
            {error || authError}
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
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-white/5 border border-white/10 focus:border-purple-500/60 rounded-xl px-4 py-3.5 text-white text-sm outline-none transition-colors placeholder:text-white/20"
            autoComplete="current-password"
          />
          <div className="space-y-3">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/', { state: location.state })}
              className="btn-ghost w-full"
            >
              Back
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

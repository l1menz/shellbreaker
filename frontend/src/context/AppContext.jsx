import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import * as api from '../api'

const AppContext = createContext(null)

// Map backend category to frontend tab names
const CATEGORY_MAP = {
  activity: 'Gym',
  dare: 'Life',
  conversation: 'Career',
  greeting: 'Life',
}

function mapTodayToTasks(todayList = []) {
  const Life = []
  const Gym = []
  const Career = []
  for (const uc of todayList) {
    const category = (uc.challenge?.category && CATEGORY_MAP[uc.challenge.category]) || 'Life'
    const item = {
      id: uc.id,
      text: uc.challenge?.title || 'Challenge',
      done: uc.status === 'completed',
      userChallengeId: uc.id,
    }
    if (category === 'Life') Life.push(item)
    else if (category === 'Gym') Gym.push(item)
    else Career.push(item)
  }
  return { Life, Gym, Career }
}

const initialCompetitions = [
  { id: 1, opponent: 'Blat', challenge: 'Run 5km', wager: 200, timeLeft: '12d', status: 'active' },
  { id: 2, opponent: 'Splat', challenge: 'Read a book', wager: 50, timeLeft: '5d', status: 'active' },
  { id: 3, opponent: 'Gyat', challenge: '100 pushups', wager: 100, timeLeft: '2d', status: 'active' },
]

const initialSquad = [
  { id: 1, name: 'Gyat', emoji: '🐉', status: 'online' },
  { id: 2, name: 'Blat', emoji: '🦁', status: 'away' },
  { id: 3, name: 'Splat', emoji: '🐯', status: 'offline' },
]

export function AppProvider({ children }) {
  const [token, setTokenState] = useState(() => api.getToken())
  const [user, setUser] = useState(null)
  const [challenges, setChallenges] = useState([])
  const [todayChallenges, setTodayChallenges] = useState([])
  const [competitions, setCompetitions] = useState(initialCompetitions)
  const [squad] = useState(initialSquad)
  const [loading, setLoading] = useState(true)
  const [authError, setAuthError] = useState(null)

  const setToken = useCallback((newToken) => {
    api.setToken(newToken)
    setTokenState(newToken)
  }, [])

  const refreshUser = useCallback(async () => {
    if (!api.getToken()) return
    try {
      const me = await api.getMe()
      setUser(me)
    } catch {
      setToken(null)
      setUser(null)
    }
  }, [setToken])

  const refreshToday = useCallback(async () => {
    if (!api.getToken()) return
    try {
      const list = await api.getTodayChallenges()
      setTodayChallenges(list)
    } catch {
      setTodayChallenges([])
    }
  }, [])

  const refreshChallenges = useCallback(async () => {
    try {
      const list = await api.getChallenges()
      setChallenges(list)
    } catch {
      setChallenges([])
    }
  }, [])

  const refreshAll = useCallback(async () => {
    setLoading(true)
    setAuthError(null)
    try {
      if (api.getToken()) {
        await Promise.all([refreshUser(), refreshToday(), refreshChallenges()])
      } else {
        setUser(null)
        setTodayChallenges([])
        await refreshChallenges()
      }
    } catch (e) {
      setAuthError(e.message)
      if (e.message?.includes('401') || e.message?.toLowerCase().includes('credentials')) {
        setToken(null)
        setUser(null)
      }
    } finally {
      setLoading(false)
    }
  }, [refreshUser, refreshToday, refreshChallenges, setToken])

  useEffect(() => {
    refreshAll()
  }, [token, refreshAll])

  const login = useCallback(async (username, password) => {
    const data = await api.login(username, password)
    setToken(data.access_token)
    await refreshUser()
  }, [setToken, refreshUser])

  const registerUser = useCallback(async ({ username, email, password }) => {
    await api.register({ username, email, password })
    await login(username, password)
  }, [login])

  const logout = useCallback(() => {
    setToken(null)
    setUser(null)
    setTodayChallenges([])
  }, [setToken])

  const toggleTask = useCallback(async (category, taskIdOrUserChallengeId) => {
    const uc = todayChallenges.find((c) => c.id === taskIdOrUserChallengeId)
    if (!uc || uc.status === 'completed') return
    try {
      await api.completeChallenge(uc.id)
      await refreshToday()
      await refreshUser()
    } catch (e) {
      console.error('Complete challenge failed', e)
    }
  }, [todayChallenges, refreshToday, refreshUser])

  const addCompetition = useCallback((comp) => {
    setCompetitions((prev) => [...prev, { ...comp, id: Date.now() }])
    if (user?.coins != null) setUser((u) => ({ ...u, coins: (u.coins ?? 0) - (comp.wager || 0) }))
  }, [user])

  const tasks = mapTodayToTasks(todayChallenges)
  const currency = user?.coins ?? 0
  const stats = {
    challengesComplete: user?.xp ? Math.floor(user.xp / 10) : 0,
    wagersWon: 0,
    peopleMet: 0,
    friendsSecured: squad.length,
  }

  const userDisplay = user
    ? {
        name: user.display_name || user.username,
        emoji: '🔥',
        bio: `Level ${user.level} · ${user.xp} XP`,
      }
    : { name: 'You', emoji: '🔥', bio: 'Sign in to track progress.' }

  return (
    <AppContext.Provider
      value={{
        token,
        user,
        loading,
        authError,
        login,
        registerUser,
        logout,
        refreshAll,
        setToken,
        currency,
        tasks,
        toggleTask,
        challenges,
        competitions,
        addCompetition,
        stats,
        squad,
        user: userDisplay,
        todayChallenges,
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}

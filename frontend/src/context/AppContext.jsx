import { createContext, useContext, useState } from 'react'

const AppContext = createContext(null)

const initialTasks = {
  Life: [
    { id: 1, text: 'Touch grass', done: false },
    { id: 2, text: 'Call mum', done: false },
    { id: 3, text: 'Read a book', done: true },
    { id: 4, text: 'Cook dinner', done: false },
  ],
  Gym: [
    { id: 5, text: 'Hit a PR', done: false },
    { id: 6, text: '100 pushups', done: true },
    { id: 7, text: 'Run 5km', done: false },
  ],
  Career: [
    { id: 8, text: 'Apply 5 jobs', done: false },
    { id: 9, text: 'Update CV', done: false },
  ],
}

const initialCompetitions = [
  { id: 1, opponent: 'Blat', challenge: 'Run 5km', wager: 200, timeLeft: '12d', status: 'active' },
  { id: 2, opponent: 'Splat', challenge: 'Read a book', wager: 50, timeLeft: '5d', status: 'active' },
  { id: 3, opponent: 'Gyat', challenge: '100 pushups', wager: 100, timeLeft: '2d', status: 'active' },
]

export function AppProvider({ children }) {
  const [currency, setCurrency] = useState(80)
  const [tasks, setTasks] = useState(initialTasks)
  const [competitions, setCompetitions] = useState(initialCompetitions)
  const [stats] = useState({
    challengesComplete: 3,
    wagersWon: 1,
    peopleMet: 7,
    friendsSecured: 3,
  })
  const [squad] = useState([
    { id: 1, name: 'Gyat', emoji: '🐉', status: 'online' },
    { id: 2, name: 'Blat', emoji: '🦁', status: 'away' },
    { id: 3, name: 'Splat', emoji: '🐯', status: 'offline' },
  ])
  const [user] = useState({
    name: 'You',
    emoji: '🔥',
    bio: 'Breaking shells one tap at a time.',
  })

  const toggleTask = (category, taskId) => {
    setTasks(prev => ({
      ...prev,
      [category]: prev[category].map(t =>
        t.id === taskId ? { ...t, done: !t.done } : t
      ),
    }))
  }

  const addCompetition = (comp) => {
    setCompetitions(prev => [...prev, { ...comp, id: Date.now() }])
    setCurrency(prev => prev - comp.wager)
  }

  return (
    <AppContext.Provider value={{
      currency, setCurrency,
      tasks, toggleTask,
      competitions, addCompetition,
      stats,
      squad,
      user,
    }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}

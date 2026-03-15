import { Navigate, useLocation } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function ProtectedRoute({ children }) {
  const { token, loading } = useApp()
  const location = useLocation()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-white/50 text-sm">
        Loading...
      </div>
    )
  }

  if (!token) {
    return <Navigate to="/" state={{ from: location }} replace />
  }

  return children
}

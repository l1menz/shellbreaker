import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import MobileLayout from './layouts/MobileLayout'
import ProtectedRoute from './components/ProtectedRoute'
import Onboarding from './pages/Onboarding'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import Compete from './pages/Compete'
import Competition from './pages/Competition'
import Stats from './pages/Stats'
import Profile from './pages/Profile'
import NFCScan from './pages/NFCScan'

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <div className="flex items-center justify-center min-h-screen bg-black">
          <div
            className="relative w-full bg-[#0a0a0a] overflow-hidden"
            style={{ maxWidth: 430, height: '100dvh' }}
          >
            <Routes>
              <Route path="/" element={<Onboarding />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route
                element={
                  <ProtectedRoute>
                    <MobileLayout />
                  </ProtectedRoute>
                }
              >
                <Route path="/home" element={<Home />} />
                <Route path="/scan" element={<NFCScan />} />
                {/* Short NFC URLs for small tags: /f, /s, /c, /k */}
                <Route path="/f" element={<NFCScan />} />
                <Route path="/s" element={<NFCScan />} />
                <Route path="/c" element={<NFCScan />} />
                <Route path="/k" element={<NFCScan />} />
                <Route path="/compete" element={<Compete />} />
                <Route path="/competition" element={<Competition />} />
                <Route path="/stats" element={<Stats />} />
                <Route path="/profile" element={<Profile />} />
              </Route>
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </AppProvider>
  )
}

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import MobileLayout from './layouts/MobileLayout'
import Onboarding from './pages/Onboarding'
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
          {/* Mobile frame */}
          <div
            className="relative w-full bg-[#0a0a0a] overflow-hidden"
            style={{ maxWidth: 430, height: '100dvh' }}
          >
            <Routes>
              <Route path="/" element={<Onboarding />} />
              <Route path="/scan" element={<NFCScan />} />
              <Route element={<MobileLayout />}>
                <Route path="/home" element={<Home />} />
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

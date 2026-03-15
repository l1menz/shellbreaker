import { Outlet } from 'react-router-dom'
import NavBar from '../components/NavBar'
import CurrencyBadge from '../components/CurrencyBadge'
import { useApp } from '../context/AppContext'

export default function MobileLayout() {
  const { currency } = useApp()

  return (
    <div className="flex flex-col h-full">
      {/* Top currency bar */}
      <div className="flex justify-end px-4 pt-3 pb-1 shrink-0">
        <CurrencyBadge amount={currency} />
      </div>

      {/* Page content */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden no-scrollbar">
        <Outlet />
      </div>

      {/* Bottom nav */}
      <NavBar />
    </div>
  )
}

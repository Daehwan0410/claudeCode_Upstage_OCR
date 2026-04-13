import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: '대시보드' },
  { to: '/upload', label: '영수증 업로드' },
  { to: '/receipts', label: '지출 내역' },
  { to: '/stats', label: '통계 분석' },
]

export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <span className="font-bold text-lg text-indigo-600">영수증 지출 관리</span>
      <ul className="flex gap-6">
        {links.map(({ to, label }) => (
          <li key={to}>
            <NavLink
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors ${
                  isActive ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-900'
                }`
              }
            >
              {label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}

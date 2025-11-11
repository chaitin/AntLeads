import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { LayoutDashboard, Users, CheckSquare, TrendingUp } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import LeadsPage from './pages/LeadsPage'
import TasksPage from './pages/TasksPage'
import FunnelPage from './pages/FunnelPage'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm border-b border-gray-200">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center gap-2">
                <TrendingUp className="text-blue-600" size={28} />
                <h1 className="text-xl font-bold text-gray-900">AntLeads</h1>
              </div>
              <div className="flex gap-6">
                <NavLink to="/" icon={<LayoutDashboard size={18} />}>
                  Dashboard
                </NavLink>
                <NavLink to="/leads" icon={<Users size={18} />}>
                  Leads
                </NavLink>
                <NavLink to="/tasks" icon={<CheckSquare size={18} />}>
                  Tasks
                </NavLink>
                <NavLink to="/funnel" icon={<TrendingUp size={18} />}>
                  Funnel
                </NavLink>
              </div>
            </div>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/leads" element={<LeadsPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/funnel" element={<FunnelPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function NavLink({
  to,
  icon,
  children,
}: {
  to: string
  icon: React.ReactNode
  children: React.ReactNode
}) {
  return (
    <Link
      to={to}
      className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
    >
      {icon}
      {children}
    </Link>
  )
}

export default App

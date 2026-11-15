
import './App.css'
import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  useLocation,
  Navigate,
  Outlet
} from 'react-router-dom'

import Overview from './pages/Overview'
import Documents from './pages/Documents'
import Chatbot from './pages/Chatbot'
import Analytics from './pages/Analytics'
import Login from './pages/Login'
import Register from './pages/Register'

// Protect dashboard routes
function ProtectedRoute() {
  const token = localStorage.getItem('access_token')

  return token ? <Outlet /> : <Navigate to="/login" replace />
}

// Dashboard layout
function DashboardLayout() {
  const location = useLocation()

  const pageName =
    location.pathname === '/documents' ? 'Documents' :
    location.pathname === '/chatbot' ? 'Chatbot' :
    location.pathname === '/analytics' ? 'Analytics' :
    'Overview'

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">O</div>
          <span>OrgBot</span>
        </div>

        <div className="workspace">
          <span className="workspace-label">WORKSPACE</span>
          <div className="organisation">
            <div className="org-avatar">A</div>
            <div>
              <strong>Acme Organisation</strong>
              <small>Free Plan</small>
            </div>
            <span className="arrow">⌄</span>
          </div>
        </div>

        <nav className="navigation">
          <span className="nav-label">MENU</span>

          <NavLink to="/" end className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            ▦ <span>Overview</span>
          </NavLink>

          <NavLink to="/documents" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            ▤ <span>Documents</span>
          </NavLink>

          <NavLink to="/chatbot" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            ✧ <span>Chatbot</span>
          </NavLink>

          <NavLink to="/analytics" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            ▥ <span>Analytics</span>
          </NavLink>

          <span className="nav-label settings-label">PREFERENCES</span>
          <a className="nav-item" href="#settings">⚙ <span>Settings</span></a>
          <a className="nav-item" href="#help">ⓘ <span>Help & Support</span></a>
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon">✦</div>
            <strong>Upgrade your plan</strong>
            <p>Unlock more documents and AI conversations.</p>
            <button>Explore plans →</button>
          </div>

          <div className="profile">
            <div className="profile-avatar">V</div>
            <div>
              <strong>Vidhi Mittal</strong>
              <small>Administrator</small>
            </div>
            <span className="arrow">⋯</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> {pageName}
          </div>

          <div className="topbar-right">
            <button className="icon-button" aria-label="Notifications">♧</button>
            <div className="top-profile">V</div>
          </div>
        </header>

        <Outlet />
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>
            <Route path="/" element={<Overview />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/analytics" element={<Analytics />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

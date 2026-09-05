import { useEffect, useState, type ReactNode } from 'react'
import { Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import { useAuth, UserButton, SignInButton } from '@clerk/react'
import { LayoutDashboard, UserRound, Compass, Map, BookOpen, TrendingUp, Building2, LogOut, Sparkles, PanelLeftClose, PanelLeftOpen } from 'lucide-react'
import { api, configureAuth } from './services/api'
import type { StudentProfile } from './types'
import Landing from './pages/Landing'
import Onboarding from './pages/Onboarding'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Careers from './pages/Careers'
import CareerDetails from './pages/CareerDetails'
import Roadmap from './pages/Roadmap'
import Resources from './pages/Resources'
import Progress from './pages/Progress'
import CollegeExplorer from './pages/CollegeExplorer'

const nav = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/profile', label: 'My Profile', icon: UserRound },
  { to: '/careers', label: 'Career Explorer', icon: Compass },
  { to: '/roadmap', label: 'My Roadmap', icon: Map },
  { to: '/resources', label: 'Learning Resources', icon: BookOpen },
  { to: '/progress', label: 'Progress', icon: TrendingUp },
  { to: '/colleges', label: 'College Explorer', icon: Building2 },
]

function AppShell({ children, student, onLogout }: { children: ReactNode; student: StudentProfile; onLogout: () => Promise<void> }) {
  const [collapsed, setCollapsed] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className="app-shell">
      <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
        <div className="brand">
          <div className="brand-mark"><Sparkles size={18} /></div>
          {!collapsed && <div><strong>SkillSensei</strong><span>Career navigation</span></div>}
        </div>
        <button className="collapse-btn" onClick={() => setCollapsed(v => !v)} aria-label="Toggle sidebar">
          {collapsed ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
        </button>
        <nav className="side-nav">
          {nav.map(item => {
            const Icon = item.icon
            const active = location.pathname === item.to || (item.to === '/careers' && location.pathname.startsWith('/careers/'))
            return <button key={item.to} className={`nav-item ${active ? 'active' : ''}`} onClick={() => navigate(item.to)} title={collapsed ? item.label : undefined}><Icon size={18} />{!collapsed && <span>{item.label}</span>}</button>
          })}
        </nav>
        <div className="sidebar-bottom">
          <div className="student-mini">
            <div className="avatar">{student.name.charAt(0).toUpperCase()}</div>
            {!collapsed && <div><strong>{student.name}</strong><span>Class {student.class_level}</span></div>}
          </div>
          <button className="nav-item ghost" onClick={onLogout}><LogOut size={18} />{!collapsed && <span>Log out</span>}</button>
        </div>
      </aside>
      <main className="main-area">
        <header className="topbar">
          <div className="topbar-title">{nav.find(n => location.pathname.startsWith(n.to))?.label || 'SkillSensei'}</div>
          <div className="topbar-right"><span className="board-pill">{student.board}</span><span className="location-pill">{student.city || 'India'}</span><UserButton /></div>
        </header>
        <div className="page-content">{children}</div>
      </main>
    </div>
  )
}

function SignedOutGate() {
  return <div className="loading-screen"><Sparkles size={26}/><div>You need to sign in to continue.</div><SignInButton mode="modal"><button className="primary-btn">Sign in</button></SignInButton></div>
}

export default function App() {
  const { isLoaded, isSignedIn, getToken, userId, signOut } = useAuth()
  const [student, setStudent] = useState<StudentProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    configureAuth(getToken)
  }, [getToken])

  useEffect(() => {
    if (!isLoaded) return
    if (!isSignedIn) {
      setStudent(null)
      setLoading(false)
      return
    }

    let active = true
    setLoading(true)
    api.me().then(profile => {
      if (!active) return
      setStudent(profile)
      if (location.pathname === '/' || location.pathname === '/onboarding') navigate('/dashboard', { replace: true })
    }).catch(() => {
      if (!active) return
      setStudent(null)
      if (location.pathname !== '/onboarding') navigate('/onboarding', { replace: true })
    }).finally(() => { if (active) setLoading(false) })

    return () => { active = false }
  }, [isLoaded, isSignedIn, userId, navigate])

  const handleLogout = async () => {
    await signOut({ redirectUrl: '/' })
    setStudent(null)
  }

  if (!isLoaded || loading) return <div className="loading-screen"><div className="loading-orb"><Sparkles /></div><div>Loading your SkillSensei workspace…</div></div>

  return (
    <Routes>
      <Route path="/" element={isSignedIn ? <Navigate to={student ? '/dashboard' : '/onboarding'} replace /> : <Landing />} />
      <Route path="/onboarding" element={!isSignedIn ? <SignedOutGate /> : student ? <Navigate to="/dashboard" replace /> : <Onboarding onCreated={(s) => { setStudent(s); navigate('/dashboard', { replace: true }) }} />} />
      {student ? <Route path="*" element={<AppShell student={student} onLogout={handleLogout}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard student={student} />} />
          <Route path="/profile" element={<Profile student={student} onSaved={setStudent} />} />
          <Route path="/careers" element={<Careers />} />
          <Route path="/careers/:careerId" element={<CareerDetails />} />
          <Route path="/roadmap" element={<Roadmap student={student} />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/progress" element={<Progress student={student} />} />
          <Route path="/colleges" element={<CollegeExplorer />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AppShell>} /> : <Route path="*" element={isSignedIn ? <Navigate to="/onboarding" replace /> : <Landing />} />}
    </Routes>
  )
}


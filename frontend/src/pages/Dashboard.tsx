import { useEffect, useState } from 'react'
import { ArrowRight, CheckCircle2, ChevronRight, Circle, Sparkles, Target, TrendingUp } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import type { DashboardData, StudentProfile } from '../types'
import RecommendationCard from '../components/RecommendationCard'
import ScoreBar from '../components/ScoreBar'
import SectionHeader from '../components/SectionHeader'

export default function Dashboard({ student }: { student: StudentProfile }) {
  const [data, setData] = useState<DashboardData | null>(null)
  const [analysis, setAnalysis] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  useEffect(() => {
    api.dashboard().then(setData).catch(err => setError(err instanceof Error ? err.message : 'Could not load your dashboard.'))
  }, [student.id])
  const refresh = async () => {
    setAnalysis(true); setError('')
    try { await api.analyze(); setData(await api.dashboard()) }
    catch (err) { setError(err instanceof Error ? err.message : 'Could not refresh recommendations.') }
    finally { setAnalysis(false) }
  }
  if (!data && error) return <div className="loading-box"><strong>We couldn’t load your dashboard.</strong><br /><button className="secondary-btn small" onClick={refresh}>Try again</button></div>
  if (!data) return <div className="loading-box">Loading your dashboard…</div>
  const next = data.roadmap.find(x => !x.completed)
  return <div>
    <div className="page-hero"><div><span className="eyebrow">Your career navigation</span><h1>Good morning, {student.name.split(' ')[0]}.</h1><p>You’re in Class {student.class_level}. Here’s what SkillSensei thinks deserves your attention right now.</p></div><button className="secondary-btn" onClick={refresh} disabled={analysis}><Sparkles size={16} />{analysis ? 'Re-analyzing…' : 'Refresh recommendations'}</button></div>
    <div className="stat-grid"><div className="stat-card"><div className="stat-icon"><Target size={18}/></div><span>Career exploration</span><strong>{data.progress.career_exploration}%</strong><small>Profile + direction</small></div><div className="stat-card"><div className="stat-icon"><TrendingUp size={18}/></div><span>Skill readiness</span><strong>{data.progress.skills}%</strong><small>Based on your current stage</small></div><div className="stat-card"><div className="stat-icon"><CheckCircle2 size={18}/></div><span>Roadmap progress</span><strong>{data.progress.roadmap}%</strong><small>{data.roadmap.filter(x => x.completed).length} milestones complete</small></div><div className="stat-card featured"><span>Overall journey</span><strong>{data.progress.overall}%</strong><div className="mini-line"><i style={{width: `${data.progress.overall}%`}} /></div><small>Keep building momentum</small></div></div>
    <div className="dashboard-grid"><section><SectionHeader eyebrow="Your strongest signals" title="Career directions" action={<button className="link-btn" onClick={() => navigate('/careers')}>View all <ArrowRight size={15}/></button>} /><div className="recommend-list">{data.recommendations.slice(0,3).map(r => <RecommendationCard key={r.career_id} rec={r} />)}</div></section><section><SectionHeader eyebrow="Right now" title="Next best step" /><div className="next-card"><div className="next-badge">UP NEXT</div><h3>{next?.title || 'Your roadmap is complete'}</h3><p>{next?.description || 'Review your profile and explore a new career direction.'}</p><div className="next-meta"><span>{next?.horizon || 'Anytime'}</span><span>{next?.type || 'explore'}</span></div><button className="primary-btn small" onClick={() => navigate('/roadmap')}>Open roadmap <ArrowRight size={16}/></button></div><div className="profile-card"><div className="avatar large">{student.name.charAt(0).toUpperCase()}</div><div><span className="eyebrow">Profile signal</span><strong>{data.recommendations[0]?.career} looks like your strongest current direction.</strong><span>Based on your academics, interests, strengths, and work preferences.</span></div></div></section></div>
    <section className="dashboard-grid lower"><section><SectionHeader eyebrow="Your strengths" title="What stands out" /><div className="strength-card">{data.strengths.map(s => <div className="strength-row" key={s.name}><span>{s.name}</span><b>{s.score}</b><ScoreBar value={s.score}/></div>)}</div></section><section><SectionHeader eyebrow="Your journey" title="Roadmap preview" action={<button className="link-btn" onClick={() => navigate('/roadmap')}>Open roadmap <ArrowRight size={15}/></button>} /><div className="timeline-card">{data.roadmap.slice(0,5).map((r,i) => <div className="timeline-row" key={r.id}><div className={`timeline-dot ${r.completed ? 'done':''}`}>{r.completed ? <CheckCircle2 size={15}/> : <Circle size={11}/>}</div><div><strong>{r.title}</strong><span>{r.description}</span></div><ChevronRight size={16}/></div>)}</div></section></section>
  </div>
}

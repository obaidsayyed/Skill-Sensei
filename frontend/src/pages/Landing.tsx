import { ArrowRight, CheckCircle2, Compass, Map, Sparkles, Target, TrendingUp } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import AuthDialog from '../components/AuthDialog'

export default function Landing() {
  const navigate = useNavigate()
  const [authMode, setAuthMode] = useState<'sign-in' | 'sign-up' | null>(null)

  return <div className="landing">
    <header className="landing-nav"><div className="brand"><div className="brand-mark"><Sparkles size={18} /></div><div><strong>SkillSensei</strong><span>Career navigation</span></div></div><div className="landing-auth"><button className="text-btn" onClick={() => setAuthMode('sign-in')}>Sign in</button><button className="text-btn" onClick={() => setAuthMode('sign-up')}>Create account <ArrowRight size={16} /></button></div></header>
    <section className="hero">
      <div className="hero-copy"><span className="eyebrow"><Sparkles size={15} /> Personal career navigation for students</span><h1>Don’t just choose a career.<br /><em>Figure out where you fit.</em></h1><p>SkillSensei turns your academics, interests, strengths, and goals into a living career map — what fits you, what to learn next, and where to go from here.</p><div className="hero-actions"><button className="primary-btn" onClick={() => setAuthMode('sign-up')}>Build my career map <ArrowRight size={18} /></button><span className="micro-copy"><CheckCircle2 size={15} /> Built for classes 10–12</span></div></div>
      <div className="hero-visual"><div className="hero-card main"><div className="card-kicker">YOUR CAREER DIRECTION</div><div className="hero-score"><div><strong>Computer Science</strong><span>Strong match based on your profile</span></div><b>91%</b></div><div className="signal"><div><span>Logical reasoning</span><span>91</span></div><div className="meter"><i style={{ width: '91%' }} /></div></div><div className="signal"><div><span>Analytical thinking</span><span>84</span></div><div className="meter"><i style={{ width: '84%' }} /></div></div><div className="signal"><div><span>Technology interest</span><span>96</span></div><div className="meter"><i style={{ width: '96%' }} /></div></div><div className="hero-next"><span>Next best step</span><strong>Explore your personalized roadmap <ArrowRight size={15} /></strong></div></div><div className="floating-card one"><Compass size={17} /><div><strong>12 career paths</strong><span>Explore beyond the usual choices</span></div></div><div className="floating-card two"><TrendingUp size={17} /><div><strong>Profile evolves</strong><span>Recommendations update as you do</span></div></div></div>
    </section>
    <section className="value-grid"><div><Target size={20} /><h3>Understand your fit</h3><p>See the reasoning behind each career recommendation rather than receiving a black-box label.</p></div><div><Map size={20} /><h3>Know what to do next</h3><p>Get class-specific milestones across subjects, skills, projects, and admissions.</p></div><div><TrendingUp size={20} /><h3>Keep evolving</h3><p>Refresh your profile as interests change and your academic direction becomes clearer.</p></div></section>
    {authMode && <AuthDialog mode={authMode} onClose={() => setAuthMode(null)} onModeChange={setAuthMode} />}
  </div>
}

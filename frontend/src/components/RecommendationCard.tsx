import { ArrowRight, Swords } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import type { Recommendation } from '../types'

export default function RecommendationCard({ rec, compact = false }: { rec: Recommendation; compact?: boolean }) {
  const navigate = useNavigate()
  return <div className={`recommend-card ${compact ? 'compact' : ''}`}><div className="recommend-top"><div className="career-icon"><Swords size={17} /></div><div className="recommend-title"><strong>{rec.career}</strong><span>{rec.domain}</span></div><div className="match"><span style={{ background: 'var(--brand-primary)', color: '#fff', padding: '4px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 'bold' }}>{rec.alignment_label}</span></div></div><p>{rec.why_match[0]}</p>{!compact && <div className="recommend-footer"><span>Confidence: {rec.confidence}</span><button className="link-btn" onClick={() => navigate(`/careers/${rec.career_id}`)}>Explore <ArrowRight size={15} /></button></div>}</div>
}

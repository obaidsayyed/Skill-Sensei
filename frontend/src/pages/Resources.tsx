import { useEffect, useMemo, useState } from 'react'
import { ExternalLink, Filter } from 'lucide-react'
import { api } from '../services/api'
import type { CareerResources } from '../types'
import SectionHeader from '../components/SectionHeader'

export default function Resources() {
  const [careerResources, setCareerResources] = useState<CareerResources[]>([])
  const [level, setLevel] = useState('All')
  const [error, setError] = useState('')

  useEffect(() => {
    api.resources()
      .then(setCareerResources)
      .catch(err => setError(err instanceof Error ? err.message : 'Could not load resources.'))
  }, [])

  return (
    <div>
      <div className="page-hero">
        <div>
          <span className="eyebrow">Curated learning paths</span>
          <h1>Learning Resources</h1>
          <p>SkillSensei structures useful free and low-cost resources around the skills you actually need.</p>
        </div>
      </div>
      
      {error && <div className="loading-box">{error}</div>}
      
      <div className="filter-row">
        <Filter size={16}/>
        {['All', 'Beginner', 'Intermediate'].map(x => (
          <button 
            className={`filter-chip ${level === x ? 'active' : ''}`} 
            key={x} 
            onClick={() => setLevel(x)}
          >
            {x}
          </button>
        ))}
      </div>

      {careerResources.map(cr => {
        const filtered = level === 'All' ? cr.resources : cr.resources.filter(r => r.level === level)
        if (filtered.length === 0) return null

        return (
          <div key={cr.career_id} className="resource-section" style={{ marginBottom: '40px' }}>
            <SectionHeader eyebrow={`${filtered.length} resources`} title={cr.career} />
            <div className="resource-list">
              {filtered.map(r => (
                <a className="resource-card" key={r.id} href={r.url} target="_blank" rel="noreferrer">
                  <div className="resource-main">
                    <span>{r.category}</span>
                    <h3>{r.title}</h3>
                    <p>{r.provider} · {r.level} · {r.free ? 'Free' : 'Paid'}</p>
                  </div>
                  <ExternalLink size={17}/>
                </a>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}

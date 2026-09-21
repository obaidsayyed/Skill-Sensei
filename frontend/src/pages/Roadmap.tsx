import { useEffect, useState } from 'react'
import { Check, Circle, Clock3, Sparkles } from 'lucide-react'
import { api } from '../services/api'
import type { CareerRoadmap, RoadmapItem, StudentProfile } from '../types'
import SectionHeader from '../components/SectionHeader'

export default function Roadmap({student}:{student:StudentProfile}) {
  const [roadmaps, setRoadmaps] = useState<CareerRoadmap[]>([])
  const [activeTabId, setActiveTabId] = useState<string>('')
  const [error, setError] = useState('')

  useEffect(() => {
    api.roadmap()
      .then(res => {
        setRoadmaps(res)
        if (res.length > 0) setActiveTabId(res[0].career_id)
      })
      .catch(err => setError(err instanceof Error ? err.message : 'Could not load roadmap.'))
  }, [])

  const complete = async(item:RoadmapItem) => {
    setError('')
    try {
      const updatedItem = await api.completeRoadmapItem(item.id)
      setRoadmaps(current => current.map(rm => ({
        ...rm,
        items: rm.items.map(i => i.id === item.id ? updatedItem : i)
      })))
    } catch(err) {
      setError(err instanceof Error ? err.message : 'Could not update this milestone.')
    }
  }

  if (error && !roadmaps.length) return <div className="loading-box">{error}</div>
  if (!roadmaps.length) return <div className="loading-box">Loading your roadmaps...</div>

  const activeRoadmap = roadmaps.find(rm => rm.career_id === activeTabId) || roadmaps[0]
  const items = activeRoadmap.items

  return (
    <div>
      <div className="page-hero">
        <div>
          <span className="eyebrow">Class {student.class_level} roadmap</span>
          <h1>My Roadmap</h1>
          <p>A time-bound set of next steps for your top recommended careers.</p>
        </div>
      </div>
      
      {error && <div className="loading-box">{error}</div>}
      
      <div className="filter-row">
        {roadmaps.map(rm => (
          <button 
            key={rm.career_id} 
            className={`filter-chip ${activeTabId === rm.career_id ? 'active' : ''}`}
            onClick={() => setActiveTabId(rm.career_id)}
          >
            {rm.career}
          </button>
        ))}
      </div>

      <div className="roadmap-header">
        <div><Sparkles size={17}/><span>Built around your current profile</span></div>
        <strong>{items.filter(x=>x.completed).length} / {items.length} complete</strong>
      </div>
      
      <SectionHeader eyebrow="Your journey" title={`What to do next for ${activeRoadmap.career}`}/>
      
      <div className="roadmap-list">
        {items.map((item, idx) => (
          <div className={`roadmap-item ${item.completed?'completed':''}`} key={item.id}>
            <div className="roadmap-marker">
              {item.completed ? <div className="done-marker"><Check size={15}/></div> : <Circle size={13}/>}
            </div>
            <div className="roadmap-copy">
              <div className="roadmap-item-head">
                <span className="horizon">{item.horizon}</span>
                <span className="item-type">{item.type}</span>
              </div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              {!item.completed && (
                <button className="secondary-btn small" onClick={() => complete(item)}>
                  <Check size={15}/> Mark complete
                </button>
              )}
            </div>
            <div className="roadmap-time">
              <Clock3 size={14}/> {idx<2 ? 'This month' : idx<4 ? 'Next 3 months' : 'Later'}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

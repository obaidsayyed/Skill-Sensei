import type { Recommendation } from '../types'
import { InteractiveHoverButton } from './InteractiveHoverButton'

export default function CareerPathTabs({
  recommendations,
  selectedId,
  onSelect,
}: {
  recommendations: Recommendation[]
  selectedId: string
  onSelect: (careerId: string) => void
}) {
  return (
    <div className="career-path-tabs">
      {recommendations.map(rec => (
        <InteractiveHoverButton
          key={rec.career_id}
          className={`career-path-tab ${selectedId === rec.career_id ? 'active' : ''}`}
          onClick={() => onSelect(rec.career_id)}
        >
          <span>{rec.career}</span>
          <b style={{ fontSize: '0.8em', opacity: 0.8 }}>{rec.alignment_label}</b>
        </InteractiveHoverButton>
      ))}
    </div>
  )
}

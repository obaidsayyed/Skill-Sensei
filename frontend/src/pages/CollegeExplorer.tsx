import { Swords } from 'lucide-react'

export default function CollegeExplorer() {
  return (
    <div>
      <div className="page-hero">
        <div>
          <span className="eyebrow">Maharashtra-focused pathway</span>
          <h1>College Explorer</h1>
          <p>Find indicative college options based on your expected percentile.</p>
        </div>
      </div>
      
      <div style={{
        marginTop: '2rem',
        background: 'var(--card-bg)',
        border: '1px solid var(--border-color)',
        borderRadius: '16px',
        padding: '4rem 2rem',
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '1rem'
      }}>
        <div style={{ 
          width: '48px', 
          height: '48px', 
          background: 'var(--surface-color)', 
          borderRadius: '50%', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: 'var(--primary-color)'
        }}>
          <Swords size={24} />
        </div>
        
        <div>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Coming Soon</h2>
          <p style={{ color: 'var(--text-muted)', maxWidth: '400px', margin: '0 auto', lineHeight: 1.5 }}>
            We're building a comprehensive database of colleges, courses, and cutoffs. Check back soon for personalized recommendations.
          </p>
        </div>
      </div>
    </div>
  )
}

import { ArrowLeft, FileQuestion } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function NotFound() {
  const navigate = useNavigate()
  
  return (
    <div style={{ padding: '10vh 2rem', textAlign: 'center', maxWidth: '500px', margin: '0 auto', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <FileQuestion size={56} style={{ color: 'var(--border-color)', marginBottom: '1.5rem' }} />
      <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', letterSpacing: '-0.02em' }}>Page not found</h1>
      <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', marginBottom: '2.5rem', lineHeight: 1.5 }}>
        We couldn't find the page you were looking for. It might have been moved or doesn't exist.
      </p>
      <button className="primary-btn" onClick={() => navigate(-1)}>
        <ArrowLeft size={16} /> Go Back
      </button>
    </div>
  )
}

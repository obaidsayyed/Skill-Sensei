import { useState, type FormEvent } from 'react'
import { ArrowRight, CheckCircle2, LogIn, X } from 'lucide-react'
import { supabase } from '../lib/supabase'

interface AuthDialogProps {
  mode: 'sign-in' | 'sign-up'
  onClose: () => void
  onModeChange: (mode: 'sign-in' | 'sign-up') => void
}

export default function AuthDialog({ mode, onClose, onModeChange }: AuthDialogProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setBusy(true)
    setError('')
    setMessage('')

    try {
      if (mode === 'sign-in') {
        const { error: authError } = await supabase.auth.signInWithPassword({ email, password })
        if (authError) throw authError
        onClose()
        return
      }

      const { data, error: authError } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: name.trim() ? { full_name: name.trim() } : undefined,
        },
      })
      if (authError) throw authError

      if (data.session) {
        onClose()
      } else {
        setMessage('Account created. Check your email to confirm your account, then sign in.')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed.')
    } finally {
      setBusy(false)
    }
  }

  const google = async () => {
    setBusy(true)
    setError('')
    const { error: authError } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: window.location.origin },
    })
    if (authError) {
      setError(authError.message)
      setBusy(false)
    }
  }

  return (
    <div className="auth-overlay" role="dialog" aria-modal="true" aria-labelledby="auth-title">
      <div className="auth-card">
        <button className="auth-close" type="button" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>
        <div className="auth-kicker"><LogIn size={14} /> SkillSensei account</div>
        <h2 id="auth-title">{mode === 'sign-in' ? 'Welcome back.' : 'Build your SkillSensei profile.'}</h2>
        <p>{mode === 'sign-in' ? 'Sign in to continue your career map.' : 'Create your account and start your personalized career journey.'}</p>

        <button className="secondary-btn auth-google" type="button" onClick={google} disabled={busy}>
          Continue with Google <ArrowRight size={15} />
        </button>

        <div className="auth-divider"><span>or</span></div>

        <form onSubmit={submit} className="auth-form">
          {mode === 'sign-up' && (
            <label>
              Name
              <input value={name} onChange={event => setName(event.target.value)} placeholder="Your name" autoComplete="name" required />
            </label>
          )}
          <label>
            Email
            <input value={email} onChange={event => setEmail(event.target.value)} type="email" placeholder="you@example.com" autoComplete="email" required />
          </label>
          <label>
            Password
            <input value={password} onChange={event => setPassword(event.target.value)} type="password" placeholder="At least 6 characters" minLength={6} autoComplete={mode === 'sign-in' ? 'current-password' : 'new-password'} required />
          </label>

          {error && <div className="inline-error">{error}</div>}
          {message && <div className="auth-success"><CheckCircle2 size={15} />{message}</div>}

          <button className="primary-btn auth-submit" type="submit" disabled={busy}>
            {busy ? 'Please wait…' : mode === 'sign-in' ? 'Sign in' : 'Create account'}
            {!busy && <ArrowRight size={16} />}
          </button>
        </form>

        <div className="auth-switch">
          {mode === 'sign-in' ? 'New to SkillSensei?' : 'Already have an account?'}{' '}
          <button type="button" onClick={() => { setError(''); setMessage(''); onModeChange(mode === 'sign-in' ? 'sign-up' : 'sign-in') }}>
            {mode === 'sign-in' ? 'Create account' : 'Sign in'}
          </button>
        </div>
      </div>
    </div>
  )
}

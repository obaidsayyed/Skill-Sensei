import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ArrowRight, Check, CheckCircle2, Sparkles } from 'lucide-react'
import { api } from '../services/api'
import { useUser } from '@clerk/react'
import type { StudentProfile } from '../types'
import type { AssessmentQuestion, AssessmentResult } from '../types/assessment'

const interests = ['Technology', 'Business', 'Design', 'Finance', 'Science', 'Law', 'Healthcare', 'Media', 'Psychology', 'Entrepreneurship']
const strengths = ['Logical reasoning', 'Communication', 'Creativity', 'Problem solving', 'Mathematics', 'Leadership', 'Research', 'Empathy', 'Attention to detail']
const workStyles = ['Building things', 'Analyzing information', 'Working with people', 'Leading teams', 'Creating visually', 'Explaining ideas', 'Working independently']
const subjects = ['Mathematics', 'Science', 'Computer Science', 'English', 'Social Science', 'Economics', 'Accountancy', 'Languages']

export default function Onboarding({ onCreated }: { onCreated: (profile: StudentProfile) => void }) {
  const { user } = useUser()
  const [step, setStep] = useState(1)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [profileSaved, setProfileSaved] = useState(false)
  const [savedProfile, setSavedProfile] = useState<StudentProfile | null>(null)
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([])
  const [questionIndex, setQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [assessmentResult, setAssessmentResult] = useState<AssessmentResult | null>(null)
  const [form, setForm] = useState<StudentProfile>({ name: '', class_level: 10, board: 'Maharashtra State Board', city: '', subjects: [], interests: [], strengths: [], work_styles: [], goals: 'I am exploring my options' })

  useEffect(() => {
    const preferredName = user?.fullName || user?.firstName || ''
    if (preferredName && !form.name) setForm(f => ({ ...f, name: preferredName }))
  }, [user?.fullName, user?.firstName])

  const toggle = (key: 'subjects'|'interests'|'strengths'|'work_styles', value: string) => setForm(f => ({ ...f, [key]: f[key].includes(value) ? f[key].filter(x => x !== value) : [...f[key], value] }))

  const valid = useMemo(() => {
    if (step === 1) return form.name.trim() && form.city.trim()
    if (step === 2) return form.subjects.length >= 2
    if (step === 3) return form.interests.length >= 2 && form.strengths.length >= 2
    if (step === 4) return form.work_styles.length >= 1
    return true
  }, [step, form])

  const startAssessment = async () => {
    setSaving(true)
    setError('')
    try {
      const saved = await api.createStudent(form)
      setProfileSaved(true)
      setSavedProfile(saved)
      const bank = await api.assessmentQuestions()
      setQuestions(bank.questions)
      setAnswers({})
      setQuestionIndex(0)
      setStep(5)
      // Keep the saved profile in this page until assessment is complete; dashboard is created only after the result.
      void saved
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not start your assessment.')
    } finally {
      setSaving(false)
    }
  }

  const next = async () => {
    if (!valid || saving) return
    if (step < 4) {
      setStep(s => s + 1)
      return
    }
    await startAssessment()
  }

  const selectAnswer = (optionId: string) => {
    const question = questions[questionIndex]
    if (!question) return
    setAnswers(prev => ({ ...prev, [question.id]: optionId }))
  }

  const nextQuestion = async () => {
    const question = questions[questionIndex]
    if (!question || !answers[question.id]) return
    if (questionIndex < questions.length - 1) {
      setQuestionIndex(i => i + 1)
      return
    }

    setSaving(true)
    setError('')
    try {
      const result = await api.submitAssessment({
        question_ids: questions.map(q => q.id),
        answers: questions.map(q => ({ question_id: q.id, option_id: answers[q.id] })),
      })
      setAssessmentResult(result)
      setStep(6)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not submit your assessment.')
    } finally {
      setSaving(false)
    }
  }

  const finishAssessment = async () => {
    if (!assessmentResult || !profileSaved) return
    setSaving(true)
    setError('')
    try {
      await api.analyze()
      onCreated(savedProfile || { ...form })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not build your career map.')
    } finally {
      setSaving(false)
    }
  }

  const stepLabel = step <= 4 ? `Step ${step} of 6` : step === 5 ? 'Assessment' : 'Assessment result'

  if (step === 5) {
    const question = questions[questionIndex]
    const selected = question ? answers[question.id] : undefined
    return <div className="onboarding assessment-page">
      <header className="landing-nav"><button className="text-btn" onClick={() => setStep(4)} disabled={saving}><ArrowLeft size={16} /> Back</button><div className="brand"><div className="brand-mark"><Sparkles size={18} /></div><strong>SkillSensei</strong></div><span className="step-counter">{stepLabel}</span></header>
      <div className="onboarding-wrap"><div className="assessment-wrap">
        <div className="assessment-intro"><span className="eyebrow">Your short assessment</span><h1>Let’s test the pattern behind your interests.</h1><p>There are 15 questions. There are no right or wrong personalities here; we are looking for how you naturally approach situations.</p></div>
        <div className="assessment-progress"><div><span>Question {questionIndex + 1} of {questions.length}</span><b>{Math.round(((questionIndex + 1) / questions.length) * 100)}%</b></div><div className="progress-line"><span style={{ width: `${((questionIndex + 1) / questions.length) * 100}%` }} /></div></div>
        {question && <div className="assessment-card"><div className="assessment-meta"><span>{question.interest}</span><span>{question.dimension.replace('_', ' ')}</span></div><h2>{question.question}</h2><div className="assessment-options">{question.options.map(option => <button key={option.id} className={`assessment-option ${selected === option.id ? 'selected' : ''}`} onClick={() => selectAnswer(option.id)}><span className="assessment-option-dot" />{option.text}</button>)}</div><div className="form-actions"><span>Question {questionIndex + 1} / {questions.length}</span><button className="primary-btn" disabled={!selected || saving} onClick={nextQuestion}>{saving ? 'Evaluating…' : questionIndex === questions.length - 1 ? 'See my result' : 'Next question'}{!saving && <ArrowRight size={17} />}</button></div></div>}
        {error && <div className="inline-error">{error}</div>}
      </div></div>
    </div>
  }

  if (step === 6 && assessmentResult) {
    return <div className="onboarding assessment-page">
      <header className="landing-nav"><div className="brand"><div className="brand-mark"><Sparkles size={18} /></div><strong>SkillSensei</strong></div><span className="step-counter">{stepLabel}</span></header>
      <div className="onboarding-wrap"><div className="assessment-result-wrap">
        <div className="result-hero"><div className="result-icon"><CheckCircle2 size={28} /></div><span className="eyebrow">Assessment complete</span><h1>{assessmentResult.message}</h1><p>Alignment signal: <strong>{assessmentResult.alignment_score}%</strong>. This is a guidance signal, not a permanent label.</p></div>
        <div className="result-grid"><div className="result-card"><div className="result-card-head"><div><span className="eyebrow">Your stream suggestions</span><h2>What your profile suggests now</h2></div><span className={`alignment-pill ${assessmentResult.status}`}>{assessmentResult.status === 'strong_match' ? 'Strong alignment' : assessmentResult.status === 'partial_match' ? 'Partial alignment' : 'Broadened view'}</span></div><div className="stream-suggestion-list">{assessmentResult.stream_suggestions.map((item, index) => <div className="stream-suggestion" key={`${item.recommendation_id || item.stream_id}-${index}`}><div><strong>{item.stream}</strong>{item.source === 'assessment' && <span className="assessment-tag">Assessment pattern</span>}</div><div className="stream-subjects">{(item.focus_subjects || []).map(subject => <span key={subject}>{subject}</span>)}</div><span>{item.source === 'assessment' ? 'Suggested from how you answered the assessment.' : 'Suggested from the interests you entered.'}</span></div>)}</div></div>
          <div className="result-card result-note"><span className="eyebrow">How to read this</span><h3>Your answers are one more signal.</h3><p>SkillSensei combines your stated interests with your answering pattern. A broader suggestion does not mean an option is ruled out; it means we are giving you more directions to explore.</p></div></div>
        {error && <div className="inline-error">{error}</div>}
        <div className="form-actions result-actions"><span>Your assessment is saved to your SkillSensei profile.</span><button className="primary-btn" onClick={finishAssessment} disabled={saving}>{saving ? 'Building your map…' : 'Continue to my career map'}{!saving && <ArrowRight size={17} />}</button></div>
      </div></div>
    </div>
  }

  return <div className="onboarding"><header className="landing-nav"><button className="text-btn" onClick={() => setStep(s => Math.max(1, s - 1))} disabled={saving}><ArrowLeft size={16} /> Back</button><div className="brand"><div className="brand-mark"><Sparkles size={18} /></div><strong>SkillSensei</strong></div><span className="step-counter">{stepLabel}</span></header><div className="onboarding-wrap"><div className="progress-line"><span style={{ width: `${step * 20}%` }} /></div><div className="form-card">
    {step === 1 && <><span className="eyebrow">Start with context</span><h1>Tell us where you are today.</h1><p>We use this to make recommendations appropriate for your class and education system.</p><label>Your name<input value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} placeholder="Aarav" /></label><div className="two-col"><label>Class<select value={form.class_level} onChange={e => setForm({ ...form, class_level: Number(e.target.value) as 10|11|12 })}><option value={10}>10th</option><option value={11}>11th</option><option value={12}>12th</option></select></label><label>Board<select value={form.board} onChange={e => setForm({ ...form, board: e.target.value })}><option>Maharashtra State Board</option><option>CBSE</option><option>ICSE</option><option>Other</option></select></label></div><label>City<input value={form.city} onChange={e => setForm({ ...form, city: e.target.value })} placeholder="Pune" /></label></>}
    {step === 2 && <><span className="eyebrow">Your academics</span><h1>Which subjects feel natural to you?</h1><p>Pick at least two. This is about confidence and enjoyment, not just marks.</p><div className="chip-grid">{subjects.map(x => <button key={x} className={`choice-chip ${form.subjects.includes(x) ? 'selected' : ''}`} onClick={() => toggle('subjects', x)}>{form.subjects.includes(x) && <Check size={14} />}{x}</button>)}</div></>}
    {step === 3 && <><span className="eyebrow">Your signals</span><h1>What pulls your attention?</h1><p>Choose the things you naturally enjoy and the abilities you trust yourself in.</p><h4>Interests</h4><div className="chip-grid small">{interests.map(x => <button key={x} className={`choice-chip ${form.interests.includes(x) ? 'selected' : ''}`} onClick={() => toggle('interests', x)}>{form.interests.includes(x) && <Check size={14} />}{x}</button>)}</div><h4>Strengths</h4><div className="chip-grid small">{strengths.map(x => <button key={x} className={`choice-chip ${form.strengths.includes(x) ? 'selected' : ''}`} onClick={() => toggle('strengths', x)}>{form.strengths.includes(x) && <Check size={14} />}{x}</button>)}</div></>}
    {step === 4 && <><span className="eyebrow">How you like to work</span><h1>What kind of work sounds satisfying?</h1><p>This helps separate careers that look similar on paper but feel very different day to day.</p><div className="chip-grid">{workStyles.map(x => <button key={x} className={`choice-chip ${form.work_styles.includes(x) ? 'selected' : ''}`} onClick={() => toggle('work_styles', x)}>{form.work_styles.includes(x) && <Check size={14} />}{x}</button>)}</div><label>What are you hoping to get from SkillSensei?<select value={form.goals} onChange={e => setForm({ ...form, goals: e.target.value })}><option>I am exploring my options</option><option>I have a few careers in mind</option><option>I know my field but need a plan</option><option>I need help choosing a stream</option><option>I need college and admission guidance</option></select></label></>}
    {error && <div className="inline-error">{error}</div>}
    <div className="form-actions"><span>{step < 4 ? 'You can change this later.' : 'Next, you will take a 15-question assessment.'}</span><button className="primary-btn" disabled={!valid || saving} onClick={next}>{saving ? 'Preparing assessment…' : step === 4 ? 'Continue to assessment' : 'Continue'}{!saving && <ArrowRight size={17} />}</button></div>
  </div></div></div>
}

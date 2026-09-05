export interface AssessmentOption {
  id: string
  text: string
}

export interface AssessmentQuestion {
  id: string
  interest: string
  dimension: string
  question: string
  options: AssessmentOption[]
}

export interface AssessmentQuestionsResponse {
  attempt_id: string
  total_questions: number
  questions: AssessmentQuestion[]
}

export interface StreamSuggestion {
  stream_id: string
  stream: string
  match_score?: number
  source: 'assessment' | 'interest'
  tag?: string | null
  focus_subjects?: string[]
  recommendation_id?: string
}

export interface AssessmentResult {
  status: 'strong_match' | 'partial_match' | 'not_fully_match'
  alignment_score: number
  answered_questions: number
  total_questions: number
  answer_stream_scores: Record<string, number>
  interest_stream_scores: Record<string, number>
  stream_suggestions: StreamSuggestion[]
  message: string
}

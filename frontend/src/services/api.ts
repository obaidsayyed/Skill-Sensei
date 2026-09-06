import type {
  Career,
  DashboardData,
  Recommendation,
  RoadmapItem,
  StudentProfile,
  Resource,
  College,
} from '../types'

import type {
  AssessmentQuestionsResponse,
  AssessmentResult,
} from '../types/assessment'

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

type TokenGetter = (options?: { forceRefresh?: boolean }) => Promise<string | null>
let tokenGetter: TokenGetter | null = null

export function configureAuth(getToken: TokenGetter) {
  tokenGetter = getToken
}

async function performRequest(
  path: string,
  options: RequestInit,
  token: string | null
): Promise<Response> {
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Bearer ${token}`)
  else headers.delete('Authorization')

  return fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  if (!tokenGetter) throw new Error('Authentication is not initialized.')

  let token = await tokenGetter()
  let response = await performRequest(path, options, token)

  if (response.status === 401) {
    token = await tokenGetter({ forceRefresh: true })
    response = await performRequest(path, options, token)
  }

  if (!response.ok) {
    const body = await response.text()
    let message = body || `Request failed: ${response.status}`
    try {
      const parsed = JSON.parse(body)
      if (parsed?.detail) {
        message = typeof parsed.detail === 'string' ? parsed.detail : JSON.stringify(parsed.detail)
      }
    } catch {
      // Keep the raw response text.
    }
    throw new Error(message)
  }

  return response.json()
}

export const api = {
  health: () =>
    request<{ status: string }>('/health'),

  me: () =>
    request<StudentProfile>('/me'),

  createStudent: (profile: StudentProfile) =>
    request<StudentProfile>('/students', {
      method: 'POST',
      body: JSON.stringify(profile),
    }),

  analyze: () =>
    request<{
      recommendations: Recommendation[]
      ai_summary: string
    }>('/analysis/career-match', {
      method: 'POST',
    }),

  dashboard: () =>
    request<DashboardData>('/students/me/dashboard'),

  careers: () =>
    request<Career[]>('/careers'),

  career: (careerId: string) =>
    request<Career>(`/careers/${careerId}`),

  roadmap: () =>
    request<RoadmapItem[]>('/students/me/roadmap'),

  completeRoadmapItem: (itemId: string) =>
    request<RoadmapItem>(
      `/students/me/roadmap/${itemId}/complete`,
      {
        method: 'POST',
      }
    ),

  resources: () =>
    request<Resource[]>('/resources'),

  colleges: () =>
    request<College[]>('/colleges'),

  predictColleges: (payload: {
    percentile: number
    branch?: string
    city?: string
  }) =>
    request<College[]>('/college-predict', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  assessmentQuestions: () =>
    request<AssessmentQuestionsResponse>(
      '/assessment/questions'
    ),

  submitAssessment: (payload: {
    question_ids: string[]
    answers: {
      question_id: string
      option_id: string
    }[]
  }) =>
    request<AssessmentResult>('/assessment/submit', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  assessmentStatus: () =>
    request<AssessmentResult & { completed: boolean }>(
      '/assessment/status'
    ),
}
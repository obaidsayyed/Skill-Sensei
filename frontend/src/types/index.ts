export interface StudentProfile {
  id?: string
  name: string
  class_level: 10 | 11 | 12
  board: string
  city: string
  subjects: string[]
  interests: string[]
  strengths: string[]
  work_styles: string[]
  goals: string
  marks?: number
}

export interface Recommendation {
  career_id: string
  career: string
  domain: string
  match_score: number
  confidence: 'High' | 'Medium' | 'Low'
  why_match: string[]
  skill_gaps: string[]
  next_steps: string[]
}

export interface Career {
  id: string
  name: string
  domain: string
  description: string
  education: string[]
  skills: string[]
  work_style: string[]
  subjects: string[]
  paths: string[]
  growth: string
  salary_range: string
  entrance: string[]
}

export interface RoadmapItem {
  id: string
  horizon: string
  title: string
  description: string
  type: 'academic' | 'skill' | 'explore' | 'admission' | 'project'
  completed: boolean
}

export interface Resource {
  id: string
  title: string
  provider: string
  category: string
  level: string
  url: string
  free: boolean
}

export interface College {
  id: string
  name: string
  city: string
  branch: string
  cutoff_percentile: number
  type: string
}

export interface DashboardData {
  student: StudentProfile
  recommendations: Recommendation[]
  strengths: { name: string; score: number }[]
  roadmap: RoadmapItem[]
  progress: { career_exploration: number; skills: number; roadmap: number; overall: number }
  resources: Resource[]
}

export * from './assessment'

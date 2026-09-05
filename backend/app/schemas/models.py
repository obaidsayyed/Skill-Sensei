from typing import Literal, Optional
from pydantic import BaseModel, Field

class StudentProfile(BaseModel):
    id: Optional[str] = None
    name: str
    class_level: Literal[10, 11, 12]
    board: str
    city: str
    subjects: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    work_styles: list[str] = Field(default_factory=list)
    goals: str
    marks: Optional[float] = None

class Recommendation(BaseModel):
    career_id: str
    career: str
    domain: str
    match_score: int
    confidence: Literal["High", "Medium", "Low"]
    why_match: list[str]
    skill_gaps: list[str]
    next_steps: list[str]

class RoadmapItem(BaseModel):
    id: str
    horizon: str
    title: str
    description: str
    type: Literal["academic", "skill", "explore", "admission", "project"]
    completed: bool = False

class CollegePredictRequest(BaseModel):
    percentile: float = Field(ge=0, le=100)
    branch: str = ""
    city: str = ""

class AssessmentAnswer(BaseModel):
    question_id: str
    option_id: str

class AssessmentSubmitRequest(BaseModel):
    question_ids: list[str] = Field(min_length=15, max_length=15)
    answers: list[AssessmentAnswer] = Field(min_length=15, max_length=15)

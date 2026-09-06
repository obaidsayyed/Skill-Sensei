from copy import deepcopy
from urllib.parse import quote
from uuid import uuid4

import httpx

from ..core.config import settings
from ..data.careers import CAREERS
from ..data.resources import RESOURCES
from ..data.colleges import COLLEGES
from ..data.questions import QUESTIONS

STUDENTS: dict[str, dict] = {}
RECOMMENDATIONS: dict[str, list[dict]] = {}
ROADMAPS: dict[str, list[dict]] = {}
PROGRESS: dict[str, dict] = {}
ASSESSMENT_ATTEMPTS: dict[str, dict] = {}


def _supabase_enabled() -> bool:
    return bool(settings.supabase_url and settings.supabase_service_role_key)


def _supabase_headers() -> dict[str, str]:
    return {
        "apikey": settings.supabase_service_role_key,
        "Authorization": f"Bearer {settings.supabase_service_role_key}",
        "Content-Type": "application/json",
    }


def _supabase_endpoint(path: str = "students") -> str:
    return f"{settings.supabase_url.rstrip('/')}/rest/v1/{path}"


def _student_from_row(row: dict) -> dict:
    profile = deepcopy(row.get("profile") or {})
    profile["id"] = row["id"]
    profile["user_id"] = row.get("user_id")
    return profile


def _row_from_student(student: dict, user_id: str) -> dict:
    profile = deepcopy(student)
    profile.pop("id", None)
    profile.pop("user_id", None)
    return {
        "id": student.get("id") or str(uuid4()),
        "user_id": user_id,
        "profile": profile,
        "recommendations": deepcopy(RECOMMENDATIONS.get(student.get("id", ""), [])),
        "roadmap": deepcopy(ROADMAPS.get(student.get("id", ""), [])),
        "progress": deepcopy(PROGRESS.get(student.get("id", ""), {})),
    }


def _load_row_by_user(user_id: str) -> dict | None:
    if not _supabase_enabled():
        return None
    url = f"{_supabase_endpoint()}?select=*&user_id=eq.{quote(user_id, safe='')}"
    with httpx.Client(timeout=10) as client:
        response = client.get(url, headers=_supabase_headers())
    response.raise_for_status()
    rows = response.json()
    return rows[0] if rows else None


def _save_row(row: dict) -> dict:
    if not _supabase_enabled():
        return row

    url = f"{_supabase_endpoint()}?on_conflict=user_id"
    headers = {
        **_supabase_headers(),
        "Prefer": "resolution=merge-duplicates,return=representation",
    }

    timeout = httpx.Timeout(
        connect=10.0,
        read=30.0,
        write=30.0,
        pool=10.0,
    )

    with httpx.Client(timeout=timeout) as client:
        response = client.post(
            url,
            headers=headers,
            json=row,
        )

    response.raise_for_status()
    rows = response.json()
    return rows[0] if rows else row

def _persist_derived(student_id: str, user_id: str) -> None:
    if not _supabase_enabled():
        return
    student = STUDENTS[student_id]
    row = _row_from_student(student, user_id)
    _save_row(row)


def create_or_update_student(payload: dict, user_id: str) -> dict:
    existing = get_student_by_user(user_id)
    student_id = existing.get("id") if existing else payload.get("id") or str(uuid4())
    record = deepcopy(payload)
    record["id"] = student_id
    record["user_id"] = user_id
    STUDENTS[student_id] = record
    # Profile edits invalidate derived outputs so recommendations and roadmap are regenerated.
    RECOMMENDATIONS.pop(student_id, None)
    ROADMAPS.pop(student_id, None)
    PROGRESS.pop(student_id, None)
    _persist_derived(student_id, user_id)
    return deepcopy(record)


def get_student(student_id: str):
    if student_id in STUDENTS:
        return deepcopy(STUDENTS[student_id])
    return None


def get_student_by_user(user_id: str):
    # Prefer persistent Supabase state when configured.
    row = _load_row_by_user(user_id)
    if row:
        student = _student_from_row(row)
        STUDENTS[student["id"]] = deepcopy(student)
        if row.get("recommendations") is not None:
            RECOMMENDATIONS[student["id"]] = deepcopy(row.get("recommendations") or [])
        if row.get("roadmap") is not None:
            ROADMAPS[student["id"]] = deepcopy(row.get("roadmap") or [])
        if row.get("progress") is not None:
            PROGRESS[student["id"]] = deepcopy(row.get("progress") or {})
        return deepcopy(student)

    for student in STUDENTS.values():
        if student.get("user_id") == user_id:
            return deepcopy(student)
    return None


def get_student_for_user(student_id: str, user_id: str):
    student = get_student(student_id)
    if student and student.get("user_id") == user_id:
        return student
    return None


def save_derived(student_id: str, user_id: str, recommendations: list[dict], roadmap: list[dict], progress: dict | None = None):
    RECOMMENDATIONS[student_id] = deepcopy(recommendations)
    ROADMAPS[student_id] = deepcopy(roadmap)
    if progress is not None:
        PROGRESS[student_id] = deepcopy(progress)
    _persist_derived(student_id, user_id)



def _assessment_questions_endpoint() -> str:
    return _supabase_endpoint("assessment_questions")


def _assessment_attempts_endpoint() -> str:
    return _supabase_endpoint("assessment_attempts")


def list_assessment_questions() -> list[dict]:
    if _supabase_enabled():
        url = f"{_assessment_questions_endpoint()}?select=id,interest,dimension,question,options&active=eq.true"
        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=_supabase_headers())
        response.raise_for_status()
        rows = response.json()
        if rows:
            return rows
    return deepcopy(QUESTIONS)


def save_assessment_attempt(attempt: dict) -> dict:
    ASSESSMENT_ATTEMPTS[attempt["user_id"]] = deepcopy(attempt)
    if not _supabase_enabled():
        return deepcopy(attempt)
    url = f"{_assessment_attempts_endpoint()}?on_conflict=user_id"
    headers = {**_supabase_headers(), "Prefer": "resolution=merge-duplicates,return=representation"}
    with httpx.Client(timeout=10) as client:
        response = client.post(url, headers=headers, json=attempt)
    response.raise_for_status()
    rows = response.json()
    return rows[0] if rows else deepcopy(attempt)


def get_assessment_attempt(user_id: str) -> dict | None:
    if _supabase_enabled():
        url = f"{_assessment_attempts_endpoint()}?select=*&user_id=eq.{quote(user_id, safe='')}"
        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=_supabase_headers())
        response.raise_for_status()
        rows = response.json()
        if rows:
            return rows[0]
    return deepcopy(ASSESSMENT_ATTEMPTS.get(user_id))


def get_questions_by_ids(question_ids: list[str]) -> list[dict]:
    indexed = {q["id"]: q for q in list_assessment_questions()}
    return [deepcopy(indexed[qid]) for qid in question_ids if qid in indexed]


def list_careers(): return deepcopy(CAREERS)
def get_career(career_id: str): return deepcopy(next((c for c in CAREERS if c["id"] == career_id), None))
def list_resources(): return deepcopy(RESOURCES)
def list_colleges(): return deepcopy(COLLEGES)

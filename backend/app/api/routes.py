from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
import random
from uuid import uuid4

from ..auth import require_user
from ..schemas.models import StudentProfile, CollegePredictRequest, AssessmentSubmitRequest
from ..services.store import (
    RECOMMENDATIONS,
    ROADMAPS,
    PROGRESS,
    create_or_update_student,
    get_student_by_user,
    list_careers,
    get_career,
    list_resources,
    list_colleges,
    _persist_derived,
    list_assessment_questions,
    get_questions_by_ids,
    save_assessment_attempt,
    get_assessment_attempt,
)
from ..services.career_engine import score_profile, score_streams_from_profile
from ..services.roadmap_service import generate_roadmap
from ..services.ai_service import personalize_with_gemini
from ..data.questions import INTEREST_STREAMS
from ..services.assessment_service import analyze_answers, serialize_question

router=APIRouter()

@router.get('/health')
def health(): return {'status':'ok'}

@router.get('/me')
def me(user_id: Annotated[str, Depends(require_user)]):
    student = get_student_by_user(user_id)
    if not student:
        raise HTTPException(404, 'Student profile not found')
    return student

@router.post('/students', response_model=StudentProfile)
def students(payload: StudentProfile, user_id: Annotated[str, Depends(require_user)]):
    data = payload.model_dump()
    # Never trust a browser-provided ID for ownership. Supabase Auth is the source of identity.
    data.pop('id', None)
    data.pop('user_id', None)
    return create_or_update_student(data, user_id)


def _get_owned_student(user_id: str):
    student = get_student_by_user(user_id)
    if not student:
        raise HTTPException(404, 'Student profile not found. Complete onboarding first.')
    return student


def _dashboard_for_student(student: dict, user_id: str):
    student_id = student['id']
    recs = RECOMMENDATIONS.get(student_id)
    if not recs:
        recs = score_profile(student)
        RECOMMENDATIONS[student_id] = recs
    if student_id not in ROADMAPS:
        ROADMAPS[student_id] = generate_roadmap(student, recs[0] if recs else None)

    rm = ROADMAPS[student_id]
    completed=sum(x['completed'] for x in rm)
    strengths=[]
    strength_names=['Logical reasoning','Communication','Creativity','Problem solving','Mathematics','Leadership','Research','Empathy','Attention to detail']
    chosen=set(student.get('strengths',[]))
    for name in strength_names:
        base=86 if name in chosen else 58
        if name in chosen and name in student.get('interests',[]): base=min(96,base+6)
        strengths.append({'name':name,'score':base})
    skills=int(min(94,48+len(student.get('strengths',[]))*6+len(student.get('subjects',[]))*3))
    career_exploration=78 if len(recs)>=3 else 55
    roadmap_progress=int(round(completed/len(rm)*100)) if rm else 0
    overall=int(round(career_exploration*.35+skills*.2+roadmap_progress*.45))
    progress={'career_exploration':career_exploration,'skills':skills,'roadmap':roadmap_progress,'overall':overall}
    PROGRESS[student_id] = progress
    _persist_derived(student_id, user_id)
    return {'student':student,'recommendations':recs,'strengths':sorted(strengths,key=lambda x:x['score'],reverse=True)[:6], 'roadmap':rm,'progress':progress,'resources':list_resources()[:4]}

@router.get('/students/me/dashboard')
def dashboard(user_id: Annotated[str, Depends(require_user)]):
    student=_get_owned_student(user_id)
    return _dashboard_for_student(student, user_id)

@router.post('/analysis/career-match')
async def analyze(user_id: Annotated[str, Depends(require_user)]):
    student=_get_owned_student(user_id)
    recs=score_profile(student)
    roadmap=generate_roadmap(student,recs[0] if recs else None)
    RECOMMENDATIONS[student['id']]=recs
    ROADMAPS[student['id']]=roadmap
    summary=await personalize_with_gemini(student,recs)
    _persist_derived(student['id'], user_id)
    return {'recommendations':recs,'ai_summary':summary}



@router.get('/assessment/questions')
def assessment_questions(user_id: Annotated[str, Depends(require_user)]):
    student = _get_owned_student(user_id)
    pool = list_assessment_questions()
    if not pool:
        raise HTTPException(503, 'Assessment question bank is unavailable.')
    interests = set(student.get('interests', []))
    selected = [q for q in pool if q.get('interest') in interests]
    if len(selected) < 15:
        selected = pool
    # Ensure a mixed set while still emphasizing the student's selected interests.
    grouped = {}
    for q in selected:
        grouped.setdefault(q.get('interest', 'General'), []).append(q)
    questions = []
    groups = list(grouped.values())
    for group in groups:
        random.shuffle(group)
    # Give each selected interest a chance to appear, then fill randomly.
    selected_interest_groups = [grouped[i] for i in interests if i in grouped]
    for group in selected_interest_groups:
        if group and len(questions) < 15:
            questions.append(group.pop())
    remainder = [q for group in grouped.values() for q in group]
    random.shuffle(remainder)
    questions.extend(remainder[:15-len(questions)])
    random.shuffle(questions)
    questions = questions[:15]
    return {
        'attempt_id': str(uuid4()),
        'total_questions': len(questions),
        'questions': [serialize_question(q) for q in questions],
    }


@router.get('/assessment/status')
def assessment_status(user_id: Annotated[str, Depends(require_user)]):
    attempt = get_assessment_attempt(user_id)
    if not attempt:
        return {'completed': False}
    return {'completed': True, **{k: attempt.get(k) for k in ['status', 'alignment_score', 'message', 'stream_suggestions', 'answered_questions', 'total_questions']}}


@router.post('/assessment/submit')
def assessment_submit(payload: AssessmentSubmitRequest, user_id: Annotated[str, Depends(require_user)]):
    student = _get_owned_student(user_id)
    question_ids = payload.question_ids
    questions = get_questions_by_ids(question_ids)
    if len(questions) != 15:
        raise HTTPException(400, 'Assessment questions are invalid or expired. Please start the assessment again.')
    question_set = {q['id'] for q in questions}
    answers = {answer.question_id: answer.option_id for answer in payload.answers}
    if set(answers) != question_set:
        raise HTTPException(400, 'Please answer all 15 assessment questions.')
    interest_stream_scores = {stream: 0.0 for stream in ['science', 'commerce', 'arts']}
    selected_interests = [i for i in student.get('interests', []) if i in INTEREST_STREAMS]
    for interest in selected_interests:
        for stream, weight in INTEREST_STREAMS[interest].items():
            interest_stream_scores[stream] += weight
    interest_suggestions = score_streams_from_profile(student)
    result = analyze_answers(question_ids, answers, student.get('interests', []), interest_stream_scores, interest_suggestions, profile=student)
    attempt = {
        'id': str(uuid4()),
        'user_id': user_id,
        'question_ids': question_ids,
        'answers': payload.model_dump()['answers'],
        'status': result['status'],
        'alignment_score': result['alignment_score'],
        'answer_stream_scores': result['answer_stream_scores'],
        'interest_stream_scores': result['interest_stream_scores'],
        'stream_suggestions': result['stream_suggestions'],
        'answered_questions': result['answered_questions'],
        'total_questions': result['total_questions'],
    }
    save_assessment_attempt(attempt)
    return result

@router.get('/careers')
def careers(user_id: Annotated[str, Depends(require_user)]): return list_careers()
@router.get('/careers/{career_id}')
def career(career_id:str, user_id: Annotated[str, Depends(require_user)]):
    c=get_career(career_id)
    if not c: raise HTTPException(404,'Career not found')
    return c

@router.get('/students/me/roadmap')
def roadmap(user_id: Annotated[str, Depends(require_user)]):
    student=_get_owned_student(user_id)
    student_id=student['id']
    if student_id not in ROADMAPS:
        recs=RECOMMENDATIONS.get(student_id) or score_profile(student)
        RECOMMENDATIONS[student_id]=recs
        ROADMAPS[student_id]=generate_roadmap(student,recs[0] if recs else None)
        _persist_derived(student_id, user_id)
    return ROADMAPS[student_id]

@router.post('/students/me/roadmap/{item_id}/complete')
def complete(item_id:str, user_id: Annotated[str, Depends(require_user)]):
    student=_get_owned_student(user_id)
    items=ROADMAPS.get(student['id'],[])
    item=next((x for x in items if x['id']==item_id),None)
    if not item: raise HTTPException(404,'Roadmap item not found')
    item['completed']=True
    _persist_derived(student['id'], user_id)
    return item

@router.get('/resources')
def resources(user_id: Annotated[str, Depends(require_user)]): return list_resources()

@router.get('/colleges')
def colleges(user_id: Annotated[str, Depends(require_user)]): return list_colleges()

@router.post('/college-predict')
def college_predict(payload:CollegePredictRequest, user_id: Annotated[str, Depends(require_user)]):
    results=[c for c in list_colleges() if c['cutoff_percentile'] <= payload.percentile+8]
    if payload.branch: results=[c for c in results if payload.branch.lower() in c['branch'].lower()] or results
    if payload.city: results=[c for c in results if payload.city.lower() in c['city'].lower()] or results
    return sorted(results,key=lambda c:abs(payload.percentile-c['cutoff_percentile']))[:6]

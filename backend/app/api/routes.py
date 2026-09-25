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
from ..services.career_engine import score_profile, score_streams_from_profile, explore_subjects_for_stream
from ..services.roadmap_service import generate_roadmaps
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
        ROADMAPS[student_id] = generate_roadmaps(student, recs[:5])

    rm = ROADMAPS[student_id][:5]
    total_items = sum(len(career_rm['items']) for career_rm in rm)
    completed = sum(x['completed'] for career_rm in rm for x in career_rm['items'])
    
    strengths=[]
    strength_names=['Logical reasoning','Communication','Creativity','Problem solving','Mathematics','Leadership','Research','Empathy','Attention to detail']
    chosen=set(student.get('strengths',[]))
    for name in strength_names:
        base=86 if name in chosen else 58
        if name in chosen and name in student.get('interests',[]): base=min(96,base+6)
        strengths.append({'name':name,'score':base})
    skills=int(min(94,48+len(student.get('strengths',[]))*6+len(student.get('subjects',[]))*3))
    career_exploration=78 if len(recs)>=3 else 55
    roadmap_progress=int(round(completed/total_items*100)) if total_items > 0 else 0
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
    roadmap=generate_roadmaps(student, recs[:5])
    RECOMMENDATIONS[student['id']]=recs
    ROADMAPS[student['id']]=roadmap
    summary=await personalize_with_gemini(student,recs)
    _persist_derived(student['id'], user_id)
    return {'recommendations':recs,'ai_summary':summary}

@router.get('/assessment/questions')
def assessment_questions(user_id: Annotated[str, Depends(require_user)]):
    student = _get_owned_student(user_id)
    interests = list(set(student.get('interests', [])))
    
    # We expect up to 3 interests. The user wants exactly 5 questions per interest.
    pool = list_assessment_questions(interests)
    
    if not pool:
        # Fallback if DB is unavailable
        pool = list_assessment_questions()
        
    grouped = {}
    for q in pool:
        # Supabase returned domain, but old structure used interest. We handle both.
        domain = q.get('domain') or q.get('interest', 'General')
        grouped.setdefault(domain, []).append(q)
        
    questions = []
    for interest in interests:
        group = grouped.get(interest, [])
        random.shuffle(group)
        # Select exactly 5 per domain
        questions.extend(group[:5])
        
    # If we somehow don't have 15 (e.g. fewer domains or fewer questions in DB), fill remainder
    if len(questions) < 15:
        remainder = [q for group in grouped.values() for q in group if q not in questions]
        random.shuffle(remainder)
        questions.extend(remainder[:15-len(questions)])
        
    random.shuffle(questions)
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
    
    student = _get_owned_student(user_id)
    for suggestion in attempt.get('stream_suggestions', []):
        if 'explore_subjects' not in suggestion:
            focus = suggestion.get('focus_subjects', [])
            suggestion['explore_subjects'] = explore_subjects_for_stream(student, suggestion['stream_id'], focus)

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
    result = analyze_answers(question_ids, answers, student.get('interests', []), interest_stream_scores, interest_suggestions, questions, profile=student)
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
        ROADMAPS[student_id]=generate_roadmaps(student, recs[:5])
        _persist_derived(student_id, user_id)
    return ROADMAPS[student_id][:5]

@router.post('/students/me/roadmap/{item_id}/complete')
def complete(item_id:str, user_id: Annotated[str, Depends(require_user)]):
    student=_get_owned_student(user_id)
    career_roadmaps=ROADMAPS.get(student['id'],[])
    
    item = None
    for career_rm in career_roadmaps:
        for rm_item in career_rm['items']:
            if rm_item['id'] == item_id:
                item = rm_item
                break
        if item:
            break
            
    if not item: raise HTTPException(404,'Roadmap item not found')
    item['completed']=True
    _persist_derived(student['id'], user_id)
    return item

RESOURCE_MAPPING = {
    "computer-science": ["Programming", "Computer Science", "Data & AI"],
    "data-science": ["Mathematics", "Data & AI", "Programming", "Computer Science"],
    "product-management": ["Business", "Programming", "Design"],
    "finance": ["Mathematics", "Business"],
    "ux-design": ["Design", "Computer Science"],
    "law": ["Business"],
    "medicine": ["Mathematics", "Science"],
    "psychology": ["Business"]
}

@router.get('/resources')
def resources(user_id: Annotated[str, Depends(require_user)]):
    student = _get_owned_student(user_id)
    recs = RECOMMENDATIONS.get(student['id'], [])
    if not recs:
        recs = score_profile(student)
        RECOMMENDATIONS[student['id']] = recs
        
    all_resources = list_resources()
    segmented_resources = []
    
    for rec in recs[:5]:
        career_id = rec.get('career_id')
        career = rec.get('career')
        categories = RESOURCE_MAPPING.get(career_id, [])
        career_resources = [r for r in all_resources if r['category'] in categories]
        if not career_resources:
            career_resources = all_resources[:2] # Fallback if no specific match
        
        segmented_resources.append({
            "career_id": career_id,
            "career": career,
            "resources": career_resources
        })
        
    return segmented_resources

@router.get('/colleges')
def colleges(user_id: Annotated[str, Depends(require_user)]): return list_colleges()

@router.post('/college-predict')
def college_predict(payload:CollegePredictRequest, user_id: Annotated[str, Depends(require_user)]):
    results=[c for c in list_colleges() if c['cutoff_percentile'] <= payload.percentile+8]
    if payload.branch: results=[c for c in results if payload.branch.lower() in c['branch'].lower()] or results
    if payload.city: results=[c for c in results if payload.city.lower() in c['city'].lower()] or results
    return sorted(results,key=lambda c:abs(payload.percentile-c['cutoff_percentile']))[:6]

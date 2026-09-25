from __future__ import annotations

from collections import defaultdict
from math import sqrt
from typing import Any

from ..data.questions import INTEREST_STREAMS, QUESTIONS_BY_ID
from .career_engine import focus_subjects_for_stream, explore_subjects_for_stream

STREAM_LABELS = {"science": "Science", "commerce": "Commerce", "arts": "Arts / Humanities"}


def _normalize(scores: dict[str, float]) -> dict[str, float]:
    total = sum(max(v, 0.0) for v in scores.values()) or 1.0
    return {k: round(max(v, 0.0) / total, 4) for k, v in scores.items()}


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = sqrt(sum(a.get(k, 0.0) ** 2 for k in keys))
    nb = sqrt(sum(b.get(k, 0.0) ** 2 for k in keys))
    if not na or not nb:
        return 0.0
    return max(0.0, min(1.0, dot / (na * nb)))


def _classification(alignment: float) -> str:
    if alignment >= 0.78:
        return "strong_match"
    if alignment >= 0.57:
        return "partial_match"
    return "not_fully_match"


def _dedupe_streams(candidates: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    seen = set()
    out = []
    for item in candidates:
        if item["stream_id"] in seen:
            continue
        seen.add(item["stream_id"])
        out.append(item)
        if len(out) == count:
            break
    return out


def analyze_answers(question_ids: list[str], answers: dict[str, str], interests: list[str], interest_stream_scores: dict[str, float], interest_stream_suggestions: list[dict[str, Any]], questions: list[dict[str, Any]], profile: dict | None = None) -> dict[str, Any]:
    stream_scores = defaultdict(float)
    answered = 0
    questions_by_id = {q["id"]: q for q in questions}
    
    # Archetype to stream mapping based on old ARCHETYPES
    archetypes = {
        "A": {"science": 6.0, "commerce": 0.8, "arts": 0.4},
        "P": {"science": 0.8, "commerce": 6.0, "arts": 0.6},
        "C": {"science": 0.4, "commerce": 0.8, "arts": 6.0},
        "I": {"science": 2.2, "commerce": 2.2, "arts": 2.2},
    }

    for qid in question_ids:
        question = questions_by_id.get(qid)
        if not question:
            continue
        option_id = answers.get(qid)
        if not option_id:
            continue
            
        answered += 1
        
        # New DB format handling
        if "scenario" in question:
            if option_id in archetypes:
                for stream, value in archetypes[option_id].items():
                    stream_scores[stream] += value
        else:
            # Old format
            option = next((x for x in question.get("options", []) if x["id"] == option_id), None)
            if option and "scores" in option:
                for stream, value in option["scores"].items():
                    stream_scores[stream] += value
                    
    answer_scores = _normalize(dict(stream_scores))
    interest_scores = _normalize(interest_stream_scores)
    alignment = _cosine(answer_scores, interest_scores)
    status = _classification(alignment)

    answer_ranked = sorted(answer_scores.items(), key=lambda x: x[1], reverse=True)
    profile = profile or {}
    answer_candidates = []
    for idx, (stream, score) in enumerate(answer_ranked):
        focus = focus_subjects_for_stream(profile, stream)
        answer_candidates.append({
            "stream_id": stream,
            "stream": STREAM_LABELS[stream],
            "source": "assessment",
            "tag": "Assessment pattern",
            "focus_subjects": focus,
            "explore_subjects": explore_subjects_for_stream(profile, stream, focus),
            "match_score": round(score * 100),
            "recommendation_id": f"assessment-{stream}-{idx}",
        })
    interest_candidates = []
    for idx, item in enumerate(interest_stream_suggestions):
        item = dict(item)
        item["source"] = "interest"
        item["tag"] = None
        item.setdefault("recommendation_id", f"interest-{item['stream_id']}-{idx}")
        focus = focus_subjects_for_stream(profile, item["stream_id"])
        item.setdefault("focus_subjects", focus)
        item.setdefault("explore_subjects", explore_subjects_for_stream(profile, item["stream_id"], focus))
        interest_candidates.append(item)

    if status == "strong_match":
        suggestions = interest_candidates[:3]
    elif status == "partial_match":
        suggestions = answer_candidates[:1] + interest_candidates[:2]
    else:
        suggestions = answer_candidates[:2] + interest_candidates[:2]

    return {
        "status": status,
        "alignment_score": round(alignment * 100),
        "answered_questions": answered,
        "total_questions": len(question_ids),
        "answer_stream_scores": answer_scores,
        "interest_stream_scores": interest_scores,
        "stream_suggestions": suggestions,
        "message": {
            "strong_match": "Your answering pattern aligns strongly with the interests you entered.",
            "partial_match": "Your answering pattern partially aligns with the interests you entered, so we are balancing both signals.",
            "not_fully_match": "Your answering pattern differs from some of the interests you entered, so we are broadening the stream options rather than ruling anything out.",
        }[status],
    }


def serialize_question(question: dict[str, Any]) -> dict[str, Any]:
    if "scenario" in question:
        return {
            "id": question["id"],
            "interest": question["domain"],
            "dimension": "General",
            "question": question["scenario"],
            "options": [
                {"id": "A", "text": question["option_a"]},
                {"id": "P", "text": question["option_p"]},
                {"id": "C", "text": question["option_c"]},
                {"id": "I", "text": question["option_i"]},
            ],
        }
    return {
        "id": question["id"],
        "interest": question["interest"],
        "dimension": question["dimension"],
        "question": question["question"],
        "options": [{"id": o["id"], "text": o["text"]} for o in question["options"]],
    }

from __future__ import annotations

from collections import defaultdict
from math import sqrt
from typing import Any

from ..data.questions import INTEREST_STREAMS, QUESTIONS_BY_ID
from .career_engine import focus_subjects_for_stream

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


def analyze_answers(question_ids: list[str], answers: dict[str, str], interests: list[str], interest_stream_scores: dict[str, float], interest_stream_suggestions: list[dict[str, Any]], profile: dict | None = None) -> dict[str, Any]:
    stream_scores = defaultdict(float)
    answered = 0
    for qid in question_ids:
        question = QUESTIONS_BY_ID.get(qid)
        if not question:
            continue
        option_id = answers.get(qid)
        option = next((x for x in question["options"] if x["id"] == option_id), None)
        if not option:
            continue
        answered += 1
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
        answer_candidates.append({
            "stream_id": stream,
            "stream": STREAM_LABELS[stream],
            "source": "assessment",
            "tag": "Assessment pattern",
            "focus_subjects": focus_subjects_for_stream(profile, stream),
            "match_score": round(score * 100),
            "recommendation_id": f"assessment-{stream}-{idx}",
        })
    interest_candidates = []
    for idx, item in enumerate(interest_stream_suggestions):
        item = dict(item)
        item["source"] = "interest"
        item["tag"] = None
        item.setdefault("recommendation_id", f"interest-{item['stream_id']}-{idx}")
        item.setdefault("focus_subjects", focus_subjects_for_stream(profile, item["stream_id"]))
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
    return {
        "id": question["id"],
        "interest": question["interest"],
        "dimension": question["dimension"],
        "question": question["question"],
        "options": [{"id": o["id"], "text": o["text"]} for o in question["options"]],
    }

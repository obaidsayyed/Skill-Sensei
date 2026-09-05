from collections import defaultdict
from ..data.careers import CAREERS

KEYWORDS = {
    "subject": {"Mathematics": {"computer-science":14,"data-science":15,"finance":12,"product-management":5},"Science": {"computer-science":8,"data-science":8,"medicine":16,"psychology":4},"Computer Science": {"computer-science":18,"data-science":14,"product-management":7},"English": {"law":10,"product-management":8,"ux-design":8,"psychology":6},"Social Science": {"law":8,"psychology":10,"product-management":7},"Economics": {"finance":15,"product-management":8,"law":5},"Accountancy": {"finance":18}},
    "interest": {"Technology":{"computer-science":18,"data-science":14,"product-management":10},"Business":{"finance":15,"product-management":15},"Design":{"ux-design":18,"product-management":6},"Finance":{"finance":20,"data-science":5},"Science":{"medicine":12,"data-science":9},"Law":{"law":20},"Healthcare":{"medicine":20,"psychology":7},"Psychology":{"psychology":18},"Media":{"ux-design":7,"product-management":5},"Entrepreneurship":{"product-management":14,"finance":7}},
    "strength": {"Logical reasoning":{"computer-science":11,"data-science":10,"law":8,"finance":6},"Communication":{"product-management":10,"law":10,"ux-design":7,"psychology":8},"Creativity":{"ux-design":13,"product-management":8},"Problem solving":{"computer-science":10,"data-science":10,"product-management":9,"medicine":6},"Mathematics":{"computer-science":9,"data-science":12,"finance":10},"Leadership":{"product-management":12,"finance":5},"Research":{"data-science":9,"law":9,"psychology":9,"medicine":8},"Empathy":{"psychology":12,"medicine":9,"ux-design":8},"Attention to detail":{"data-science":9,"finance":10,"law":9,"medicine":10}},
    "style": {"Building things":{"computer-science":8,"ux-design":8,"product-management":5},"Analyzing information":{"data-science":10,"finance":10,"law":7},"Working with people":{"psychology":10,"law":7,"product-management":8,"medicine":8},"Leading teams":{"product-management":12},"Creating visually":{"ux-design":13},"Explaining ideas":{"law":8,"product-management":10,"psychology":7},"Working independently":{"computer-science":7,"data-science":8,"finance":6,"research":5}}
}

def score_profile(profile: dict) -> list[dict]:
    totals=defaultdict(float)
    for subject in profile.get("subjects",[]):
        for cid,pts in KEYWORDS["subject"].get(subject,{}).items(): totals[cid]+=pts
    for interest in profile.get("interests",[]):
        for cid,pts in KEYWORDS["interest"].get(interest,{}).items(): totals[cid]+=pts
    for strength in profile.get("strengths",[]):
        for cid,pts in KEYWORDS["strength"].get(strength,{}).items(): totals[cid]+=pts
    for style in profile.get("work_styles",[]):
        for cid,pts in KEYWORDS["style"].get(style,{}).items(): totals[cid]+=pts
    for career in CAREERS: totals[career["id"]] += 3
    max_score=max(totals.values() or [1]); ranked=[]
    for career in CAREERS:
        raw=totals[career["id"]]
        pct=int(round(58+(raw/max_score)*40)) if max_score else 60
        pct=max(55,min(98,pct))
        ranked.append((pct,career))
    ranked.sort(key=lambda x:x[0], reverse=True)
    result=[]
    for pct,c in ranked[:5]:
        matched=[]
        # Explain from selected inputs without pretending the score is a scientific psychometric measurement.
        for item in profile.get("interests",[]):
            if item in c["name"] or item in c["domain"] or item in c["description"]: matched.append(f"Your interest in {item.lower()} aligns with this path.")
        if not matched:
            if c["skills"] and profile.get("strengths"): matched.append(f"Your {profile['strengths'][0].lower()} strength maps well to the skills used here.")
            elif profile.get("subjects"): matched.append(f"Your {profile['subjects'][0]} background is relevant to this direction.")
        why=matched[:2] or [f"This path overlaps with several of the signals in your current profile."]
        skill_gaps=[s for s in c["skills"] if s.lower() not in ' '.join(profile.get("strengths",[])).lower()][:3]
        result.append({"career_id":c["id"],"career":c["name"],"domain":c["domain"],"match_score":pct,"confidence":"High" if pct>=88 else "Medium" if pct>=75 else "Low","why_match":why,"skill_gaps":skill_gaps,"next_steps":[f"Explore what a typical {c['name']} workday looks like",f"Review the skills needed for {c['name']}",f"Add one beginner-level {c['domain'].lower()} learning milestone to your roadmap"]})
    return result


CAREER_STREAM = {
    "computer-science": "science",
    "data-science": "science",
    "medicine": "science",
    "finance": "commerce",
    "product-management": "commerce",
    "ux-design": "arts",
    "law": "arts",
    "psychology": "arts",
}

STREAM_LABELS = {"science": "Science", "commerce": "Commerce", "arts": "Arts / Humanities"}

def score_streams_from_profile(profile: dict) -> list[dict]:
    career_scores = score_profile(profile)
    totals = {"science": 55.0, "commerce": 55.0, "arts": 55.0}
    counts = {"science": 1, "commerce": 1, "arts": 1}
    for rec in career_scores:
        stream = CAREER_STREAM.get(rec["career_id"])
        if stream:
            totals[stream] += rec["match_score"]
            counts[stream] += 1
    ranked = sorted(totals.items(), key=lambda x: x[1] / counts[x[0]], reverse=True)
    return [
        {"stream_id": sid, "stream": STREAM_LABELS[sid], "match_score": int(round(score / counts[sid])), "source": "interest", "tag": None, "focus_subjects": _focus_subjects(profile, sid, source="interest")}
        for sid, score in ranked
    ]

def _focus_subjects(profile: dict, stream_id: str, source: str = "interest") -> list[str]:
    interests = set(profile.get("interests", []))
    subjects = set(profile.get("subjects", []))
    if stream_id == "science":
        if "Computer Science" in subjects or "Technology" in interests or "Data Science" in interests:
            return ["Mathematics", "Physics", "Computer Science"]
        if "Healthcare" in interests or "Science" in interests:
            return ["Physics", "Chemistry", "Biology"]
        return ["Mathematics", "Physics", "Chemistry"]
    if stream_id == "commerce":
        if {"Finance", "Business", "Entrepreneurship"} & interests:
            return ["Accountancy", "Economics", "Mathematics"]
        return ["Accountancy", "Economics", "Business Studies"]
    if "Law" in interests:
        return ["English", "Political Science", "History"]
    if "Psychology" in interests or "Healthcare" in interests:
        return ["Psychology", "English", "Social Science"]
    if {"Design", "Media"} & interests:
        return ["English", "Design / Media", "Social Science"]
    return ["English", "Social Science", "Economics"]


def focus_subjects_for_stream(profile: dict, stream_id: str) -> list[str]:
    return _focus_subjects(profile, stream_id, source="assessment")

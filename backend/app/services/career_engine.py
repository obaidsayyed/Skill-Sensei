from collections import defaultdict
from .store import list_careers

STREAM_LABELS = {"science": "Science", "commerce": "Commerce", "arts": "Arts / Humanities"}

def score_profile(profile: dict) -> list[dict]:
    careers = list_careers()
    totals = defaultdict(float)
    
    # Generic scoring logic matching profile to career fields
    student_subjects = [s.lower() for s in profile.get("subjects", [])]
    student_interests = [i.lower() for i in profile.get("interests", [])]
    student_strengths = [s.lower() for s in profile.get("strengths", [])]
    student_styles = [s.lower() for s in profile.get("work_styles", [])]
    
    for c in careers:
        # Base score
        totals[c["id"]] += 3
        
        # Match subjects
        c_subjects = [s.lower() for s in c.get("subjects", [])]
        for s in student_subjects:
            if s in c_subjects:
                totals[c["id"]] += 15
            elif any(s in cs or cs in s for cs in c_subjects):
                totals[c["id"]] += 8
                
        # Match interests to domain and description
        c_domain = c.get("domain", "").lower()
        c_desc = c.get("description", "").lower()
        for i in student_interests:
            if i in c_domain:
                totals[c["id"]] += 18
            elif i in c_desc or i in c.get("name", "").lower():
                totals[c["id"]] += 12
                
        # Match strengths to skills
        c_skills = [s.lower() for s in c.get("skills", [])]
        for s in student_strengths:
            if s in c_skills:
                totals[c["id"]] += 12
            elif any(s in cs or cs in s for cs in c_skills):
                totals[c["id"]] += 6
                
        # Match work styles
        c_styles = [s.lower() for s in c.get("work_style", [])]
        for s in student_styles:
            if s in c_styles:
                totals[c["id"]] += 10
            elif any(s in cs or cs in s for cs in c_styles):
                totals[c["id"]] += 5

    max_score = max(totals.values() or [1])
    ranked = []
    for c in careers:
        raw = totals[c["id"]]
        pct = int(round(58 + (raw / max_score) * 40)) if max_score else 60
        pct = max(55, min(98, pct))
        ranked.append((pct, c))
        
    ranked.sort(key=lambda x: x[0], reverse=True)
    result = []
    
    # Return top 5
    for pct, c in ranked[:5]:
        matched = []
        for item in profile.get("interests", []):
            if item.lower() in c["name"].lower() or item.lower() in c["domain"].lower() or item.lower() in c["description"].lower():
                matched.append(f"Your interest in {item.lower()} aligns with this path.")
        if not matched:
            if c.get("skills") and profile.get("strengths"):
                matched.append(f"Your {profile['strengths'][0].lower()} strength maps well to the skills used here.")
            elif profile.get("subjects"):
                matched.append(f"Your {profile['subjects'][0]} background is relevant to this direction.")
                
        why = matched[:2] or [f"This path overlaps with several of the signals in your current profile."]
        skill_gaps = [s for s in c.get("skills", []) if s.lower() not in ' '.join(profile.get("strengths", [])).lower()][:3]
        
        result.append({
            "career_id": c["id"],
            "career": c["name"],
            "domain": c["domain"],
            "match_score": pct,
            "confidence": "High" if pct >= 88 else "Medium" if pct >= 75 else "Low",
            "why_match": why,
            "skill_gaps": skill_gaps,
            "next_steps": [
                f"Explore what a typical {c['name']} workday looks like",
                f"Review the skills needed for {c['name']}",
                f"Add one beginner-level {c['domain'].lower()} learning milestone to your roadmap"
            ]
        })
    return result

def score_streams_from_profile(profile: dict) -> list[dict]:
    # Determine stream dynamically based on top careers
    career_scores = score_profile(profile)
    totals = {"science": 55.0, "commerce": 55.0, "arts": 55.0}
    counts = {"science": 1, "commerce": 1, "arts": 1}
    
    for rec in career_scores:
        domain = rec.get("domain", "").lower()
        if "technology" in domain or "science" in domain or "healthcare" in domain:
            totals["science"] += rec["match_score"]
            counts["science"] += 1
        elif "business" in domain or "finance" in domain:
            totals["commerce"] += rec["match_score"]
            counts["commerce"] += 1
        else:
            totals["arts"] += rec["match_score"]
            counts["arts"] += 1
            
    ranked = sorted(totals.items(), key=lambda x: x[1] / counts[x[0]], reverse=True)
    return [
        {
            "stream_id": sid, 
            "stream": STREAM_LABELS[sid], 
            "match_score": int(round(score / counts[sid])), 
            "source": "interest", 
            "tag": None, 
            "focus_subjects": _focus_subjects(profile, sid, source="interest")
        }
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

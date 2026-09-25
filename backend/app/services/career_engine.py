from collections import defaultdict
from sentence_transformers import SentenceTransformer
from .store import list_careers, match_career_embeddings, match_stream_embeddings, get_career

STREAM_LABELS = {"science": "Science", "commerce": "Commerce", "arts": "Arts / Humanities"}

# Load the model globally so it's only loaded once when the server starts
model = SentenceTransformer('BAAI/bge-large-en-v1.5')

def _get_alignment_label(sim: float) -> str:
    if sim >= 0.70: return "Strong alignment"
    if sim >= 0.60: return "Good alignment"
    if sim >= 0.50: return "Possible fit"
    return "Explore further"

def score_profile(profile: dict) -> list[dict]:
    # 1. Convert profile to a structured string for embedding
    parts = [
        f"Interests: {', '.join(profile.get('interests', []))}",
        f"Preferred activities: {', '.join(profile.get('strengths', []))}",
        f"Subjects: {', '.join(profile.get('subjects', []))}",
        f"Work style: {', '.join(profile.get('work_styles', []))}"
    ]
    query_text = "\n".join(parts)
    
    # 2. Generate embedding
    query_embedding = model.encode(query_text).tolist()
    
    # 3. Match via Supabase RPC
    matches = match_career_embeddings(query_embedding, match_count=70)
    
    result = []
    if not matches:
        print("Warning: No matches from Supabase RPC, falling back to empty list")
        return []

    for i, m in enumerate(matches[:5]):
        c = get_career(m['career_id'])
        if not c: continue
        
        sim = m['similarity']
        
        matched = []
        for item in profile.get("interests", []):
            if item.lower() in c["name"].lower() or item.lower() in c["domain"].lower() or item.lower() in c.get("description", "").lower():
                matched.append(f"Your interest in {item.lower()} aligns with this path.")
        if not matched:
            if c.get("skills") and profile.get("strengths"):
                matched.append(f"Your {profile['strengths'][0].lower()} strength maps well to the skills used here.")
            elif profile.get("subjects"):
                matched.append(f"Your {profile['subjects'][0]} background is relevant to this direction.")
                
        why = matched[:2] or [f"This path strongly aligns with your overall semantic profile."]
        skill_gaps = [s for s in c.get("skills", []) if s.lower() not in ' '.join(profile.get("strengths", [])).lower()][:3]
        
        result.append({
            "career_id": c["id"],
            "career": c["name"],
            "domain": c["domain"],
            "match_score": int(round(sim * 100)), # Frontend uses this as a 0-100 percentage
            "alignment_label": _get_alignment_label(sim),
            "confidence": "High" if sim >= 0.70 else "Medium" if sim >= 0.60 else "Low",
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
    # 1. Embed structured profile
    parts = [
        f"Interests: {', '.join(profile.get('interests', []))}",
        f"Preferred activities: {', '.join(profile.get('strengths', []))}",
        f"Subjects: {', '.join(profile.get('subjects', []))}",
        f"Work style: {', '.join(profile.get('work_styles', []))}"
    ]
    query_text = "\n".join(parts)
    query_embedding = model.encode(query_text).tolist()
    
    # 2. Get direct stream embeddings similarity
    stream_matches = match_stream_embeddings(query_embedding, match_count=3)
    stream_sims = {m['stream_id']: m['similarity'] for m in stream_matches} if stream_matches else {}
    
    # 3. Get career evidence similarity
    career_matches = match_career_embeddings(query_embedding, match_count=70)
    
    stream_career_scores = {"science": [], "commerce": [], "arts": []}
    if career_matches:
        for m in career_matches:
            c = get_career(m['career_id'])
            if not c: continue
            domain = c.get("domain", "").lower()
            if "technology" in domain or "science" in domain or "healthcare" in domain:
                stream_career_scores["science"].append(m['similarity'])
            elif "business" in domain or "finance" in domain:
                stream_career_scores["commerce"].append(m['similarity'])
            else:
                stream_career_scores["arts"].append(m['similarity'])
                
    final_scores = {}
    for sid, scores in stream_career_scores.items():
        if not scores:
            final_scores[sid] = stream_sims.get(sid, 0.0)
            continue
            
        # Top-K Weighted Score
        scores = sorted(scores, reverse=True)
        top_k = scores[:3]
        weights = [1.0, 0.8, 0.6]
        
        weighted_sum = sum(s * w for s, w in zip(top_k, weights[:len(top_k)]))
        weight_total = sum(weights[:len(top_k)])
        top_k_score = weighted_sum / weight_total if weight_total > 0 else 0
        
        # Consistency
        top_5 = scores[:5]
        consistency = sum(top_5) / len(top_5) if top_5 else 0
        
        # Career Evidence Score
        career_evidence = (0.75 * top_k_score) + (0.25 * consistency)
        
        # Final combine: 50% Direct Stream Similarity, 50% Career Evidence
        direct_sim = stream_sims.get(sid, 0.0)
        final_scores[sid] = (0.5 * direct_sim) + (0.5 * career_evidence)
            
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    
    return [
        {
            "stream_id": sid, 
            "stream": STREAM_LABELS[sid], 
            "match_score": int(round(score * 100)),
            "alignment_label": _get_alignment_label(score),
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

def explore_subjects_for_stream(profile: dict, stream_id: str, focus_subjects: list[str]) -> list[str]:
    all_extras = {
        "science": ["Biology", "Computer Science", "Information Technology", "Electronics", "Mathematics", "Physics", "Chemistry"],
        "commerce": ["Business Studies", "Mathematics", "Statistics", "Finance", "Economics", "Accountancy"],
        "arts": ["Psychology", "Sociology", "History", "Political Science", "Geography", "Languages"]
    }
    
    interests = set(i.lower() for i in profile.get("interests", []))
    extras_for_stream = all_extras.get(stream_id, ["English", "Languages", "Physical Education"])
    
    available = [s for s in extras_for_stream if s not in focus_subjects]
    
    ranked = []
    for s in available:
        score = 0
        if s.lower() in interests:
            score += 10
        elif "technology" in interests and s in ["Computer Science", "Information Technology", "Electronics"]:
            score += 5
        elif "finance" in interests and s in ["Statistics", "Finance"]:
            score += 5
        elif "business" in interests and s in ["Business Studies"]:
            score += 5
        elif "science" in interests and s in ["Biology", "Chemistry", "Physics"]:
            score += 5
        ranked.append((score, s))
        
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [s for score, s in ranked[:2]]

def generate_roadmaps(profile: dict, recommendations: list[dict]) -> list[dict]:
    roadmaps = []
    
    if not recommendations:
        return roadmaps

    from .store import get_career

    for index, rec in enumerate(recommendations):
        career_name = rec.get("career", "your strongest career direction")
        career_id = rec.get("career_id", f"c{index}")
        
        career_details = get_career(career_id)
        if not career_details:
            continue
            
        sequence = career_details.get("roadmap_sequence", [])
        
        items = []
        for i, step in enumerate(sequence):
            horizon = "This month" if i < 2 else "Next 3 months" if i < 5 else "Later"
            items.append((horizon, step.get("title", ""), step.get("description", ""), "skill"))
            
        roadmap_items = [{"id":f"{career_id}-r{i+1}","horizon":h,"title":t,"description":d,"type":typ,"completed":False} for i,(h,t,d,typ) in enumerate(items)]
        roadmaps.append({
            "career_id": career_id,
            "career": career_name,
            "items": roadmap_items
        })
        
    return roadmaps

import sys
import httpx
import os

# Ensure the backend directory is in the python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.store import _supabase_enabled, _supabase_endpoint, _supabase_headers, _save_row, _student_from_row
from app.services.career_engine import score_profile
from app.services.roadmap_service import generate_roadmaps

def migrate():
    if not _supabase_enabled():
        print("Supabase is not enabled. Nothing to migrate.")
        return
        
    url = f"{_supabase_endpoint('students')}?select=*"
    with httpx.Client(timeout=10) as client:
        response = client.get(url, headers=_supabase_headers())
    
    if response.status_code != 200:
        print(f"Error fetching students: {response.text}")
        return
        
    rows = response.json()
    print(f"Found {len(rows)} students to migrate.")
    
    for row in rows:
        student = _student_from_row(row)
        user_id = row.get("user_id")
        if not user_id:
            continue
            
        print(f"Migrating student {student.get('name', 'Unknown')} ({user_id})...")
        
        # 1. Regenerate recommendations
        recs = score_profile(student)
        
        # 2. Regenerate roadmaps
        roadmap = generate_roadmaps(student, recs[:5])
        
        # 3. Update row
        row["recommendations"] = recs
        row["roadmap"] = roadmap
        
        # 4. Save using the built-in store method (which merges on conflict)
        _save_row(row)
        
    print("Migration complete!")

if __name__ == "__main__":
    migrate()

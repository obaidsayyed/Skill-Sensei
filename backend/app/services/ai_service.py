import json
import httpx
from ..core.config import settings

async def personalize_with_gemini(profile: dict, recommendations: list[dict]) -> str:
    if not settings.gemini_api_key:
        return "Your current recommendations are based on the signals in your profile. Treat these as directions to explore, not permanent labels."
    prompt = {
      "task":"Write a concise student-friendly career analysis summary for a dashboard.",
      "student":{"class":profile.get("class_level"),"board":profile.get("board"),"interests":profile.get("interests"),"strengths":profile.get("strengths"),"goals":profile.get("goals")},
      "recommendations":[{"career":r["career"],"score":r["match_score"],"gaps":r["skill_gaps"]} for r in recommendations[:3]],
      "rules":["Do not claim scientific certainty or make a life-determining diagnosis.","Do not invent statistics.","Keep under 90 words."]
    }
    url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.gemini_api_key}"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp=await client.post(url,json={"contents":[{"parts":[{"text":json.dumps(prompt)}]}]})
            resp.raise_for_status(); data=resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return "Your current recommendations are based on the signals in your profile. Treat these as directions to explore, not permanent labels."

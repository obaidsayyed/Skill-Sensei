from __future__ import annotations

from copy import deepcopy

from ..data.resources import RESOURCES

# Curated resource sets per career. These are intentionally deterministic so
# each recommended path has its own learning library without requiring an LLM.
CAREER_RESOURCE_IDS: dict[str, list[str]] = {
    "computer-science": ["cs50", "python-freecodecamp", "khan-algebra"],
    "data-science": ["python-freecodecamp", "google-data", "khan-algebra", "data-statistics"],
    "product-management": ["product-foundations", "product-discovery", "mit-business"],
    "finance": ["finance-khan", "finance-accounting", "mit-business"],
    "ux-design": ["figma-learn", "ux-research", "design-thinking"],
    "law": ["law-legal-reasoning", "law-india-basics", "law-research"],
    "medicine": ["biology-khan", "chemistry-khan", "healthcare-science"],
    "psychology": ["psychology-khan", "psychology-research", "social-science-research"],
}

def resources_for_career(career_id: str) -> list[dict]:
    ids = CAREER_RESOURCE_IDS.get(career_id, [])
    by_id = {r["id"]: r for r in RESOURCES}
    selected = [deepcopy(by_id[rid]) for rid in ids if rid in by_id]
    if selected:
        return selected
    return deepcopy(RESOURCES[:4])

def generate_roadmap(profile: dict, top_career: dict | None) -> list[dict]:
    cls=profile.get("class_level",10); career=top_career.get("career","your strongest career direction") if top_career else "your strongest career direction"
    if cls==10:
        items=[
          ("Now","Understand your top career directions",f"Review why SkillSensei currently sees {career} as a strong direction.","explore"),
          ("Now","Review stream implications", "Compare which Class 11 stream keeps your strongest directions open.","academic"),
          ("Next 3 months","Strengthen your strongest subjects", "Pick two subjects connected to your leading options and build consistency.","academic"),
          ("Next 3 months","Explore one career deeply", f"Learn about roles, education routes, and day-to-day work in {career}.","explore"),
          ("Next 6 months","Start a foundational skill", "Choose one beginner-friendly skill aligned with your strongest direction.","skill"),
          ("Later","Review and update your profile", "Refresh interests and goals before locking your stream decision.","explore")]
    elif cls==11:
        items=[
          ("Now","Confirm your target direction",f"Keep {career} as a working hypothesis and validate it against your interests.","explore"),
          ("Now","Map your skill gaps","Identify two or three practical skills that school coursework does not fully cover.","skill"),
          ("Next 3 months","Build a first practical project","Create a small project that applies one target skill to a real problem.","project"),
          ("Next 6 months","Build evidence of learning","Document your project, reflections, and progress in a simple portfolio.","project"),
          ("Later","Research college routes", "Compare degree routes, entrance exams, and realistic alternatives.","admission")]
    else:
        items=[
          ("Now","Finalize target career options",f"Keep {career} as one of your leading options and compare it with your alternatives.","explore"),
          ("Now","Map entrance requirements","Record the exams, subjects, and academic requirements for your target route.","admission"),
          ("Next 3 months","Build a college shortlist","Create stretch, target, and safer options for your preferred course.","admission"),
          ("Next 3 months","Track application milestones","Keep a checklist for forms, documents, deadlines, and admission rounds.","admission"),
          ("Later","Create Plan B and Plan C","Choose credible alternatives that still move you toward related career outcomes.","admission")]
    return [{"id":f"r{i+1}","horizon":h,"title":t,"description":d,"type":typ,"completed":False} for i,(h,t,d,typ) in enumerate(items)]

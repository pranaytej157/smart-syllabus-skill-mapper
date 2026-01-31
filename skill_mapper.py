# skill_mapper.py

def map_skills_to_roles(ai_skills, skill_taxonomy):
    """Map extracted skills to roles. Case-insensitive matching."""
    ai_skills_lower = {s.lower() for s in (ai_skills or [])}
    mapping = {}
    for role, skills in skill_taxonomy.items():
        matched = [skill for skill in (skills or []) if skill.lower() in ai_skills_lower]
        missing = [skill for skill in (skills or []) if skill.lower() not in ai_skills_lower]
        mapping[role] = {"matched": matched, "missing": missing}
    return mapping

def generate_skill_roadmap(mapping):
    roadmap = {}
    for role, data in mapping.items():
        roadmap[role] = {}
        for skill in data["missing"]:
            roadmap[role][skill] = [
                f"Learn basics of {skill}",
                f"Take online tutorial/course for {skill}",
                f"Build mini project involving {skill}"
            ]
    return roadmap

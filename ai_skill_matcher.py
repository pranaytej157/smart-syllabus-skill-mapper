"""
AI Skill Agent: spontaneously maps user wording to taxonomy skills at scale.
No hardcoded synonyms – AI flexibly links any alternate/relative tags
(dbms, mysql, RDBMS → databases/SQL; programming, coding, DSA → Programming, DSA; etc.)
to all skills in the taxonomy from the attached data files.

Requires: OPENAI_API_KEY environment variable.
Fallback: taxonomy-based keyword matching when no API key.
"""
import os
import json
import re


def ai_detect_and_map_skills(
    syllabus_text: str,
    taxonomy_skills: list[str],
    role_skills: dict[str, list[str]] | None = None,
) -> list[str]:
    """
    AI agent: spontaneously detect skill-related concepts in user input and
    link them to taxonomy skills. Works for all taxonomy data at scale.
    Understands synonyms, abbreviations, alternate tags for any skill.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return []

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except ImportError:
        return []

    skills_list = list(sorted(set(taxonomy_skills)))
    skills_str = ", ".join(skills_list)

    role_context = ""
    if role_skills:
        role_lines = [f"- {role}: {', '.join(skills[:15])}{'...' if len(skills) > 15 else ''}" for role, skills in list(role_skills.items())[:25]]
        role_context = "\nROLE-SKILL CONTEXT (for reference):\n" + "\n".join(role_lines)

    prompt = f"""You are a skill mapping agent for a taxonomy of {len(skills_list)} skills. Read the user's syllabus/course text and spontaneously identify ANY skill-related concepts mentioned (technologies, tools, methods, domains, frameworks).
Then link each detected concept to one or more taxonomy skills below.

RULES:
- Use your full knowledge: synonyms, abbreviations, alternate tags, related terms for EVERY taxonomy skill.
- Map flexibly: dbms/mysql/postgresql/RDBMS → databases, SQL; programming/coding/DSA → Programming, DSA; ml/deep learning/neural nets → Machine Learning, ML; stats/analytics → statistics; excel/spreadsheets → Excel; git/version control → Git; etc. Apply this spontaneity to ALL {len(skills_list)} skills.
- User may share relative or alternate tags – link them to taxonomy skills.
- Return ONLY taxonomy skill names below – no new names.

TAXONOMY SKILLS:
{skills_str}
{role_context}

USER SYLLABUS TEXT:
{syllabus_text}

Return a JSON array of taxonomy skill names that are mentioned or implied. Use exact strings from the taxonomy list.
Example: ["databases", "SQL", "Programming", "DSA"]
Return [] if nothing matches. No explanation."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            parts = content.split("```")
            content = parts[1] if len(parts) > 1 else content
            if content.lower().startswith("json"):
                content = content[4:].strip()
        result = json.loads(content)
        if isinstance(result, list):
            taxonomy_lower = {s.lower(): s for s in taxonomy_skills}
            return list({taxonomy_lower[r.lower()] for r in result if r and isinstance(r, str) and r.lower() in taxonomy_lower})
        return []
    except Exception:
        return []


def extract_skills_from_taxonomy_in_text(text: str, taxonomy_skills: list[str]) -> list[str]:
    """
    Fallback when no API key. Check which taxonomy skills appear in text.
    Uses taxonomy as the dynamic keyword source – no hardcoded list.
    """
    if not text or not taxonomy_skills:
        return []
    text_lower = text.lower()
    words = set(re.sub(r'[^\w\s]', ' ', text_lower).split())
    matched = []
    for skill in taxonomy_skills:
        s_lower = skill.lower()
        if len(s_lower) > 2 and s_lower in text_lower:
            matched.append(skill)
        elif s_lower in words:
            matched.append(skill)
        else:
            s_norm = re.sub(r'[^\w]', '', s_lower)
            text_no_spaces = re.sub(r'\s', '', re.sub(r'[^\w\s]', ' ', text_lower))
            if s_norm and len(s_norm) > 2 and s_norm in text_no_spaces:
                matched.append(skill)
    return list(set(matched))

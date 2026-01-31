import re
import pandas as pd


def _split_skills(skill_str):
    """Split skill string by comma, slash, + to get individual skills."""
    if not skill_str or not isinstance(skill_str, str):
        return []
    parts = re.split(r'[,/\+&]|(?:\s+and\s+)', skill_str, flags=re.IGNORECASE)
    return [s.strip() for s in parts if s.strip()]


def load_skill_taxonomy(file_path):
    """
    Load Excel containing Role -> Skills mapping.
    Returns a dictionary: {Role: [Skill1, Skill2, ...]}
    Supports comma/slash-separated skills in cells (e.g., "HTML, CSS, JavaScript").
    Column names are matched case-insensitively (Role/role, Skill/skill).
    """
    df = pd.read_excel(file_path)
    # Case-insensitive column lookup (Role/role, Skill/skill)
    cols = {str(c).lower(): c for c in df.columns}
    col_list = list(df.columns)
    role_col = cols.get('role', col_list[0] if col_list else None)
    skill_col = cols.get('skill', col_list[1] if len(col_list) > 1 else col_list[0])
    if role_col is None or skill_col is None:
        return {}
    skill_dict = {}
    for _, row in df.iterrows():
        role = row.get(role_col)
        skill_val = row.get(skill_col)
        if pd.notna(role) and pd.notna(skill_val):
            role = str(role).strip()
            skill_str = str(skill_val).strip()
            if role and skill_str:
                for skill in _split_skills(skill_str):
                    if skill and skill not in skill_dict.setdefault(role, []):
                        skill_dict[role].append(skill)
    return skill_dict

import re
import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "Python", "C++", "Java", "JavaScript", "HTML", "CSS", "React",
    "Node.js", "Flask", "FastAPI", "SQL", "Data Analysis",
    "Machine Learning", "Deep Learning", "NLP", "ML",
    "Data Visualization", "AI", "APIs", "Excel", "Git",
    "Programming", "DSA", "Statistics", "databases",
    "Linux", "cloud", "AWS", "Azure", "networking", "deployment",
    "Testing", "automation", "Figma", "UI design", "problem solving"
]

def preprocess_text(text):
    """
    Lowercase, remove extra spaces, punctuation.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def extract_skills_from_text(text):
    """
    Extract skills from syllabus text using keyword matching + NLP entities.
    Returns a list of skills found in the text.
    """
    text = preprocess_text(text)
    doc = nlp(text)

    candidates_lower = {ent.text.lower() for ent in doc.ents}  # Entities
    candidates_lower.update(token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"])

    words = set(text.split())  # Whole words only to avoid false matches (e.g. "c" in "css")

    def skill_in_text(skill_lower):
        """Check if skill appears in text. Use word boundaries to avoid false matches (e.g. 'c' in 'css')."""
        if skill_lower in text:
            return True
        norm = skill_lower.replace('.', '').replace('+', '').strip()
        return norm in words if norm else False

    matched_skills = [
        skill for skill in SKILL_KEYWORDS
        if skill_in_text(skill.lower()) or skill.lower() in candidates_lower
    ]

    return matched_skills

if __name__ == "__main__":
    sample_syllabus = """
    This course covers Python programming, Data Analysis, SQL, Machine Learning basics, and building APIs with Flask.
    """
    skills = extract_skills_from_text(sample_syllabus)
    print("Extracted Skills:", skills)

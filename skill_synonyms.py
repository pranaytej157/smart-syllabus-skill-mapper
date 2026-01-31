"""
Large-scale synonym/alias map: alternate tags → taxonomy skills.
Maps user wording (dbms, mysql, programming, coding, ml, etc.) to taxonomy skills
so users have flexibility without needing an API.
"""
import re

# Alternate terms → taxonomy skill names (must match data/skill_list.xlsx)
# Multiple alternates can map to same skill; one alternate can map to multiple skills
SKILL_ALIASES = {
    # Database & SQL
    "dbms": ["databases", "SQL"],
    "database management system": ["databases", "SQL"],
    "rdbms": ["databases", "SQL"],
    "mysql": ["databases", "SQL"],
    "postgresql": ["databases", "SQL"],
    "postgres": ["databases", "SQL"],
    "mongodb": ["databases"],
    "mongo": ["databases"],
    "nosql": ["databases"],
    "sql queries": ["SQL"],
    "sql": ["SQL"],
    "database": ["databases"],
    "databases": ["databases"],
    "oracle": ["Oracle knowledge"],
    "oracle db": ["Oracle knowledge"],
    # Programming & DSA
    "programming": ["Programming", "Programming basics"],
    "coding": ["Programming", "coding"],
    "software programming": ["Programming", "Programming basics"],
    "dsa": ["DSA"],
    "data structures": ["DSA", "Algorithms"],
    "algorithms": ["Algorithms"],
    "software development": ["Programming", "Full-cycle dev"],
    "software dev": ["Programming", "Full-cycle dev"],
    "low-level": ["Low-level programming"],
    "low level programming": ["Low-level programming"],
    "embedded systems": ["Embedded"],
    "embedded": ["Embedded"],
    "scripting": ["scripting"],
    # ML & AI
    "ml": ["ML", "ML models"],
    "machine learning": ["ML", "ML models"],
    "deep learning": ["ML", "ML models"],
    "neural nets": ["ML", "ML models"],
    "neural networks": ["ML", "ML models"],
    "ai": ["AI models", "AI prompting"],
    "artificial intelligence": ["AI models"],
    "nlp": ["Language processing"],
    "natural language processing": ["Language processing"],
    # Stats & Analytics
    "stats": ["statistics", "Math"],
    "statistics": ["statistics"],
    "analytics": ["statistics", "analysis"],
    "statistical analysis": ["statistics"],
    "data analysis": ["analysis", "statistics"],
    # Excel & Spreadsheets
    "excel": ["Excel"],
    "spreadsheets": ["Excel"],
    "xlsx": ["Excel"],
    "ms excel": ["Excel"],
    # Version control
    "git": ["Git"],
    "version control": ["Version control", "Git"],
    "github": ["Git", "Version control"],
    "gitlab": ["Git", "Version control"],
    # UI/UX
    "ui": ["UI design", "UI logic"],
    "ux": ["UI design"],
    "user interface": ["UI design"],
    "user experience": ["UI design"],
    "frontend design": ["UI design", "Frontend"],
    "figma": ["Figma"],
    "design tools": ["Figma", "Design thinking"],
    "prototyping": ["Figma"],
    # APIs & Backend
    "apis": ["APIs"],
    "rest": ["REST", "APIs"],
    "rest api": ["REST", "APIs", "API design"],
    "api design": ["API design"],
    "api integration": ["API integration"],
    "backend": ["Backend"],
    "backend development": ["Backend"],
    # Cloud
    "aws": ["AWS"],
    "amazon web services": ["AWS"],
    "ec2": ["AWS", "cloud"],
    "s3": ["AWS"],
    "azure": ["Azure"],
    "microsoft cloud": ["Azure"],
    "cloud": ["cloud"],
    "cloud computing": ["cloud"],
    # Linux & OS
    "linux": ["Linux"],
    "ubuntu": ["Linux"],
    "unix": ["Linux"],
    "os": ["OS concepts"],
    "operating system": ["OS concepts"],
    # Testing
    "testing": ["Testing"],
    "test automation": ["automation", "Testing techniques"],
    "selenium": ["Selenium", "Testing"],
    "qa": ["Testing", "Testing techniques"],
    "load testing": ["Load testing"],
    # Web
    "html": ["HTML"],
    "css": ["CSS"],
    "javascript": ["JavaScript", "JS"],
    "js": ["JS", "JavaScript"],
    "react": ["Rendering"],
    "frontend": ["Frontend"],
    "web": ["Web"],
    "web development": ["Web", "Frontend", "Backend"],
    # Big Data
    "hadoop": ["Hadoop"],
    "spark": ["Spark"],
    "big data": ["Hadoop", "Spark"],
    # Blockchain
    "blockchain": ["Blockchain concepts"],
    "ethereum": ["Blockchain concepts", "Solidity"],
    "solidity": ["Solidity"],
    "smart contracts": ["Blockchain concepts", "Solidity"],
    # Mobile
    "android": ["Android"],
    "kotlin": ["Android"],
    "ios": ["iOS"],
    "swift": ["Swift"],
    "mobile": ["Android", "iOS"],
    "mobile development": ["Android", "iOS"],
    # Security
    "security": ["security basics", "Cloud security"],
    "penetration testing": ["penetration testing"],
    "pentest": ["penetration testing"],
    "pen testing": ["penetration testing"],
    "cybersecurity": ["security basics", "Cloud security"],
    "vulnerability": ["exploitation", "penetration testing"],
    # DevOps
    "ci": ["CI"],
    "cd": ["CD"],
    "ci/cd": ["CI", "CD"],
    "devops": ["CI", "CD", "deployment"],
    "deployment": ["deployment"],
    "pipelines": ["pipelines"],
    # Unity & Game dev
    "unity": ["Unity"],
    "game dev": ["Unity", "3D concepts"],
    "game development": ["Unity", "3D concepts"],
    "3d": ["3D concepts", "3D virtual worlds"],
    "3d modeling": ["3D concepts"],
    "graphics": ["graphics"],
    # Data viz
    "data visualization": ["data visualization"],
    "visualization": ["data visualization"],
    "dashboards": ["dashboards"],
    # Other
    "networking": ["Networking", "networking"],
    "network": ["Networking", "networking"],
    "communication": ["Communication", "communication"],
    "collaboration": ["Collaboration"],
    "agile": ["Agile frameworks"],
    "scrum": ["Scrum practices"],
    "python": ["Python"],
    "java": ["Java"],
    "problem solving": ["problem solving"],
    "documentation": ["Documentation skills"],
    "etl": ["ETL"],
    "data transformation": ["Data transformation"],
    "system design": ["System design"],
    # Additional taxonomy coverage
    "requirements": ["Requirement analysis", "Requirement prioritization"],
    "scrum": ["Scrum practices"],
    "agile": ["Agile frameworks"],
    "figma": ["Figma"],
    "design thinking": ["Design thinking"],
    "troubleshooting": ["Troubleshooting"],
    "monitoring": ["Monitoring"],
    "log analysis": ["Log analysis"],
    "log monitoring": ["Log monitoring"],
    "automation": ["automation"],
    "performance": ["performance tuning", "System tuning"],
    "optimization": ["Optimization"],
    "deployment": ["deployment"],
    "pipelines": ["pipelines"],
    "robotics": ["Robotics"],
    "microcontrollers": ["microcontrollers"],
    "solidity": ["Solidity"],
    "blockchain": ["Blockchain concepts"],
    "unity": ["Unity"],
    "3d": ["3D concepts", "3D virtual worlds"],
    "graphics": ["graphics"],
    "linux": ["Linux"],
    "networking": ["Networking", "networking"],
    "vpn": ["VPNs"],
    "firewall": ["Firewalls"],
    "cloud security": ["Cloud security"],
    "penetration": ["penetration testing"],
    "exploitation": ["exploitation", "Advanced exploitation"],
}


def map_alternates_to_taxonomy(text: str, taxonomy_skills: list[str]) -> list[str]:
    """
    Map user's alternate/relative tags to taxonomy skills using the synonym map.
    Case-insensitive; whole-word match to avoid false positives (e.g. 'os' in 'postgresql').
    """
    if not text or not taxonomy_skills:
        return []
    text_lower = text.lower()
    text_norm = re.sub(r"[^\w\s]", " ", text_lower)
    text_words = set(text_norm.split())
    taxonomy_lower = {s.lower(): s for s in taxonomy_skills}
    matched = set()
    for alias, skills in SKILL_ALIASES.items():
        alias_lower = alias.lower()
        # Whole-word match (avoids 'os' matching 'postgresql')
        in_words = alias_lower in text_words
        in_text_boundary = bool(re.search(rf"\b{re.escape(alias_lower)}\b", text_lower))
        if in_words or in_text_boundary:
            for sk in skills:
                sk_lower = sk.lower()
                if sk_lower in taxonomy_lower:
                    matched.add(taxonomy_lower[sk_lower])
    return list(matched)

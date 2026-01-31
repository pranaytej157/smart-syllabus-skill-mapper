# app.py
from flask import Flask, request, jsonify, render_template
from ai_skill_matcher import ai_detect_and_map_skills, extract_skills_from_taxonomy_in_text
from skill_synonyms import map_alternates_to_taxonomy
from data_service import load_skill_taxonomy
from skill_mapper import map_skills_to_roles, generate_skill_roadmap

app = Flask(__name__)

# Load skill taxonomy once at startup
skill_taxonomy = load_skill_taxonomy("data/skill_list.xlsx")

@app.route("/map_skills", methods=["POST"])
def map_skills_api():
    # Get syllabus text from frontend
    syllabus_text = request.json.get("syllabus") if request.json else None
    if not syllabus_text:
        return jsonify({"message": "Syllabus text is required"}), 400
    
    # 1️⃣ AI agent: spontaneously detect skills and link to taxonomy (all data)
    taxonomy_skills = list({s for skills in skill_taxonomy.values() for s in skills})
    ai_skills = ai_detect_and_map_skills(syllabus_text, taxonomy_skills, role_skills=skill_taxonomy)
    if not ai_skills:
        ai_skills = extract_skills_from_taxonomy_in_text(syllabus_text, taxonomy_skills)
    # Large-scale synonym map: dbms→databases, mysql→SQL, programming→Programming, etc.
    synonym_matched = map_alternates_to_taxonomy(syllabus_text, taxonomy_skills)
    ai_skills = list(set(ai_skills) | set(synonym_matched))

    # 3️⃣ Map to roles & find missing skills
    mapping = map_skills_to_roles(ai_skills, skill_taxonomy)

    # 4️⃣ Generate roadmap for missing skills
    roadmap = generate_skill_roadmap(mapping)

    # 5 Return JSON response
    return jsonify({
        "matched_skills": {role: mapping[role]["matched"] for role in mapping},
        "missing_skills": {role: mapping[role]["missing"] for role in mapping},
        "roadmap": roadmap
    })

@app.route("/api/roles", methods=["GET"])
def get_roles():
    """Return list of available roles for the target-role selector."""
    return jsonify({"roles": list(skill_taxonomy.keys())})


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

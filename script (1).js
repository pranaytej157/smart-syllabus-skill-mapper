function checkSkills() {

    let syllabus = document.getElementById("syllabus").value.toLowerCase();
    let job = document.getElementById("job").value;

    if (!job) {
        alert("Please select a job role");
        return;
    }

    let aiSkillMap = {
        "dbms": "Database Management",
        "database": "Database Management",
        "sql": "Database Querying",
        "html": "HTML",
        "css": "CSS",
        "javascript": "JavaScript",
        "python": "Python Programming",
        "statistics": "Statistics",
        "machine learning": "ML Basics",
        "ml": "ML Basics"
    };

    let jobSkills = {
        software: ["Programming Basics","Data Structures","Problem Solving","OOP Concepts","Debugging"],
        web: ["HTML","CSS","JavaScript","Responsive Design","Backend Basics"],
        frontend: ["HTML","CSS","JavaScript","UI Design","Framework Basics"],
        backend: ["Python Programming","Database Management","API Development","System Design","Authentication"],
        data: ["Database Querying","Statistics","Data Analysis","Excel","Data Visualization"],
        ml: ["Python Programming","Statistics","ML Basics","Data Preprocessing","Model Evaluation"],
        cloud: ["Cloud Computing","Virtualization","Networking Basics","Security Basics","DevOps Basics"],
        security: ["Networking Basics","Security Fundamentals","Cryptography Basics","Risk Management","Ethical Hacking"]
    };

    let learningRoadmap = {
        "Python Programming": {
            topic: "Programming Fundamentals",
            course: "NPTEL / Coursera Python",
            project: "Student Management System",
            practice: "HackerRank"
        },
        "ML Basics": {
            topic: "Statistics + Python",
            course: "Coursera ML – Andrew Ng",
            project: "Student Result Prediction",
            practice: "Kaggle"
        },
        "Responsive Design": {
            topic: "Web Technologies",
            course: "FreeCodeCamp",
            project: "Responsive Website",
            practice: "Frontend Mentor"
        },
        "Backend Basics": {
            topic: "DBMS",
            course: "Node.js / Django",
            project: "Login & Registration System",
            practice: "CodeChef"
        }
    };

    let foundSkills = [];

    for (let key in aiSkillMap) {
        if (syllabus.includes(key)) {
            if (!foundSkills.includes(aiSkillMap[key])) {
                foundSkills.push(aiSkillMap[key]);
            }
        }
    }

    let missingSkills = jobSkills[job].filter(
        skill => !foundSkills.includes(skill)
    );

    let roadmapHTML = "";

    for (let skill of missingSkills) {
        if (learningRoadmap[skill]) {
            roadmapHTML += `
                <div class="roadmap-box">
                    <b>Skill:</b> ${skill}<br>
                    <b>Topic:</b> ${learningRoadmap[skill].topic}<br>
                    <b>Course:</b> ${learningRoadmap[skill].course}<br>
                    <b>Mini Project:</b> ${learningRoadmap[skill].project}<br>
                    <b>Practice:</b> ${learningRoadmap[skill].practice}
                </div>
            `;
        }
    }

    document.getElementById("result").innerHTML = `
        <b>Skills from Syllabus:</b><br>
        ${foundSkills.length ? foundSkills.join(", ") : "None"}
        <br><br>
        <b>Missing Skills:</b><br>
        ${missingSkills.length ? missingSkills.join(", ") : "None"}
    `;

    document.getElementById("roadmap").innerHTML = `
        <h3> Study & Learning Roadmap</h3>
        ${roadmapHTML || "No roadmap required 🎉"}
    `;
}
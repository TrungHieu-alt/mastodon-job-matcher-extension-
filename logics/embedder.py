from sentence_transformers import SentenceTransformer
import numpy as np

# ------------------ Setup model ------------------
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


# ------------------ JSON → Text (CV) ------------------
def json_to_text_cv(data: dict) -> str:
    try:
        parts = []
        if data.get("summary"):
            parts.append(f"Summary: {data['summary']}")
        if data.get("skills"):
            parts.append("Skills: " + ", ".join(sorted(set(data["skills"]))))

        if data.get("experiences"):
            exps = []
            for e in data["experiences"]:
                role = e.get("role", "")
                org = e.get("organization", "")
                yrs = e.get("years", 0)
                highlights = "; ".join(e.get("highlights", []))
                exps.append(f"{role} at {org} ({yrs} yrs) - {highlights}")
            parts.append("Experience: " + " | ".join(exps))

        if data.get("projects"):
            projs = []
            for p in data["projects"]:
                projs.append(f"{p.get('role','')} - {'; '.join(p.get('highlights', []))}")
            parts.append("Projects: " + " | ".join(projs))

        if data.get("education"):
            edus = []
            for edu in data["education"]:
                edus.append(f"{edu.get('degree','')} at {edu.get('school','')} ({edu.get('year','')}) GPA {edu.get('gpa','')}")
            parts.append("Education: " + " | ".join(edus))

        if data.get("certifications"):
            certs = [f"{c.get('name','')} ({c.get('year','')})" for c in data["certifications"]]
            parts.append("Certifications: " + ", ".join(certs))

        return "\n".join(parts).strip()
    except Exception as e:
        print(f"❌ Error converting CV JSON to text: {e}")
        return ""


# ------------------ JSON → Text (JD) ------------------
def json_to_text_jd(data: dict) -> str:
    try:
        parts = []
        if data.get("title"):
            parts.append(f"Job Title: {data['title']}")
        if data.get("summary"):
            parts.append(f"Summary: {data['summary']}")
        if data.get("requirements"):
            parts.append("Requirements: " + ", ".join(sorted(set(data["requirements"]))))
        if data.get("experience_level"):
            parts.append(f"Experience Level: {data['experience_level']}")
        if data.get("years_of_experience"):
            parts.append(f"Years of Experience: {data['years_of_experience']}")
        if data.get("tech_stack"):
            parts.append("Tech Stack: " + ", ".join(sorted(set(data["tech_stack"]))))
        if data.get("nice_to_have"):
            parts.append("Nice to have: " + ", ".join(sorted(set(data["nice_to_have"]))))
        return "\n".join(parts).strip()
    except Exception as e:
        print(f"❌ Error converting JD JSON to text: {e}")
        return ""


# ------------------ Detect Type & Convert ------------------
def json_to_text_auto(data: dict) -> str:
    try:
        if "skills" in data or "education" in data or "experiences" in data:
            return json_to_text_cv(data)
        elif "requirements" in data or "tech_stack" in data or "experience_level" in data:
            return json_to_text_jd(data)
        else:
            print("⚠️ Không xác định được loại dữ liệu (CV/JD), trả text thô.")
            return str(data)
    except Exception as e:
        print(f"❌ Error detecting JSON type: {e}")
        return str(data)


# ------------------ Embed JSON ------------------
def embed_json(data: dict):
    try:
        text = json_to_text_auto(data)
        print("\n----- Text to Embed -----")
        print(text)

        if not text.strip():
            raise ValueError("Empty text after JSON conversion")

        if model is None:
            raise RuntimeError("Embedding model is not loaded!")

        emb = model.encode(text, normalize_embeddings=True)
        print(f"✅ Embedding success, vector length = {len(emb)}")
        return text, np.array(emb, dtype=np.float32)

    except Exception as e:
        print(f"❌ Error during embedding: {e}")
        return "", np.array([])


# ------------------ Test ------------------
if __name__ == "__main__":
    try:
        # CV Sample
        sample_cv = {
            "summary": "Backend developer skilled in Node.js and SQL.",
            "skills": ["Node.js", "Express", "MySQL"],
            "experiences": [{"role": "Backend Dev", "organization": "ABC", "years": 1.5, "highlights": ["Built REST APIs"]}],
            "projects": [{"role": "Chat App", "highlights": ["Implemented real-time messaging with Socket.IO"]}],
            "education": [{"degree": "Computer Science", "school": "HUST", "year": "2022", "gpa": "3.7/4.0"}],
        }

        # JD Sample
        sample_jd = {
            "title": "Backend Developer",
            "summary": "Build and maintain scalable APIs using Node.js and databases.",
            "requirements": ["Node.js", "Express", "MySQL", "Docker"],
            "experience_level": "Mid",
            "years_of_experience": "2+",
            "tech_stack": ["Node.js", "Express", "MySQL", "Docker", "AWS"],
            "nice_to_have": ["CI/CD", "DevOps"]
        }

        print("\n=== 🧠 EMBED CV ===")
        text_cv, vec_cv = embed_json(sample_cv)
        print("Vector shape (CV):", vec_cv.shape)

        print("\n=== 🧠 EMBED JD ===")
        text_jd, vec_jd = embed_json(sample_jd)
        print("Vector shape (JD):", vec_jd.shape)

    except Exception as e:
        print(f"❌ Fatal error in __main__: {e}")

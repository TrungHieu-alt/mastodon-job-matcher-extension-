# ============================================
#           EMBEDDER FINAL VERSION
#    Multi-field Embedding for CV & JD
# ============================================

from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


# ======================================================
# UTILS — safe embed string → vector
# ======================================================
def embed_text(text: str):
    if not text or not text.strip():
        return np.zeros(384, dtype=np.float32)

    emb = model.encode(text.strip(), normalize_embeddings=True)
    return np.array(emb, dtype=np.float32)


# ======================================================
#   EMBED CV — 5 FIELDS
# ======================================================

def embed_cv(cv: dict):
    """
    Input schema: (from cvParser_final.py)
    {
        "summary": "",
        "skills": [],
        "experience_text": "",
        "projects_text": "",
        "full_text": ""
    }
    """

    summary = cv.get("summary", "")
    skills_list = cv.get("skills", [])
    skills_text = ", ".join(skills_list)
    exp_text = cv.get("experience_text", "")
    proj_text = cv.get("projects_text", "")
    full = cv.get("full_text", "")

    return {
        "emb_summary": embed_text(summary),
        "emb_skills": embed_text(skills_text),
        "emb_experience": embed_text(exp_text),
        "emb_projects": embed_text(proj_text),
        "emb_full": embed_text(full)
    }


# ======================================================
#   EMBED JD — 5 FIELDS
# ======================================================

def embed_jd(jd: dict):
    """
    Input schema: (from jdParser_final.py)
    {
        "job_description": "",
        "required_skills": [],
        "responsibilities": "",
        "techstack": "",
        "full_text": ""
    }
    """

    desc = jd.get("job_description", "")
    req_skills_list = jd.get("required_skills", [])
    skills_text = ", ".join(req_skills_list)
    responsibilities = jd.get("responsibilities", "")
    tech_text = jd.get("techstack", "")
    full = jd.get("full_text", "")

    return {
        "emb_description": embed_text(desc),
        "emb_required_skills": embed_text(skills_text),
        "emb_responsibilities": embed_text(responsibilities),
        "emb_techstack": embed_text(tech_text),
        "emb_full": embed_text(full)
    }


# ======================================================
# AUTO-DETECT (CV or JD)
# ======================================================

def embed_auto(data: dict):
    if "experience_text" in data or "projects_text" in data:
        return embed_cv(data)
    elif "responsibilities" in data or "techstack" in data:
        return embed_jd(data)
    else:
        raise ValueError("❌ Cannot detect CV/JD format. Wrong schema.")


# ======================================================
# TEST
# ======================================================
if __name__ == "__main__":

    sample_cv = {
        "summary": "Backend dev with Python + FastAPI",
        "skills": ["Python", "FastAPI", "MongoDB"],
        "experience_text": "Built backend services and optimized database queries.",
        "projects_text": "Developed job matching system using embeddings.",
        "full_text": "This is full CV text."
    }

    sample_jd = {
        "job_description": "We need a backend engineer to build FastAPI services.",
        "required_skills": ["Python", "FastAPI", "MongoDB"],
        "responsibilities": "Build APIs. Optimize DB queries.",
        "techstack": "FastAPI, Python, MongoDB",
        "full_text": "This is full JD text."
    }

    print("\n=== CV Embeddings ===")
    cv_vecs = embed_cv(sample_cv)
    for k, v in cv_vecs.items():
        print(k, v.shape)

    print("\n=== JD Embeddings ===")
    jd_vecs = embed_jd(sample_jd)
    for k, v in jd_vecs.items():
        print(k, v.shape)

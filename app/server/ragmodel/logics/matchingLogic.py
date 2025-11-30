import os, json, traceback
import numpy as np

from dataPreprocess.cvParser_final import parse_resume
from dataPreprocess.jdParser_final import parse_jobpost
from logics.embedder_final import embed_cv, embed_jd
from logics.llmEvaluate import evaluate_match   # vẫn giữ để giải thích top N nếu muốn

# =========================
# 0️⃣ Very simple in-memory "DB"
#    → mày thay bằng real DB / Chroma / LlamaIndex sau
# =========================

CV_STORE = {}   # cv_id -> {"data": cv_json, "emb": cv_embs}
JD_STORE = {}   # jd_id -> {"data": jd_json, "emb": jd_embs}


def upsert_cv(cv_id: str, cv_data: dict, cv_emb: dict):
    CV_STORE[cv_id] = {"data": cv_data, "emb": cv_emb}


def upsert_jd(jd_id: str, jd_data: dict, jd_emb: dict):
    JD_STORE[jd_id] = {"data": jd_data, "emb": jd_emb}


def get_all_cvs():
    return CV_STORE.items()


def get_all_jds():
    return JD_STORE.items()


# =========================
# 🔢 Helper: cosine
# =========================

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    if a is None or b is None or a.shape != b.shape:
        return 0.0
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


# =========================
# 🎯 Multi-field score CV ↔ JD
# =========================

def score_cv_for_jd(cv_emb: dict, jd_emb: dict) -> float:
    """
    cv_emb keys:
        emb_summary, emb_skills, emb_experience, emb_projects, emb_full
    jd_emb keys:
        emb_description, emb_required_skills, emb_responsibilities, emb_techstack, emb_full
    """

    w_summary = 0.35
    w_skills = 0.35
    w_exp = 0.15
    w_proj = 0.10
    w_full = 0.05

    s_summary = cosine(cv_emb["emb_summary"], jd_emb["emb_description"])
    s_skills = cosine(cv_emb["emb_skills"], jd_emb["emb_required_skills"])
    s_exp = cosine(cv_emb["emb_experience"], jd_emb["emb_responsibilities"])
    s_proj = cosine(cv_emb["emb_projects"], jd_emb["emb_techstack"])
    s_full = cosine(cv_emb["emb_full"], jd_emb["emb_full"])

    total = (
        w_summary * s_summary +
        w_skills * s_skills +
        w_exp * s_exp +
        w_proj * s_proj +
        w_full * s_full
    )
    return total


def score_jd_for_cv(jd_emb: dict, cv_emb: dict) -> float:
    # symmetric, nên dùng lại hàm trên cho nhất quán
    return score_cv_for_jd(cv_emb, jd_emb)


# =========================
# 1️⃣ Index all CVs
# =========================

def index_all_cvs(cv_folder="cv_folder"):
    print("\n=== 📥 INDEXING CVS (multi-field) ===")
    count = 0
    for file in os.listdir(cv_folder):
        if not file.lower().endswith(".pdf"):
            continue

        path = os.path.join(cv_folder, file)
        print(f"🧾 Parsing CV: {file}")
        try:
            cv_json = parse_resume(path)        # {"summary", "skills", "experience_text", "projects_text", "full_text"}
            cv_embs = embed_cv(cv_json)         # {"emb_summary", "emb_skills", ...}

            cv_id = file                        # hoặc hash/path/id gì mày muốn
            upsert_cv(cv_id, cv_json, cv_embs)

            count += 1
        except Exception as e:
            print(f"❌ Error processing CV {file}: {e}")
            traceback.print_exc()

    print(f"✅ Indexed {count} CVs with structured embeddings.")
    return count


# =========================
# 2️⃣ Index all JDs
# =========================

def index_all_jds(jd_folder="jd_folder"):
    print("\n=== 📥 INDEXING JDS (multi-field) ===")
    count = 0
    for file in os.listdir(jd_folder):
        if not file.lower().endswith(".txt"):
            continue

        path = os.path.join(jd_folder, file)
        print(f"🧾 Parsing JD: {file}")
        try:
            jd_text = open(path, "r", encoding="utf8").read()
            jd_json = parse_jobpost(jd_text)    # {"job_description", "required_skills", ...}
            jd_embs = embed_jd(jd_json)

            jd_id = file
            upsert_jd(jd_id, jd_json, jd_embs)

            count += 1
        except Exception as e:
            print(f"❌ Error processing JD {file}: {e}")
            traceback.print_exc()

    print(f"✅ Indexed {count} JDs with structured embeddings.")
    return count


# =========================
# 3️⃣ Find best candidates for a JD (text)
# =========================

def find_best_candidates(jd_text: str, top_k: int = 5, explain_top_n: int = 3):
    print("\n=== 🧩 FIND BEST CANDIDATES (semantic) ===")
    try:
        # 1. Parse + embed JD
        jd_json = parse_jobpost(jd_text)
        jd_emb = embed_jd(jd_json)

        # 2. Score tất cả CV (vì dataset nhỏ, brute-force cũng được)
        scored = []
        for cv_id, record in get_all_cvs():
            cv_data = record["data"]
            cv_emb = record["emb"]
            score = score_cv_for_jd(cv_emb, jd_emb)
            scored.append((cv_id, cv_data, score))

        # 3. Sort theo score
        scored.sort(key=lambda x: x[2], reverse=True)
        top = scored[:top_k]

        results = []

        # 4. Optional: LLM evaluate + reason cho top N
        for i, (cv_id, cv_data, score) in enumerate(top):
            jd_for_llm = jd_json["full_text"]
            cv_for_llm = cv_data["full_text"]

            eval_result = {"score": None, "reason": None}
            if i < explain_top_n:
                eval_result = evaluate_match(jd_for_llm, cv_for_llm)

            results.append({
                "target": cv_id,
                "semantic_score": round(score, 4),
                "llm_score": eval_result.get("score"),
                "reason": eval_result.get("reason")
            })

        print("\n🏆 TOP MATCHED CANDIDATES")
        for i, r in enumerate(results):
            print(f"\n#{i+1} {r['target']} | semantic={r['semantic_score']} | llm={r['llm_score']}")
            if r["reason"]:
                print(f"Reason: {r['reason'][:200]}...")

        return results

    except Exception as e:
        print(f"❌ Fatal error in find_best_candidates: {e}")
        traceback.print_exc()
        return []


# =========================
# 4️⃣ Find best jobs for a CV (path)
# =========================

def find_best_jobs(cv_path: str, top_k: int = 5, explain_top_n: int = 3):
    print("\n=== 🧩 FIND BEST JOBS (semantic) ===")
    try:
        # 1. Parse + embed CV
        cv_json = parse_resume(cv_path)
        cv_emb = embed_cv(cv_json)

        # 2. Score tất cả JD
        scored = []
        for jd_id, record in get_all_jds():
            jd_data = record["data"]
            jd_emb = record["emb"]
            score = score_jd_for_cv(jd_emb, cv_emb)
            scored.append((jd_id, jd_data, score))

        scored.sort(key=lambda x: x[2], reverse=True)
        top = scored[:top_k]

        results = []

        # 3. Optional: LLM evaluate
        for i, (jd_id, jd_data, score) in enumerate(top):
            jd_for_llm = jd_data["full_text"]
            cv_for_llm = cv_json["full_text"]

            eval_result = {"score": None, "reason": None}
            if i < explain_top_n:
                eval_result = evaluate_match(jd_for_llm, cv_for_llm)

            results.append({
                "target": jd_id,
                "semantic_score": round(score, 4),
                "llm_score": eval_result.get("score"),
                "reason": eval_result.get("reason")
            })

        print("\n🏆 TOP MATCHED JOBS")
        for i, r in enumerate(results):
            print(f"\n#{i+1} {r['target']} | semantic={r['semantic_score']} | llm={r['llm_score']}")
            if r["reason"]:
                print(f"Reason: {r['reason'][:200]}...")

        return results

    except Exception as e:
        print(f"❌ Fatal error in find_best_jobs: {e}")
        traceback.print_exc()
        return []


# =========================
# 5️⃣ Demo entry
# =========================

if __name__ == "__main__":
    try:
        # 1. Index trước
        index_all_cvs("cv_folder")
        index_all_jds("jd_folder")

        # 2. Demo tìm candidate
        jd_text = """
        Hiring Backend Developer skilled in Python, FastAPI, and MongoDB.
        0-2 years experience. Knowledge of Docker and cloud is a plus.
        """
        find_best_candidates(jd_text)

    except Exception as e:
        print(f"❌ Fatal error in __main__: {e}")
        traceback.print_exc()

import os, json, traceback
from dataPreprocess.resumeParser import parse_resume
from dataPreprocess.jobParser import parse_job_description
from db.LlamaIndexAdapter import upsert_json_doc, query_topk
from logics.embedder import json_to_text_auto
from logics.llmEvaluate import evaluate_match


# =========================
# 1️⃣ Build or update index
# =========================
def index_all_cvs(cv_folder="cv_folder"):
    cvs = []
    print("\n=== 📥 INDEXING CVS ===")
    try:
        for file in os.listdir(cv_folder):
            if not file.lower().endswith(".pdf"):
                continue
            path = os.path.join(cv_folder, file)
            print(f"🧾 Parsing CV: {file}")
            try:
                cv_json = parse_resume(path)
                upsert_json_doc("cv_collection", cv_json, {"type": "cv", "filename": file})
                cvs.append(cv_json)
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")
                traceback.print_exc()
        print(f"✅ Indexed {len(cvs)} CVs successfully.")
    except Exception as e:
        print(f"❌ Fatal error while indexing CVs: {e}")
        traceback.print_exc()
    return cvs


def index_all_jds(jd_folder="jd_folder"):
    jds = []
    print("\n=== 📥 INDEXING JDS ===")
    try:
        for file in os.listdir(jd_folder):
            if not file.lower().endswith(".txt"):
                continue
            path = os.path.join(jd_folder, file)
            print(f"🧾 Parsing JD: {file}")
            try:
                jd_text = open(path, "r", encoding="utf8").read()
                jd_json = parse_job_description(jd_text)
                upsert_json_doc("jd_collection", jd_json, {"type": "jd", "filename": file})
                jds.append(jd_json)
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")
                traceback.print_exc()
        print(f"✅ Indexed {len(jds)} JDs successfully.")
    except Exception as e:
        print(f"❌ Fatal error while indexing JDs: {e}")
        traceback.print_exc()
    return jds


# =========================
# 2️⃣ Find best candidates
# =========================
def find_best_candidates(jd_text: str):
    print("\n=== 🧩 FIND BEST CANDIDATES ===")
    try:
        jd_json = parse_job_description(jd_text)
        jd_text_norm = json_to_text_auto(jd_json)
        print("🔎 Querying top CVs from collection...")
        nodes = query_topk("cv_collection", jd_text_norm, top_k=5)
        print(f"✅ Retrieved {len(nodes)} candidates from vector DB.")

        results = []
        for node in nodes:
            try:
                cv_text = node.node.get_text()
                cv_meta = node.node.metadata or {}
                name = cv_meta.get("filename") or cv_meta.get("id") or "UNKNOWN"
                print(f"\n🧠 Evaluating {name}")
                eval_result = evaluate_match(jd_text_norm, cv_text)
                results.append({
                    "target": name,
                    "similarity": round(node.score, 4),
                    "evaluation": eval_result
                })
            except Exception as e:
                print(f"❌ Error evaluating candidate: {e}")
                traceback.print_exc()

        results.sort(key=lambda x: x["evaluation"].get("score", 0), reverse=True)

        print("\n🏆 TOP MATCHED CANDIDATES")
        for i, r in enumerate(results):
            print(f"\n#{i+1} {r['target']} | LLM Score {r['evaluation'].get('score')}")
            print(f"Reason: {r['evaluation'].get('reason')}")

        return results

    except Exception as e:
        print(f"❌ Fatal error in find_best_candidates: {e}")
        traceback.print_exc()
        return []


# =========================
# 3️⃣ Find best jobs
# =========================
def find_best_jobs(cv_path: str):
    print("\n=== 🧩 FIND BEST JOBS ===")
    try:
        cv_json = parse_resume(cv_path)
        cv_text_norm = json_to_text_auto(cv_json)
        print("🔎 Querying top JDs from collection...")
        nodes = query_topk("jd_collection", cv_text_norm, top_k=5)
        print(f"✅ Retrieved {len(nodes)} JDs from vector DB.")

        results = []
        for node in nodes:
            try:
                jd_text = node.node.get_text()
                jd_meta = node.node.metadata or {}
                name = jd_meta.get("filename") or jd_meta.get("id") or "UNKNOWN"
                print(f"\n🧠 Evaluating {name}")
                eval_result = evaluate_match(jd_text, cv_text_norm)
                results.append({
                    "target": name,
                    "similarity": round(node.score, 4),
                    "evaluation": eval_result
                })
            except Exception as e:
                print(f"❌ Error evaluating JD: {e}")
                traceback.print_exc()

        results.sort(key=lambda x: x["evaluation"].get("score", 0), reverse=True)

        print("\n🏆 TOP MATCHED JOBS")
        for i, r in enumerate(results):
            print(f"\n#{i+1} {r['target']} | LLM Score {r['evaluation'].get('score')}")
            print(f"Reason: {r['evaluation'].get('reason')}")

        return results

    except Exception as e:
        print(f"❌ Fatal error in find_best_jobs: {e}")
        traceback.print_exc()
        return []


# =========================
# 4️⃣ Demo entry
# =========================
if __name__ == "__main__":
    try:
        jd_text = """
        Hiring Backend Developer skilled in Node.js, SQL, and API design.
        no experience needed. Familiar with Docker and AWS is a plus.
        """
        find_best_candidates(jd_text)
    except Exception as e:
        print(f"❌ Fatal error in __main__: {e}")
        traceback.print_exc()

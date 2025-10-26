# init_db.py
import os
import json
from dataPreprocess.resumeParser import parse_resume
from dataPreprocess.jobParser import parse_job_description
from db.LlamaIndexAdapter import upsert_json_doc

# ===============================
# 📁 Setup folders
# ===============================
CV_FOLDER = "cv_folder"
os.makedirs(CV_FOLDER, exist_ok=True)

# ===============================
# 🧠 Sample JD (1 job)
# ===============================
SAMPLE_JD_TEXT = """
We are hiring a Backend Developer.
Responsibilities:
- Build and maintain scalable APIs using Node.js and Express.
- Work with databases like MySQL or PostgreSQL.
- Collaborate with frontend and DevOps teams.
Requirements:
- 2+ years of experience in backend development.
- Strong knowledge of JavaScript, RESTful APIs, and SQL.
- Familiar with Docker and AWS is a plus.
"""

# ===============================
# ⚙️ Step 1: Seed JD
# ===============================
print("\n=== 🚀 Seeding Job Description ===")
jd_json = parse_job_description(SAMPLE_JD_TEXT)
upsert_json_doc("jd_collection", jd_json, {"type": "jd", "filename": "sample_backend_jd.txt"})
print("✅ JD inserted into Chroma\n")

# ===============================
# ⚙️ Step 2: Seed all CVs
# ===============================
print("=== 🚀 Seeding CVs ===")

cv_files = [f for f in os.listdir(CV_FOLDER) if f.lower().endswith((".pdf", ".png", ".jpg", ".jpeg"))]
if not cv_files:
    print("⚠️ Không tìm thấy CV nào trong thư mục cv_folder/. Hãy đặt file .pdf vào đó trước khi chạy.")
else:
    for cv_file in cv_files:
        cv_path = os.path.join(CV_FOLDER, cv_file)
        try:
            cv_json = parse_resume(cv_path)
            upsert_json_doc("cv_collection", cv_json, {"type": "cv", "filename": cv_file})
            print(f"✅ CV added: {cv_file}")
        except Exception as e:
            print(f"❌ Lỗi khi parse {cv_file}: {e}")

print("\n🎉 Database initialization complete!")
print("Bạn có thể chạy:")
print("  → find_best_candidates(JD_text)")
print("  → find_best_jobs('cv_folder/<your_cv>.pdf')")

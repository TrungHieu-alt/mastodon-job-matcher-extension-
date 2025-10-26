# jdParser.py
import re
import google.generativeai as gemini
from dotenv import load_dotenv
import os
import json

# --- Cấu hình ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
gemini.configure(api_key=api_key)

def parse_job_description(jd_text: str) -> dict:
    """
    Chuẩn hóa (normalize) và trích xuất thông tin quan trọng từ JD bằng Gemini.
    Trả về đối tượng JSON chuẩn gồm các trường chính.
    """
    prompt = f"""
    You are a precise JD parser. Read the following Job Description and extract key info.
    Return VALID JSON ONLY with these fields:
    {{
      "title": "Job title",
      "summary": "Short 2-3 sentence summary of the role",
      "requirements": ["list of skill or tech requirements"],
      "experience_level": "Junior/Mid/Senior/Lead/Manager",
      "years_of_experience": "Number of years if available",
      "tech_stack": ["list of mentioned technologies"],
      "nice_to_have": ["optional but beneficial skills"]
    }}

    Respond with JSON only, no explanation or extra text.

    --- JD ---
    {jd_text}
    """
    response = gemini.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
    text = response.text.strip()

    # Tìm và trích JSON trong phần text trả về
    json_pattern = re.search(r"\{[\s\S]*\}", text)
    if json_pattern:
        json_str = json_pattern.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"⚠️ Parse lỗi JSON ({e}), trả về text thô.")
            return {"raw_text": jd_text.strip()}
    else:
        print("⚠️ Không tìm thấy JSON trong phản hồi, trả về text thô.")
        return {"raw_text": jd_text.strip()}


# --- Test trực tiếp  ---
if __name__ == "__main__":
  print("helo")
  sample_jd = """
We are hiring a Backend Developer.

Responsibilities:
- Build and maintain scalable APIs using Node.js and Express.
- Work with databases like MySQL or MongoDB.
- Collaborate with frontend and DevOps teams.

Requirements:
- 2+ years of experience in backend development.
- Strong knowledge of JavaScript, RESTful APIs, and SQL.
- Familiar with Docker, AWS, or CI/CD tools is a plus.
"""

  result = parse_job_description(sample_jd)
  print("\n===== 🧠 PARSED JD JSON =====")
  print(json.dumps(result, indent=2, ensure_ascii=False))

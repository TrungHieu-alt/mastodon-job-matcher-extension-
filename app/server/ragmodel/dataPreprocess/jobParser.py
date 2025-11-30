# ============================
#       JD PARSER FINAL
#   Hybrid Regex + LLM Clean
# ============================

import google.generativeai as gemini
import re
import json
from config import GEMINI_API_KEY

gemini.configure(api_key=GEMINI_API_KEY)
llm = gemini.GenerativeModel("gemini-2.5-flash")


# ==========================================
# REGEX HELPERS
# ==========================================

def find_section(text, names):
    p = r"(?:^|\n)(%s)[\:\s]*\n" % "|".join([re.escape(n) for n in names])
    parts = re.split(p, text, flags=re.I)
    out = {}
    for i in range(1, len(parts), 2):
        sec = parts[i].lower()
        data = parts[i+1]
        out[sec] = data.strip()
    return out


def extract_skill_list(text):
    lines = text.split("\n")
    out = []
    for line in lines:
        if "," in line:
            out.extend([s.strip() for s in line.split(",") if s.strip()])
    return list(dict.fromkeys(out))


def extract_bullets(text):
    lines = text.split("\n")
    out = []
    for line in lines:
        if re.match(r"^[\-\•\*]\s+", line.strip()):
            out.append(line.strip("•-* \n"))
    return out


# ==========================================
# LLM CLEANERS
# ==========================================

def llm_clean_desc(text):
    prompt = f"""
Clean this job description intro.
Rules:
- Do NOT invent anything.
- Keep 1–3 sentences max.
- Use only the meaning from the first 300 characters.

Text:
{text[:300]}

Return only cleaned text, no JSON.
"""
    return llm.generate_content(prompt).text.strip()


def llm_clean_text(text):
    if not text:
        return ""
    prompt = f"""
Clean the following list of bullet points or requirement lines.
Rules:
- Do not invent.
- Keep original meaning.
- Combine into 1–3 sentences max.
- No JSON.

Input:
{text}
"""
    return llm.generate_content(prompt).text.strip()


# ==========================================
# MAIN FUNCTION
# ==========================================

def parse_jobpost(jd_text: str) -> dict:
    sections = find_section(jd_text, 
        ["DESCRIPTION", "RESPONSIBILITIES", "REQUIREMENTS", "TECH STACK", "TECHNOLOGIES"]
    )

    # --- description / summary ---
    if "description" in sections:
        job_desc = llm_clean_desc(sections["description"])
    else:
        job_desc = llm_clean_desc(jd_text[:300])

    # --- responsibilities ---
    res_bullets = ""
    if "responsibilities" in sections:
        bullets = extract_bullets(sections["responsibilities"])
        res_bullets = llm_clean_text("\n".join(bullets))

    # --- skills ---
    raw_skills = []
    if "requirements" in sections:
        raw_skills = extract_skill_list(sections["requirements"])
    elif "tech stack" in sections:
        raw_skills = extract_skill_list(sections["tech stack"])

    skills = sorted(list(dict.fromkeys([s.strip() for s in raw_skills if s.strip()])))

    # --- tech stack text (for projects_text mirror) ---
    tech_text = ""
    if "tech stack" in sections:
        bullets = extract_bullets(sections["tech stack"])
        tech_text = llm_clean_text("\n".join(bullets))

    return {
        "job_description": job_desc,
        "required_skills": skills,
        "responsibilities": res_bullets,
        "techstack": tech_text,
        "full_text": jd_text.strip()
    }


# DEBUG
if __name__ == "__main__":
    sample = """
    We are hiring a Backend Developer.

    Responsibilities:
    - Build APIs using Node.js, Express.
    - Work with MongoDB or SQL.
    - Deploy via Docker.

    Requirements:
    JavaScript, Node.js, SQL, Docker

    Tech Stack:
    - Node.js
    - Express
    - SQL
    - AWS
    """
    print(json.dumps(parse_jobpost(sample), indent=2, ensure_ascii=False))

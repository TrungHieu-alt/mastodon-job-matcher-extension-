# ============================
#       CV PARSER FINAL
#   Hybrid Regex + LLM Clean
#      Output EXACTLY 5 fields
# ============================

import google.generativeai as gemini
import fitz
import pytesseract
from PIL import Image
from config import GEMINI_API_KEY
import re
import json
import os

gemini.configure(api_key=GEMINI_API_KEY)
llm = gemini.GenerativeModel("gemini-2.5-flash")


# ==========================================
# STEP 1 — RAW TEXT EXTRACTION
# ==========================================
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for p in doc:
        text += p.get_text("text") + "\n"
    return text.strip()

def extract_text_from_img(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img).strip()


# ==========================================
# STEP 2 — REGEX PRE-EXTRACTION
# ==========================================

def regex_find_section(text, names):
    """
    Tách section dựa vào heading như SUMMARY, SKILLS, EXPERIENCE, PROJECTS.
    """
    pattern = r"(?:^|\n)(%s)[\:\s]*\n" % "|".join([re.escape(n) for n in names])
    splits = re.split(pattern, text, flags=re.I)

    out = {}
    for i in range(1, len(splits), 2):
        sec = splits[i].lower()
        data = splits[i+1]
        out[sec] = data.strip()
    return out


def regex_extract_skills(text):
    """
    Extract skill list (raw) dựa vào:
    - dòng chứa dấu phẩy
    - bullet có nhiều tech
    """
    lines = text.split("\n")
    candidates = []

    for line in lines:
        if "," in line:
            candidates.extend([s.strip() for s in line.split(",") if len(s.strip()) > 1])

    # lọc ký tự rác
    clean = []
    for s in candidates:
        if re.match(r"[A-Za-z0-9#\+\.\-\s]+$", s):
            clean.append(s)

    # unique
    clean = list(dict.fromkeys(clean))
    return clean


def regex_extract_highlights(raw_text):
    """Tìm bullet lines (•, -, *)"""
    lines = raw_text.split("\n")
    out = []
    for line in lines:
        if re.match(r"^[\-\*\•]\s+", line.strip()):
            out.append(line.strip("•-* \n"))
    return out


# ==========================================
# STEP 3 — LLM CLEANING (NO INFERENCE)
# ==========================================

def llm_clean_summary(text):
    prompt = f"""
You will clean and extract a resume SUMMARY section.
Rules:
- MUST NOT invent information.
- If no summary exists, return "".
- Summary should be 1–3 sentences max.
- Only use text from the first 300 characters of the resume.

Resume intro:
{text[:300]}
Return ONLY the cleaned summary text (no JSON).
"""
    rep = llm.generate_content(prompt)
    return rep.text.strip()


def llm_clean_block(text):
    """
    Clean experience/project highlights into 1 semantic paragraph.
    """
    if not text or len(text.strip()) < 5:
        return ""

    prompt = f"""
Clean the following action/bullet points.
Rules:
- Do NOT invent new facts.
- Keep original meaning ONLY.
- Merge into 1–3 sentences max.
- Remove duplicates.
- No JSON. Just the cleaned text.

Input:
{text}
"""
    rep = llm.generate_content(prompt)
    return rep.text.strip()


# ==========================================
# STEP 4 — BUILD FINAL 5 FIELDS
# ==========================================

def build_final_cv(raw_text):
    # ---- PRE-EXTRACT SECTIONS ----
    sections = regex_find_section(raw_text, 
        ["SUMMARY", "PROFESSIONAL SUMMARY", "PROFILE", "SKILLS", "EXPERIENCE", "PROJECTS"]
    )

    # ---- Summary ----
    summary = ""
    if "summary" in sections:
        summary = llm_clean_summary(sections["summary"])
    else:
        summary = llm_clean_summary(raw_text[:350])

    # ---- Skills ----
    raw_skills = []
    if "skills" in sections:
        raw_skills = regex_extract_skills(sections["skills"])
    else:
        raw_skills = regex_extract_skills(raw_text)

    # unique normalize
    skills = sorted(list(dict.fromkeys([s.strip() for s in raw_skills if s.strip()])))

    # ---- Experience ----
    exp_highlights = ""
    if "experience" in sections:
        bullets = regex_extract_highlights(sections["experience"])
        exp_highlights = llm_clean_block("\n".join(bullets))

    # ---- Projects ----
    proj_highlights = ""
    if "projects" in sections:
        bullets = regex_extract_highlights(sections["projects"])
        proj_highlights = llm_clean_block("\n".join(bullets))

    return {
        "summary": summary or "",
        "skills": skills or [],
        "experience_text": exp_highlights or "",
        "projects_text": proj_highlights or "",
        "full_text": raw_text
    }


# ==========================================
# MAIN FUNCTION
# ==========================================

def parse_resume(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        raw = extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        raw = extract_text_from_img(file_path)
    else:
        raise ValueError("Unsupported format")

    return build_final_cv(raw)


# DEBUG
if __name__ == "__main__":
    print(json.dumps(parse_resume("public/resume.pdf"), indent=2, ensure_ascii=False))

# llmEvaluate_final.py
from google import generativeai as gemini
from config import GEMINI_API_KEY
import json, re, traceback

def _log(msg: str):
    print(msg.replace("```", "'''"))


# ============================
# Gemini Setup
# ============================
try:
    gemini.configure(api_key=GEMINI_API_KEY)
    _log("✅ Gemini API configured successfully.")
except Exception as e:
    _log(f"❌ Failed to configure Gemini API: {e}")


# ============================
# JSON CLEAN HELPERS
# ============================
def _clean_code_fence(t: str) -> str:
    t = t.strip()
    t = re.sub(r"```json", "", t, flags=re.I)
    t = re.sub(r"```", "", t)
    return t.strip()


def _extract_json(t: str) -> str:
    """Take { ... } block only."""
    start = t.find("{")
    end = t.rfind("}")
    if start != -1 and end != -1 and end > start:
        return t[start:end+1]
    return t.strip()


def _sanitize_json(t: str) -> str:
    t = re.sub(r'\([^)]*\)', '', t)
    t = re.sub(r'//.*', '', t)
    t = re.sub(r'#.*', '', t)
    t = t.replace("\n", " ")
    return t.strip()


def _validate(obj: dict) -> dict:
    if not isinstance(obj, dict):
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "reason": str(obj)[:200]
        }

    out = {
        "score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "reason": ""
    }

    # score
    try:
        val = obj.get("score", 0)
        if isinstance(val, (int, float)):
            out["score"] = int(val)
        else:
            val = str(val).replace("%", "")
            out["score"] = int(float(val)) if val.replace(".", "").isdigit() else 0
    except:
        out["score"] = 0

    # skills
    out["matched_skills"] = [s.strip() for s in obj.get("matched_skills", []) if isinstance(s, str)]
    out["missing_skills"] = [s.strip() for s in obj.get("missing_skills", []) if isinstance(s, str)]

    # reason
    out["reason"] = str(obj.get("reason", ""))[:400]

    return out


# ============================
# MAIN
# ============================
def evaluate_match(jd_fulltext: str, cv_fulltext: str):
    """
    jd_fulltext = JD["full_text"]
    cv_fulltext = CV["full_text"]
    """

    _log("\n=== 🤖 EVALUATING MATCH ===")

    if not jd_fulltext.strip() or not cv_fulltext.strip():
        return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": "Empty input."}

    prompt = f"""
You are a senior recruiter. Evaluate how well this CV matches this Job Description.

STRICT RULES:
- DO NOT invent skills. Only extract skills that explicitly appear in the text.
- matched_skills MUST be a subset of the actual skills found in BOTH texts.
- missing_skills MUST be a subset of REQUIREMENTS found in JD but NOT in CV.
- reason MUST be 1–2 sentences, concise, no hallucination.
- score MUST be an integer 0–100.
- Return ONLY valid JSON, no code fences.

Job Description (JD):
{jd_fulltext}

Curriculum Vitae (CV):
{cv_fulltext}

Return JSON:
{{
  "score": 0-100,
  "matched_skills": [],
  "missing_skills": [],
  "reason": ""
}}
"""

    try:
        model = gemini.GenerativeModel("gemini-2.5-flash")
        resp = model.generate_content(prompt)

        raw = (resp.text or "").strip()
        _log("Raw LLM output:")
        _log(raw[:600])

        cleaned = _clean_code_fence(raw)
        cleaned = _extract_json(cleaned)
        cleaned = _sanitize_json(cleaned)

        try:
            parsed = json.loads(cleaned)
            return _validate(parsed)
        except:
            _log("❌ JSON Failed:")
            _log(cleaned)
            return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": cleaned[:200]}

    except Exception as e:
        _log(f"❌ Fatal LLM error: {e}")
        traceback.print_exc()
        return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": str(e)[:200]}

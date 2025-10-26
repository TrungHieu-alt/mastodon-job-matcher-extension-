# llmEvaluate.py
from google import generativeai as gemini
from config import GEMINI_API_KEY
import json, re, traceback

def _log(msg: str):
    print(msg.replace("```", "'''"))  # tránh highlight markdown

# ------------------ Setup Gemini ------------------
try:
    gemini.configure(api_key=GEMINI_API_KEY)
    _log("✅ Gemini API configured successfully.")
except Exception as e:
    _log(f"❌ Failed to configure Gemini API: {e}")


# ------------------ JSON Cleaning Helpers ------------------
def _strip_code_fence(text: str) -> str:
    """Loại bỏ ```json ... ``` hoặc ``` ... ``` ở đầu/cuối."""
    t = text.strip()
    t = re.sub(r"^\s*```json\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\s*```\s*", "", t)
    t = re.sub(r"\s*```\s*$", "", t)
    return t.strip()


def _extract_json_block(text: str) -> str:
    """
    Tìm ra khối JSON hợp lệ trong text.
    Thứ tự:
      1. Trong ```json``` hoặc ```
      2. Bằng dấu { ... }
    """
    # Có thể nằm trong code fence
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()

    m = re.search(r"```\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if m:
        return m.group(1).strip()

    # Fallback: tìm dấu ngoặc đầu–cuối
    s = text
    start = s.find("{")
    if start == -1:
        return text.strip()
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start:i+1].strip()
    return text.strip()


def _sanitize_json_text(txt: str) -> str:
    """Làm sạch text để tránh lỗi JSON: bỏ comment, ngoặc tròn, xuống dòng thừa."""
    txt = re.sub(r'\([^)]*\)', '', txt)  # bỏ (comment)
    txt = re.sub(r'//.*', '', txt)       # bỏ comment //
    txt = re.sub(r'#.*', '', txt)        # bỏ comment #
    txt = txt.replace('\n', ' ')         # gộp dòng
    txt = txt.replace('\r', '')
    return txt.strip()


def _coerce_schema(obj: dict) -> dict:
    """Ép schema JSON về chuẩn."""
    if not isinstance(obj, dict):
        return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": str(obj)[:200]}
    out = {}
    try:
        val = obj.get("score", 0)
        if isinstance(val, (int, float)):
            out["score"] = int(val)
        else:
            out["score"] = int(float(str(val).replace("%", "").strip()) if str(val).replace(".", "", 1).isdigit() else 0)
    except Exception:
        out["score"] = 0

    out["matched_skills"] = list(obj.get("matched_skills", []))
    out["missing_skills"] = list(obj.get("missing_skills", []))
    out["reason"] = str(obj.get("reason", ""))[:500]
    return out


# ------------------ Main Evaluation ------------------
def evaluate_match(jd_text: str, cv_text: str):
    _log("\n=== 🤖 EVALUATING MATCH WITH GEMINI ===")
    try:
        if not jd_text.strip() or not cv_text.strip():
            _log("⚠️ Empty JD or CV text, skipping evaluation.")
            return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": "Empty input text."}

        prompt = f"""
You are an experienced recruiter. Evaluate how well this CV fits the job.

JD:
{jd_text}

CV:
{cv_text}

Return ONLY valid JSON (no code fences, no markdown, no explanation):
{{
  "score": 40-100,
  "matched_skills": [],
  "missing_skills": [],
  "reason": "1-2 sentence summary"
}}
"""

        model = gemini.GenerativeModel("gemini-2.5-flash")
        _log("🕐 Sending request to Gemini...")
        response = model.generate_content(prompt)
        raw = (response.text or "").strip()

        if not raw:
            _log("⚠️ Gemini returned empty response.")
            return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": "Gemini returned empty response"}

        _log("✅ Raw Gemini response (truncated if long):")
        _log(raw[:800] + ("..." if len(raw) > 800 else ""))

        cleaned = _strip_code_fence(raw)
        cleaned = _extract_json_block(cleaned)
        cleaned = _sanitize_json_text(cleaned)

        try:
            parsed = json.loads(cleaned)
            parsed = _coerce_schema(parsed)
            _log("✅ Parsed JSON successfully.")
            return parsed
        except json.JSONDecodeError as e:
            _log(f"❌ JSON decode failed: {e}")
            _log("⚠️ Cleaned content fallback:")
            _log(cleaned[:400])
            return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": cleaned[:200]}

    except Exception as e:
        _log(f"❌ Unexpected error during LLM evaluation: {e}")
        traceback.print_exc()
        return {"score": 0, "matched_skills": [], "missing_skills": [], "reason": str(e)[:200]}

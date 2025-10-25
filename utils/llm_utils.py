"""LLM utilities for candidate evaluation."""

import json
from typing import Dict, Any
from loguru import logger


def evaluate_candidate_with_llm(job_description: str, candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate a candidate using LLM."""
    try:
        from openai import OpenAI
        client = OpenAI()
        
        cv_metadata = candidate.get('metadata', {})
        cv_name = cv_metadata.get('name', 'N/A')
        
        # Convert CV metadata to readable text
        cv_text = json.dumps(cv_metadata, indent=2, ensure_ascii=False)
        
        system_prompt = """
        Bạn là một chuyên gia tuyển dụng kỹ thuật (Tech Recruiter) rất kinh nghiệm và tỉ mỉ.
        Nhiệm vụ của bạn là đánh giá một CV của ứng viên dựa trên một Bản mô tả công việc (JD) được cung cấp.
        Hãy phân tích sâu và trả về kết quả đánh giá DUY NHẤT dưới dạng một đối tượng JSON.

        Đối tượng JSON phải có các trường sau:
        - "score": một con số từ 0 đến 100, thể hiện mức độ phù hợp tổng thể.
        - "skills_checklist": một đối tượng chứa hai danh sách: "matched_skills" và "missing_skills".
        - "experience_match": một chuỗi ngắn để đánh giá kinh nghiệm (ví dụ: "Rất phù hợp", "Phù hợp", "Không đủ kinh nghiệm").
        - "risk_points": một danh sách các điểm rủi ro hoặc không phù hợp cần lưu ý.
        - "rationale": một đoạn văn ngắn (2-3 câu) giải thích lý do cho điểm số của bạn.
        - "strengths": một danh sách các điểm mạnh của ứng viên.
        - "recommendations": một danh sách các đề xuất cải thiện cho ứng viên.
        """
        
        user_prompt = f"""
        Dưới đây là Bản mô tả công việc (JD) và CV của ứng viên. Vui lòng đánh giá.

        --- JD ---
        {job_description}

        --- CV ---
        {cv_text}
        """
        
        logger.info(f"Evaluating candidate with LLM: {cv_name}")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        evaluation = json.loads(response.choices[0].message.content)
        logger.info(f"✅ Completed LLM evaluation for {cv_name}")
        
        return evaluation
        
    except Exception as e:
        logger.error(f"Error evaluating candidate with LLM: {e}")
        return None


def evaluate_job_match_with_llm(cv_data: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate how well a job matches a CV using LLM."""
    try:
        from openai import OpenAI
        client = OpenAI()
        
        job_metadata = job.get('metadata', {})
        job_title = job_metadata.get('title', 'Unknown Position')
        
        # Convert CV data to readable text
        cv_text = json.dumps(cv_data, indent=2, ensure_ascii=False)
        
        # Convert job data to readable text
        job_text = job.get('document', '')
        
        system_prompt = """
        Bạn là một chuyên gia tuyển dụng kỹ thuật (Tech Recruiter) rất kinh nghiệm.
        Nhiệm vụ của bạn là đánh giá mức độ phù hợp giữa một CV và một công việc.
        Hãy phân tích và trả về kết quả đánh giá dưới dạng một đối tượng JSON.

        Đối tượng JSON phải có các trường sau:
        - "score": một con số từ 0 đến 100, thể hiện mức độ phù hợp tổng thể.
        - "skills_match": một đối tượng chứa "matched_skills" và "missing_skills".
        - "experience_match": đánh giá kinh nghiệm (ví dụ: "Rất phù hợp", "Phù hợp", "Thiếu kinh nghiệm").
        - "education_match": đánh giá trình độ học vấn.
        - "strengths": danh sách các điểm mạnh của ứng viên cho công việc này.
        - "concerns": danh sách các điểm cần lưu ý hoặc thiếu sót.
        - "rationale": lý do cho điểm số (2-3 câu).
        - "recommendation": đề xuất (ví dụ: "Highly recommended", "Good fit", "Consider with reservations").
        """
        
        user_prompt = f"""
        Đánh giá mức độ phù hợp giữa CV và công việc sau:

        --- CÔNG VIỆC ---
        {job_text}

        --- CV ---
        {cv_text}
        """
        
        logger.info(f"Evaluating job match with LLM: {job_title}")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        evaluation = json.loads(response.choices[0].message.content)
        logger.info(f"✅ Completed LLM evaluation for job: {job_title}")
        
        return evaluation
        
    except Exception as e:
        logger.error(f"Error evaluating job match with LLM: {e}")
        return None

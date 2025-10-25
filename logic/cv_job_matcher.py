"""CV to Job matching logic."""

import json
from typing import List, Dict, Any
from loguru import logger

from db.job_storage import search_similar_jobs
from utils.llm_utils import evaluate_job_match_with_llm
from utils.text_utils import create_embedding_content_from_json


def find_matching_jobs_for_cv(cv_data: Dict[str, Any], max_jobs: int = 5) -> List[Dict[str, Any]]:
    """Find matching jobs for a CV."""
    try:
        logger.info("Starting CV to job matching process")
        
        # Create search query from CV data
        search_query = create_cv_search_query(cv_data)
        
        # Step 1: Search for similar jobs using ChromaDB
        similar_jobs = search_similar_jobs(
            query=search_query,
            n_results=max_jobs * 2,
            similarity_threshold=0.6
        )
        
        if not similar_jobs:
            logger.warning("No similar jobs found")
            return []
        
        logger.info(f"Found {len(similar_jobs)} similar jobs from ChromaDB")
        
        # Step 2: Evaluate job matches with LLM
        evaluated_jobs = []
        for job in similar_jobs[:max_jobs]:
            try:
                evaluation = evaluate_job_match_with_llm(cv_data, job)
                if evaluation:
                    job['llm_evaluation'] = evaluation
                    job['llm_score'] = evaluation.get('score', 0)
                    evaluated_jobs.append(job)
                else:
                    # Add job without LLM evaluation
                    job['llm_evaluation'] = {'score': 0, 'error': 'Evaluation failed'}
                    job['llm_score'] = 0
                    evaluated_jobs.append(job)
                    
            except Exception as e:
                logger.error(f"Error evaluating job match: {e}")
                job['llm_evaluation'] = {'score': 0, 'error': str(e)}
                job['llm_score'] = 0
                evaluated_jobs.append(job)
        
        # Step 3: Sort by LLM score
        evaluated_jobs.sort(
            key=lambda x: x.get('llm_score', 0),
            reverse=True
        )
        
        logger.info(f"Completed CV to job matching: {len(evaluated_jobs)} jobs evaluated")
        return evaluated_jobs
        
    except Exception as e:
        logger.error(f"Error in CV to job matching: {e}")
        return []


def create_cv_search_query(cv_data: Dict[str, Any]) -> str:
    """Create search query from CV data for job matching."""
    query_parts = []
    
    # Add name and summary
    if cv_data.get("name"):
        query_parts.append(f"Looking for {cv_data['name']}")
    
    if cv_data.get("summary"):
        query_parts.append(cv_data["summary"])
    
    # Add experience
    experiences = cv_data.get("experiences", [])
    if experiences:
        exp_text = []
        for exp in experiences:
            if isinstance(exp, dict):
                role = exp.get("role", "")
                org = exp.get("organization", "")
                if role and org:
                    exp_text.append(f"{role} at {org}")
        if exp_text:
            query_parts.append(f"Experience: {', '.join(exp_text)}")
    
    # Add skills
    skills = cv_data.get("skills", [])
    if skills:
        query_parts.append(f"Skills: {', '.join(skills)}")
    
    # Add education
    education = cv_data.get("education", [])
    if education:
        edu_text = []
        for edu in education:
            if isinstance(edu, dict):
                degree = edu.get("degree", "")
                school = edu.get("school", "")
                if degree and school:
                    edu_text.append(f"{degree} from {school}")
        if edu_text:
            query_parts.append(f"Education: {', '.join(edu_text)}")
    
    return " ".join(query_parts)


def calculate_cv_job_match_score(cv_data: Dict[str, Any], job: Dict[str, Any]) -> float:
    """Calculate match score between CV and job."""
    try:
        similarity_score = job.get('similarity', 0)
        llm_score = job.get('llm_score', 0)
        
        # Weighted combination: 30% similarity + 70% LLM score
        match_score = (similarity_score * 0.3) + (llm_score * 0.7)
        
        return match_score
        
    except Exception as e:
        logger.error(f"Error calculating CV-job match score: {e}")
        return 0.0

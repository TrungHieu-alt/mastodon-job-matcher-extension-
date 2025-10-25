"""Database save operations for CVs and job descriptions."""

from typing import Dict, Any, Optional
from loguru import logger

from db.chromaDB import chroma_db


def save_resume_to_chroma(cv_data: Dict[str, Any], owner: str, source_url: str = None) -> Optional[str]:
    """
    Save a parsed CV to ChromaDB.
    
    Args:
        cv_data: Parsed CV data dictionary
        owner: Mastodon username of CV owner
        source_url: URL of the original Mastodon post
        
    Returns:
        CV ID if successful, None otherwise
    """
    try:
        if not isinstance(cv_data, dict) or not cv_data:
            logger.error("Invalid CV data provided")
            return None

        # Save CV using ChromaDB manager
        cv_id = chroma_db.save_cv(cv_data, owner, source_url)
        
        if cv_id:
            logger.info(f"✅ Successfully saved CV for @{owner} with ID: {cv_id}")
        else:
            logger.error(f"❌ Failed to save CV for @{owner}")
            
        return cv_id
        
    except Exception as e:
        logger.error(f"Error saving CV for @{owner}: {e}")
        return None


def save_job_description_to_chroma(job_data: Dict[str, Any]) -> Optional[str]:
    """
    Save a job description to ChromaDB.
    
    Args:
        job_data: Job description data dictionary
        
    Returns:
        Job ID if successful, None otherwise
    """
    try:
        if not isinstance(job_data, dict) or not job_data:
            logger.error("Invalid job data provided")
            return None

        # Save job description using ChromaDB manager
        jd_id = chroma_db.save_job_description(job_data)
        
        if jd_id:
            logger.info(f"✅ Successfully saved job description with ID: {jd_id}")
        else:
            logger.error("❌ Failed to save job description")
            
        return jd_id
        
    except Exception as e:
        logger.error(f"Error saving job description: {e}")
        return None


def get_cv_by_id(cv_id: str) -> Optional[Dict[str, Any]]:
    """Get a CV by ID."""
    return chroma_db.get_cv_by_id(cv_id)


def get_job_by_id(jd_id: str) -> Optional[Dict[str, Any]]:
    """Get a job description by ID."""
    return chroma_db.get_job_by_id(jd_id)


def search_similar_cvs(query: str, n_results: int = 5, similarity_threshold: float = 0.7) -> list:
    """Search for similar CVs."""
    return chroma_db.search_similar_cvs(query, n_results, similarity_threshold)


def search_similar_jobs(query: str, n_results: int = 5, similarity_threshold: float = 0.7) -> list:
    """Search for similar job descriptions."""
    return chroma_db.search_similar_jobs(query, n_results, similarity_threshold)

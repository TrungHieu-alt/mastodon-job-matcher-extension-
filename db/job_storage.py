"""Job description storage operations with ChromaDB."""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

from db.chroma_connection import chroma_connection


def save_job_to_database(job_data: Dict[str, Any]) -> Optional[str]:
    """Save a job description to the database."""
    try:
        # Generate unique job ID
        jd_id = f"jd_{uuid.uuid4().hex[:8]}"
        
        # Prepare metadata
        metadata = prepare_job_metadata(job_data, jd_id)
        
        # Create embedding text
        embedding_text = create_job_embedding_text(job_data)
        
        # Save to collection
        chroma_connection.jd_collection.add(
            ids=[jd_id],
            documents=[embedding_text],
            metadatas=[metadata]
        )
        
        logger.info(f"Successfully saved job description: {jd_id}")
        return jd_id
        
    except Exception as e:
        logger.error(f"Failed to save job description: {e}")
        return None


def search_similar_jobs(query: str, n_results: int = 5, similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
    """Search for similar job descriptions."""
    try:
        results = chroma_connection.jd_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        similar_jobs = []
        if results['ids'] and results['ids'][0]:
            for i, (jd_id, distance) in enumerate(zip(results['ids'][0], results['distances'][0])):
                similarity = 1 - distance  # Convert distance to similarity
                if similarity >= similarity_threshold:
                    similar_jobs.append({
                        'id': jd_id,
                        'similarity': similarity,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'document': results['documents'][0][i] if results['documents'] else ""
                    })
        
        logger.info(f"Found {len(similar_jobs)} similar job descriptions for query")
        return similar_jobs
        
    except Exception as e:
        logger.error(f"Failed to search job descriptions: {e}")
        return []


def get_job_by_id(jd_id: str) -> Optional[Dict[str, Any]]:
    """Get a job description by ID."""
    try:
        results = chroma_connection.jd_collection.get(ids=[jd_id])
        if results['ids']:
            return {
                'id': results['ids'][0],
                'metadata': results['metadatas'][0] if results['metadatas'] else {},
                'document': results['documents'][0] if results['documents'] else ""
            }
        return None
    except Exception as e:
        logger.error(f"Failed to get job description {jd_id}: {e}")
        return None


def get_all_jobs(limit: int = 100) -> List[Dict[str, Any]]:
    """Get all job descriptions with optional limit."""
    try:
        results = chroma_connection.jd_collection.get(limit=limit)
        jobs = []
        if results['ids']:
            for i, jd_id in enumerate(results['ids']):
                jobs.append({
                    'id': jd_id,
                    'metadata': results['metadatas'][i] if results['metadatas'] else {},
                    'document': results['documents'][i] if results['documents'] else ""
                })
        return jobs
    except Exception as e:
        logger.error(f"Failed to get all jobs: {e}")
        return []


def prepare_job_metadata(job_data: Dict[str, Any], jd_id: str) -> Dict[str, Any]:
    """Prepare job metadata for storage."""
    return {
        "id": jd_id,
        "title": job_data.get("title", ""),
        "company": job_data.get("company", ""),
        "location": job_data.get("location", ""),
        "employment_type": job_data.get("employment_type", ""),
        "salary_range": job_data.get("salary_range", ""),
        "required_skills": job_data.get("required_skills", []),
        "required_experience_years": job_data.get("required_experience_years", 0),
        "source_url": job_data.get("source_url", ""),
        "posted_by": job_data.get("posted_by", ""),
        "posted_date": job_data.get("posted_date", datetime.now().isoformat()),
        "created_at": datetime.now().isoformat()
    }


def create_job_embedding_text(job_data: Dict[str, Any]) -> str:
    """Create embedding text from job data."""
    content_parts = []
    
    if job_data.get("title"):
        content_parts.append(f"Job Title: {job_data['title']}")
    if job_data.get("company"):
        content_parts.append(f"Company: {job_data['company']}")
    if job_data.get("location"):
        content_parts.append(f"Location: {job_data['location']}")
    if job_data.get("description"):
        content_parts.append(f"Description: {job_data['description']}")
    if job_data.get("required_skills"):
        skills_text = ", ".join(job_data["required_skills"])
        content_parts.append(f"Required Skills: {skills_text}")
    if job_data.get("required_experience_years"):
        content_parts.append(f"Required Experience: {job_data['required_experience_years']} years")
    
    return "\n".join(content_parts)

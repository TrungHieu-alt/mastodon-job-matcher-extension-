"""CV storage operations with ChromaDB."""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

from db.chroma_connection import chroma_connection
from utils.text_utils import create_embedding_content_from_json


def save_cv_to_database(cv_data: Dict[str, Any], owner: str, source_url: str = None) -> Optional[str]:
    """Save a CV to the database."""
    try:
        # Generate unique CV ID
        cv_id = f"cv_{owner}_{uuid.uuid4().hex[:8]}"
        
        # Prepare metadata
        metadata = prepare_cv_metadata(cv_data, owner, source_url, cv_id)
        
        # Create embedding content
        embedding_text = create_embedding_content_from_json(cv_data)
        
        # Save to collection
        chroma_connection.cv_collection.add(
            ids=[cv_id],
            documents=[embedding_text],
            metadatas=[metadata]
        )
        
        logger.info(f"Successfully saved CV: {cv_id} for @{owner}")
        return cv_id
        
    except Exception as e:
        logger.error(f"Failed to save CV for @{owner}: {e}")
        return None


def search_similar_cvs(query: str, n_results: int = 5, similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
    """Search for similar CVs."""
    try:
        results = chroma_connection.cv_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        similar_cvs = []
        if results['ids'] and results['ids'][0]:
            for i, (cv_id, distance) in enumerate(zip(results['ids'][0], results['distances'][0])):
                similarity = 1 - distance  # Convert distance to similarity
                if similarity >= similarity_threshold:
                    similar_cvs.append({
                        'id': cv_id,
                        'similarity': similarity,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'document': results['documents'][0][i] if results['documents'] else ""
                    })
        
        logger.info(f"Found {len(similar_cvs)} similar CVs for query")
        return similar_cvs
        
    except Exception as e:
        logger.error(f"Failed to search CVs: {e}")
        return []


def get_cv_by_id(cv_id: str) -> Optional[Dict[str, Any]]:
    """Get a CV by ID."""
    try:
        results = chroma_connection.cv_collection.get(ids=[cv_id])
        if results['ids']:
            return {
                'id': results['ids'][0],
                'metadata': results['metadatas'][0] if results['metadatas'] else {},
                'document': results['documents'][0] if results['documents'] else ""
            }
        return None
    except Exception as e:
        logger.error(f"Failed to get CV {cv_id}: {e}")
        return None


def get_all_cvs(limit: int = 100) -> List[Dict[str, Any]]:
    """Get all CVs with optional limit."""
    try:
        results = chroma_connection.cv_collection.get(limit=limit)
        cvs = []
        if results['ids']:
            for i, cv_id in enumerate(results['ids']):
                cvs.append({
                    'id': cv_id,
                    'metadata': results['metadatas'][i] if results['metadatas'] else {},
                    'document': results['documents'][i] if results['documents'] else ""
                })
        return cvs
    except Exception as e:
        logger.error(f"Failed to get all CVs: {e}")
        return []


def prepare_cv_metadata(cv_data: Dict[str, Any], owner: str, source_url: str, cv_id: str) -> Dict[str, Any]:
    """Prepare CV metadata for storage."""
    return {
        "id": cv_id,
        "owner": owner,
        "source_url": source_url or "",
        "name": cv_data.get("name", ""),
        "posted_at": datetime.now().isoformat(),
        "skills": cv_data.get("skills", []),
        "experience_years": calculate_total_experience(cv_data),
        "education_level": get_highest_education(cv_data),
        "location": extract_location(cv_data),
        "created_at": datetime.now().isoformat()
    }


def calculate_total_experience(cv_data: Dict[str, Any]) -> float:
    """Calculate total years of experience."""
    experiences = cv_data.get("experiences", [])
    total_years = 0.0
    
    for exp in experiences:
        if isinstance(exp, dict):
            years = exp.get("years", 0)
            if isinstance(years, (int, float)) and years > 0:
                total_years += years
    
    return round(total_years, 2)


def get_highest_education(cv_data: Dict[str, Any]) -> str:
    """Get the highest education level."""
    education = cv_data.get("education", [])
    if not education:
        return "Unknown"
    
    degrees = [edu.get("degree", "").lower() for edu in education if isinstance(edu, dict)]
    
    if any("phd" in degree or "doctorate" in degree for degree in degrees):
        return "PhD"
    elif any("master" in degree for degree in degrees):
        return "Master's"
    elif any("bachelor" in degree for degree in degrees):
        return "Bachelor's"
    elif any("associate" in degree for degree in degrees):
        return "Associate's"
    else:
        return degrees[0] if degrees else "Unknown"


def extract_location(cv_data: Dict[str, Any]) -> str:
    """Extract location from CV data."""
    experiences = cv_data.get("experiences", [])
    for exp in experiences:
        if isinstance(exp, dict) and exp.get("location"):
            return exp["location"]
    
    activities = cv_data.get("activities", [])
    for act in activities:
        if isinstance(act, dict) and act.get("location"):
            return act["location"]
    
    return "Unknown"

"""ChromaDB vector database implementation for CV and job description storage."""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import Optional, List, Dict, Any, Union
from loguru import logger
import uuid
from datetime import datetime

from config.settings import settings


class ChromaDBManager:
    """ChromaDB manager for CV and job description storage and retrieval."""
    
    def __init__(self):
        """Initialize ChromaDB client and collections."""
        try:
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_directory,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            logger.info(f"ChromaDB client initialized at {settings.chroma_persist_directory}")
            
            # Initialize collections
            self._cv_collection = None
            self._jd_collection = None
            self._init_collections()
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def _init_collections(self):
        """Initialize CV and job description collections."""
        try:
            # CV Collection
            try:
                self._cv_collection = self.client.get_collection("cvs")
                logger.info("Connected to existing CV collection")
            except ValueError:
                self._cv_collection = self.client.create_collection(
                    name="cvs",
                    metadata={"description": "CV documents and embeddings"}
                )
                logger.info("Created new CV collection")
            
            # Job Description Collection
            try:
                self._jd_collection = self.client.get_collection("job_descriptions")
                logger.info("Connected to existing job descriptions collection")
            except ValueError:
                self._jd_collection = self.client.create_collection(
                    name="job_descriptions",
                    metadata={"description": "Job description documents and embeddings"}
                )
                logger.info("Created new job descriptions collection")
                
        except Exception as e:
            logger.error(f"Failed to initialize collections: {e}")
            raise
    
    @property
    def cv_collection(self):
        """Get CV collection."""
        return self._cv_collection
    
    @property
    def jd_collection(self):
        """Get job description collection."""
        return self._jd_collection
    
    def save_cv(self, cv_data: Dict[str, Any], owner: str, source_url: str = None) -> Optional[str]:
        """
        Save a CV to the vector database.
        
        Args:
            cv_data: Parsed CV data dictionary
            owner: Mastodon username of CV owner
            source_url: URL of the original Mastodon post
            
        Returns:
            CV ID if successful, None otherwise
        """
        try:
            # Generate unique CV ID
            cv_id = f"cv_{owner}_{uuid.uuid4().hex[:8]}"
            
            # Prepare metadata
            metadata = {
                "id": cv_id,
                "owner": owner,
                "source_url": source_url or "",
                "name": cv_data.get("name", ""),
                "posted_at": datetime.now().isoformat(),
                "skills": cv_data.get("skills", []),
                "experience_years": self._calculate_total_experience(cv_data),
                "education_level": self._get_highest_education(cv_data),
                "location": self._extract_location(cv_data),
                "created_at": datetime.now().isoformat()
            }
            
            # Create embedding text
            embedding_text = self._create_cv_embedding_text(cv_data)
            
            # Add to collection
            self.cv_collection.add(
                ids=[cv_id],
                documents=[embedding_text],
                metadatas=[metadata]
            )
            
            logger.info(f"Successfully saved CV: {cv_id} for @{owner}")
            return cv_id
            
        except Exception as e:
            logger.error(f"Failed to save CV for @{owner}: {e}")
            return None
    
    def save_job_description(self, job_data: Dict[str, Any]) -> Optional[str]:
        """
        Save a job description to the vector database.
        
        Args:
            job_data: Job description data dictionary
            
        Returns:
            Job ID if successful, None otherwise
        """
        try:
            # Generate unique job ID
            jd_id = f"jd_{uuid.uuid4().hex[:8]}"
            
            # Prepare metadata
            metadata = {
                "id": jd_id,
                "title": job_data.get("title", ""),
                "company": job_data.get("company", ""),
                "location": job_data.get("location", ""),
                "employment_type": job_data.get("employment_type", ""),
                "salary_range": job_data.get("salary_range", ""),
                "required_skills": job_data.get("required_skills", []),
                "required_experience_years": job_data.get("required_experience_years", 0),
                "source_url": job_data.get("source_url", ""),
                "posted_date": job_data.get("posted_date", datetime.now().isoformat()),
                "created_at": datetime.now().isoformat()
            }
            
            # Create embedding text
            embedding_text = self._create_jd_embedding_text(job_data)
            
            # Add to collection
            self.jd_collection.add(
                ids=[jd_id],
                documents=[embedding_text],
                metadatas=[metadata]
            )
            
            logger.info(f"Successfully saved job description: {jd_id}")
            return jd_id
            
        except Exception as e:
            logger.error(f"Failed to save job description: {e}")
            return None
    
    def search_similar_cvs(self, query: str, n_results: int = 5, 
                          similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Search for CVs similar to the query.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of similar CVs with metadata and scores
        """
        try:
            results = self.cv_collection.query(
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
    
    def search_similar_jobs(self, query: str, n_results: int = 5, 
                           similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Search for job descriptions similar to the query.
        
        Args:
            query: Search query text
            n_results: Number of results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of similar job descriptions with metadata and scores
        """
        try:
            results = self.jd_collection.query(
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
    
    def get_cv_by_id(self, cv_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific CV by ID."""
        try:
            results = self.cv_collection.get(ids=[cv_id])
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
    
    def get_job_by_id(self, jd_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific job description by ID."""
        try:
            results = self.jd_collection.get(ids=[jd_id])
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
    
    def get_all_cvs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all CVs with optional limit."""
        try:
            results = self.cv_collection.get(limit=limit)
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
    
    def get_all_jobs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all job descriptions with optional limit."""
        try:
            results = self.jd_collection.get(limit=limit)
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
    
    def delete_cv(self, cv_id: str) -> bool:
        """Delete a CV by ID."""
        try:
            self.cv_collection.delete(ids=[cv_id])
            logger.info(f"Successfully deleted CV: {cv_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete CV {cv_id}: {e}")
            return False
    
    def delete_job(self, jd_id: str) -> bool:
        """Delete a job description by ID."""
        try:
            self.jd_collection.delete(ids=[jd_id])
            logger.info(f"Successfully deleted job description: {jd_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete job description {jd_id}: {e}")
            return False
    
    def _create_cv_embedding_text(self, cv_data: Dict[str, Any]) -> str:
        """Create embedding text from CV data."""
        from utils.text_utils import create_embedding_content_from_json
        return create_embedding_content_from_json(cv_data)
    
    def _create_jd_embedding_text(self, job_data: Dict[str, Any]) -> str:
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
    
    def _calculate_total_experience(self, cv_data: Dict[str, Any]) -> float:
        """Calculate total years of experience from CV data."""
        experiences = cv_data.get("experiences", [])
        total_years = 0.0
        
        for exp in experiences:
            if isinstance(exp, dict):
                years = exp.get("years", 0)
                if isinstance(years, (int, float)) and years > 0:
                    total_years += years
        
        return total_years
    
    def _get_highest_education(self, cv_data: Dict[str, Any]) -> str:
        """Get the highest education level from CV data."""
        education = cv_data.get("education", [])
        if not education:
            return ""
        
        # Simple logic to determine highest education
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
            return degrees[0] if degrees else ""
    
    def _extract_location(self, cv_data: Dict[str, Any]) -> str:
        """Extract location from CV data."""
        # Try to get location from experiences
        experiences = cv_data.get("experiences", [])
        for exp in experiences:
            if isinstance(exp, dict) and exp.get("location"):
                return exp["location"]
        
        # Try to get from activities
        activities = cv_data.get("activities", [])
        for act in activities:
            if isinstance(act, dict) and act.get("location"):
                return act["location"]
        
        return ""


# Global ChromaDB manager instance
chroma_db = ChromaDBManager()

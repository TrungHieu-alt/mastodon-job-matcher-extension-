"""Scoring and matching utilities."""

from typing import List, Dict, Any


def calculate_skill_match_score(cv_skills: List[str], job_skills: List[str]) -> float:
    """Calculate skill match score between CV and job."""
    if not job_skills:
        return 0.5  # Neutral score if no job skills specified
    
    if not cv_skills:
        return 0.0
    
    # Normalize skills to lowercase for comparison
    cv_skills_lower = [skill.lower() for skill in cv_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    
    # Calculate intersection
    matched_skills = set(cv_skills_lower).intersection(set(job_skills_lower))
    
    return len(matched_skills) / len(job_skills_lower)


def calculate_experience_match_score(cv_experience: float, job_experience: int) -> float:
    """Calculate experience match score."""
    if job_experience == 0:
        return 0.5  # Neutral score if no experience requirement
    
    if cv_experience >= job_experience:
        return 1.0  # Perfect match
    else:
        return cv_experience / job_experience  # Partial match


def calculate_composite_score(similarity: float, skill_score: float, experience_score: float) -> float:
    """Calculate overall matching score."""
    weights = {
        "similarity": 0.4,
        "skills": 0.4,
        "experience": 0.2
    }
    
    return (
        similarity * weights["similarity"] +
        skill_score * weights["skills"] +
        experience_score * weights["experience"]
    )


def calculate_total_experience(cv_data: Dict[str, Any]) -> float:
    """Calculate total years of experience from CV data."""
    experiences = cv_data.get("experiences", [])
    total_years = 0.0
    
    for exp in experiences:
        if isinstance(exp, dict):
            years = exp.get("years", 0)
            if isinstance(years, (int, float)) and years > 0:
                total_years += years
    
    return total_years


def get_highest_education_level(cv_data: Dict[str, Any]) -> str:
    """Get the highest education level from CV data."""
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
    
    return "Unknown"

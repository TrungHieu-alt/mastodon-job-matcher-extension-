"""Text processing utilities."""

import re
from typing import Dict, List, Any


def create_embedding_content_from_json(cv_data: Dict[str, Any]) -> str:
    """Create embedding content from CV data for ChromaDB."""
    content_parts = []
    
    # Basic info
    if cv_data.get("name"):
        content_parts.append(f"Name: {cv_data['name']}")
    
    if cv_data.get("summary"):
        content_parts.append(f"Summary: {cv_data['summary']}")
    
    # Education
    if cv_data.get("education"):
        content_parts.append("Education:")
        for edu in cv_data["education"]:
            if isinstance(edu, dict):
                edu_parts = []
                if edu.get("degree"):
                    edu_parts.append(edu["degree"])
                if edu.get("school"):
                    edu_parts.append(f"from {edu['school']}")
                if edu.get("year"):
                    edu_parts.append(f"({edu['year']})")
                if edu_parts:
                    content_parts.append(f"- {' '.join(edu_parts)}")
    
    # Experience
    if cv_data.get("experiences"):
        content_parts.append("Work Experience:")
        for exp in cv_data["experiences"]:
            if isinstance(exp, dict):
                exp_parts = []
                if exp.get("role"):
                    exp_parts.append(exp["role"])
                if exp.get("organization"):
                    exp_parts.append(f"at {exp['organization']}")
                if exp.get("years") and exp["years"] > 0:
                    exp_parts.append(f"({exp['years']} years)")
                if exp.get("location"):
                    exp_parts.append(f"in {exp['location']}")
                
                if exp_parts:
                    content_parts.append(f"- {' '.join(exp_parts)}")
                
                # Add highlights
                if exp.get("highlights"):
                    for highlight in exp["highlights"]:
                        if highlight:
                            content_parts.append(f"  • {highlight}")
    
    # Projects
    if cv_data.get("projects"):
        content_parts.append("Projects:")
        for proj in cv_data["projects"]:
            if isinstance(proj, dict) and proj.get("role"):
                content_parts.append(f"- {proj['role']}")
                if proj.get("highlights"):
                    for highlight in proj["highlights"]:
                        if highlight:
                            content_parts.append(f"  • {highlight}")
    
    # Skills
    if cv_data.get("skills"):
        skills_text = ", ".join(cv_data["skills"])
        content_parts.append(f"Skills: {skills_text}")
    
    # Languages
    if cv_data.get("languages"):
        languages_text = ", ".join(cv_data["languages"])
        content_parts.append(f"Languages: {languages_text}")
    
    # Certifications
    if cv_data.get("certifications"):
        content_parts.append("Certifications:")
        for cert in cv_data["certifications"]:
            if isinstance(cert, dict) and cert.get("name"):
                cert_parts = [cert["name"]]
                if cert.get("issuer"):
                    cert_parts.append(f"from {cert['issuer']}")
                if cert.get("year"):
                    cert_parts.append(f"({cert['year']})")
                content_parts.append(f"- {' '.join(cert_parts)}")
    
    # Awards
    if cv_data.get("awards"):
        content_parts.append("Awards:")
        for award in cv_data["awards"]:
            if isinstance(award, dict) and award.get("title"):
                award_parts = [award["title"]]
                if award.get("issuer"):
                    award_parts.append(f"from {award['issuer']}")
                if award.get("year"):
                    award_parts.append(f"({award['year']})")
                content_parts.append(f"- {' '.join(award_parts)}")
    
    return "\n".join(content_parts)


def extract_keywords_from_text(text: str) -> List[str]:
    """Extract relevant keywords from text for matching."""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
        "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "can", "this", "that", "these", "those"
    }
    
    # Extract words (alphanumeric + some special chars)
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    
    # Filter out stop words and short words
    keywords = [word for word in words if len(word) > 2 and word not in stop_words]
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(keywords))


def extract_skills_from_text(text: str) -> List[str]:
    """Extract technical skills from text."""
    tech_skills = [
        'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
        'node.js', 'django', 'flask', 'spring', 'express', 'mongodb', 'postgresql',
        'mysql', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'linux', 'windows',
        'machine learning', 'ai', 'data science', 'analytics', 'sql', 'nosql',
        'html', 'css', 'bootstrap', 'jquery', 'php', 'ruby', 'go', 'rust',
        'c++', 'c#', '.net', 'swift', 'kotlin', 'android', 'ios'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in tech_skills:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return found_skills


def extract_experience_requirement(text: str) -> int:
    """Extract experience requirement from text."""
    patterns = [
        r'(\d+)\s*năm\s*kinh\s*nghiệm',
        r'(\d+)\s*years?\s*experience',
        r'kinh\s*nghiệm\s*(\d+)\s*năm',
        r'experience\s*(\d+)\s*years?',
        r'(\d+)\+\s*years?',
        r'(\d+)\+\s*năm'
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return int(match.group(1))
    
    return 0


def extract_job_title(text: str) -> str:
    """Extract job title from text."""
    lines = text.split('\n')
    for line in lines[:3]:  # Check first 3 lines
        line = line.strip()
        if any(keyword in line.lower() for keyword in ['tuyển', 'tìm', 'cần', 'recruit', 'hiring']):
            if len(line) < 100:  # Reasonable title length
                return line
    return "Job Position"


def normalize_text(text: str) -> str:
    """Normalize text for better matching."""
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters except spaces and basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()
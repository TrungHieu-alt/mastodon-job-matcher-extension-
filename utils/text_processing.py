"""Text processing utilities."""

import re
from typing import List, Dict, Any


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


def normalize_text(text: str) -> str:
    """Normalize text for better matching."""
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters except spaces and basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()


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

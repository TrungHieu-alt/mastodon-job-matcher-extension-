"""Job post processing logic."""

import re
import time
from typing import Dict, Any, Optional
from loguru import logger

from db.job_storage import save_job_to_database
from utils.text_utils import extract_skills_from_text, extract_experience_requirement, extract_job_title


def process_job_post(post_content: str, poster_account: Dict[str, Any]) -> Dict[str, Any]:
    """Process a job post and extract job information."""
    try:
        # Extract job description
        job_text = extract_job_description(post_content)
        if not job_text:
            return {'success': False, 'error': 'No job description found'}
        
        # Create job data
        job_data = create_job_data(job_text, poster_account)
        
        # Save job to database
        job_id = save_job_to_database(job_data)
        if not job_id:
            return {'success': False, 'error': 'Failed to save job description'}
        
        return {
            'success': True,
            'job_id': job_id,
            'job_text': job_text,
            'job_data': job_data
        }
        
    except Exception as e:
        logger.error(f"Error processing job post: {e}")
        return {'success': False, 'error': str(e)}


def extract_job_description(content: str) -> Optional[str]:
    """Extract job description from post content."""
    try:
        # Remove HTML tags
        job_text = re.sub(r'<.*?>', '', content).strip()
        # Remove hashtags
        job_text = re.sub(r'#\w+', '', job_text).strip()
        # Remove extra whitespace
        job_text = re.sub(r'\s+', ' ', job_text)
        return job_text if job_text else None
    except Exception as e:
        logger.error(f"Error extracting job description: {e}")
        return None


def create_job_data(job_text: str, poster_account: Dict[str, Any]) -> Dict[str, Any]:
    """Create job data from text and poster account."""
    return {
        "title": extract_job_title(job_text),
        "description": job_text,
        "company": "Unknown",  # Could be extracted from post
        "location": "Unknown",  # Could be extracted from post
        "required_skills": extract_skills_from_text(job_text),
        "required_experience_years": extract_experience_requirement(job_text),
        "employment_type": "Full-time",  # Default
        "source_url": f"https://mastodonuet.duckdns.org/web/statuses/{poster_account.get('id', '')}",
        "posted_by": poster_account.get('acct', 'Unknown'),
        "posted_date": time.strftime("%Y-%m-%d %H:%M:%S")
    }

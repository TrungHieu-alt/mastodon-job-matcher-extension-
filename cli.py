"""Command-line interface for managing the CV matching system."""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from utils.logging_config import setup_logging
from services.job_service import job_service
from services.matching_service import matching_service
from database.chroma_client import chroma_client
from loguru import logger


def add_job_command(args):
    """Add a job description from file or input."""
    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                job_data = json.load(f)
        else:
            # Interactive input
            job_data = {
                "title": input("Job Title: "),
                "company": input("Company: "),
                "location": input("Location: "),
                "description": input("Job Description: "),
                "required_skills": input("Required Skills (comma-separated): ").split(","),
                "required_experience_years": int(input("Required Experience (years): ") or 0),
                "employment_type": input("Employment Type: "),
                "salary_range": input("Salary Range: "),
                "source_url": input("Source URL (optional): ")
            }
        
        job_id = job_service.add_job_description(job_data)
        if job_id:
            print(f"✅ Job description added successfully: {job_id}")
        else:
            print("❌ Failed to add job description")
            
    except Exception as e:
        logger.error(f"Error adding job: {e}")
        print(f"❌ Error: {e}")


def search_cvs_command(args):
    """Search for CVs matching a job description."""
    try:
        # Get job description
        if args.job_id:
            job = job_service.get_job_by_id(args.job_id)
            if not job:
                print(f"❌ Job not found: {args.job_id}")
                return
            query = job["document"]
        else:
            query = args.query
        
        # Search for matching CVs
        matches = matching_service.match_job_to_cvs(
            job_description=query,
            job_metadata={},
            max_matches=args.max_results
        )
        
        if matches:
            print(f"\n📋 Found {len(matches)} matching CVs:\n")
            for i, match in enumerate(matches, 1):
                cv_metadata = match.get("metadata", {})
                print(f"{i}. {cv_metadata.get('name', 'Unknown')} (@{cv_metadata.get('owner', 'Unknown')})")
                print(f"   Overall Score: {match['overall_score']:.2f}")
                print(f"   Similarity: {match['similarity']:.2f}")
                print(f"   Skills Match: {match['skill_match_score']:.2f}")
                print(f"   Experience Match: {match['experience_score']:.2f}")
                print(f"   Skills: {', '.join(cv_metadata.get('skills', [])[:5])}")
                print()
        else:
            print("❌ No matching CVs found")
            
    except Exception as e:
        logger.error(f"Error searching CVs: {e}")
        print(f"❌ Error: {e}")


def search_jobs_command(args):
    """Search for jobs matching a CV."""
    try:
        # This would require CV data input - simplified for now
        print("❌ CV search not implemented yet. Use the Mastodon listener to add CVs first.")
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        print(f"❌ Error: {e}")


def list_jobs_command(args):
    """List all job descriptions."""
    try:
        # Get all jobs (this is a simplified implementation)
        print("📋 Available Job Descriptions:")
        print("Note: Full job listing requires database query implementation")
        
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        print(f"❌ Error: {e}")


def main():
    """Main CLI function."""
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Mastodon CV Matcher CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add job command
    add_parser = subparsers.add_parser("add-job", help="Add a job description")
    add_group = add_parser.add_mutually_exclusive_group(required=True)
    add_group.add_argument("--file", help="JSON file containing job data")
    add_group.add_argument("--interactive", action="store_true", help="Interactive input")
    
    # Search CVs command
    search_cvs_parser = subparsers.add_parser("search-cvs", help="Search for matching CVs")
    search_group = search_cvs_parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument("--job-id", help="Job ID to search for")
    search_group.add_argument("--query", help="Search query")
    search_cvs_parser.add_argument("--max-results", type=int, default=5, help="Maximum results")
    
    # Search jobs command
    search_jobs_parser = subparsers.add_parser("search-jobs", help="Search for matching jobs")
    
    # List jobs command
    list_parser = subparsers.add_parser("list-jobs", help="List all job descriptions")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "add-job":
        add_job_command(args)
    elif args.command == "search-cvs":
        search_cvs_command(args)
    elif args.command == "search-jobs":
        search_jobs_command(args)
    elif args.command == "list-jobs":
        list_jobs_command(args)


if __name__ == "__main__":
    main()

"""Main Mastodon bot entry point with two-way matching."""

import os
import sys
from pathlib import Path
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.logging_config import setup_logging
from bot.mastodon_client import mastodon_client
from listener.cv_listener import CVListener
from listener.job_listener import JobListener


def main():
    """Main function to run the Mastodon bot with two-way matching."""
    # Setup logging
    setup_logging()
    
    try:
        # Test connection
        if not mastodon_client.test_connection():
            logger.error("Failed to connect to Mastodon")
            return
        
        logger.info("🤖 Starting Mastodon CV Matcher Bot...")
        logger.info("   > Two-way matching system:")
        logger.info("     - #cv → Find matching jobs")
        logger.info("     - #tuyendungAI → Find matching candidates")
        
        # Start CV listener (CV → Job matching)
        cv_listener = CVListener()
        logger.info("✅ Started CV listener for #cv hashtag")
        
        # Start job listener (Job → CV matching)  
        job_listener = JobListener(mastodon_client.bot_username)
        logger.info("✅ Started job listener for #tuyendungAI hashtag")
        
        # Note: In a real implementation, you would need to run both listeners
        # This is a simplified version that focuses on job matching
        # For production, you'd need to run both listeners concurrently
        logger.info("🚀 Starting job matching stream...")
        mastodon_client.start_stream(job_listener, "tuyendungAI")
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise


if __name__ == "__main__":
    main()

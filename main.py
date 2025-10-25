"""Main application entry point for Mastodon CV Matcher."""

import os
import sys
from pathlib import Path
from mastodon import Mastodon
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from utils.logging_config import setup_logging
from listeners.postCVListener import CVListener
from services.matching_service import matching_service


def main():
    """Main application function."""
    # Setup logging
    setup_logging()
    logger.info("Starting Mastodon CV Matcher Extension")
    
    try:
        # Initialize Mastodon client
        mastodon = Mastodon(
            access_token=settings.mastodon_access_token,
            api_base_url=settings.mastodon_instance_url
        )
        
        # Verify connection
        try:
            user_info = mastodon.me()
            logger.info(f"Connected to Mastodon as @{user_info['acct']}")
        except Exception as e:
            logger.error(f"Failed to connect to Mastodon: {e}")
            return
        
        # Initialize CV listener
        cv_listener = CVListener()
        
        # Start listening for CV posts
        logger.info("Starting to listen for CV posts with #cv hashtag...")
        mastodon.stream_public(cv_listener)
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise


if __name__ == "__main__":
    main()

"""Job post listener for #tuyendungAI hashtag."""

import re
import time
from mastodon import StreamListener
from loguru import logger

from logic.job_processor import process_job_post
from logic.candidate_matcher import find_matching_candidates
from utils.mastodon_utils import send_confirmation, send_candidate_results, send_error_message


class JobListener(StreamListener):
    """Listens for job posts with #tuyendungAI hashtag."""
    
    def __init__(self, bot_username: str):
        """Initialize job listener."""
        self.bot_username = bot_username
        self.listen_hashtag = "tuyendungAI"
    
    def on_update(self, status):
        """Handle new status updates."""
        # Skip posts from the bot itself
        if status['account']['username'] == self.bot_username:
            return

        # Check if post contains the recruitment hashtag
        hashtags = [tag['name'] for tag in status['tags']]
        if self.listen_hashtag.lower() not in [h.lower() for h in hashtags]:
            return

        logger.info(f"🔥 Detected job post from @{status['account']['acct']}")

        # Extract job description text
        jd_text = self._extract_job_description(status['content'])
        if not jd_text:
            logger.warning("No job description text found")
            return

        # Get poster account info
        poster_account = status['account']

        # Send confirmation message
        send_confirmation(poster_account, status['id'])

        try:
            # Process the job description
            logger.info(f"Processing job description: {jd_text[:100]}...")
            
            # Find matching candidates
            candidates = find_matching_candidates(jd_text)
            
            # Send results to poster
            send_candidate_results(poster_account, candidates)

        except Exception as e:
            logger.error(f"Error processing job description: {e}")
            send_error_message(poster_account, f"Processing error: {str(e)}")
    
    def _extract_job_description(self, content: str) -> str:
        """Extract job description from post content."""
        # Remove HTML tags
        jd_text = re.sub(r'<.*?>', '', content).strip()
        # Remove the hashtag
        jd_text = jd_text.replace(f"#{self.listen_hashtag}", "").strip()
        # Remove extra whitespace
        jd_text = re.sub(r'\s+', ' ', jd_text)
        return jd_text if jd_text else None

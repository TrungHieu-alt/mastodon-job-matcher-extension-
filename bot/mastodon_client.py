"""Mastodon API client wrapper."""

import os
from mastodon import Mastodon
from loguru import logger


class MastodonClient:
    """Mastodon API client wrapper."""
    
    def __init__(self):
        """Initialize Mastodon client."""
        self.client = None
        self.bot_username = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Mastodon client connection."""
        try:
            self.client = Mastodon(
                client_id=os.getenv("MASTODON_CLIENT_KEY"),
                client_secret=os.getenv("MASTODON_CLIENT_SECRET"),
                access_token=os.getenv("MASTODON_ACCESS_TOKEN"),
                api_base_url=os.getenv("MASTODON_API_BASE_URL", "https://mastodonuet.duckdns.org/")
            )
            
            # Get bot information
            bot_info = self.client.me()
            self.bot_username = bot_info['username']
            logger.info(f"Mastodon client initialized for @{self.bot_username}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Mastodon client: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test Mastodon connection."""
        try:
            user_info = self.client.me()
            logger.info(f"Connected to Mastodon as @{user_info['acct']}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Mastodon: {e}")
            return False
    
    def post_status(self, content: str, visibility: str = 'public', in_reply_to_id: int = None) -> bool:
        """Post a status update."""
        try:
            self.client.status_post(
                content=content,
                visibility=visibility,
                in_reply_to_id=in_reply_to_id
            )
            logger.info(f"Posted status: {content[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Failed to post status: {e}")
            return False
    
    def start_stream(self, listener, hashtag: str):
        """Start streaming hashtag posts."""
        try:
            logger.info(f"Starting stream for hashtag: #{hashtag}")
            self.client.stream_hashtag(hashtag, listener, reconnect_async=True)
        except Exception as e:
            logger.error(f"Failed to start stream: {e}")
            raise


# Global Mastodon client instance
mastodon_client = MastodonClient()

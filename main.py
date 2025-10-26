import os
import time
from mastodon import Mastodon
from dotenv import load_dotenv
from listeners.postJDListener import RecruitmentListener

# --- Load config ---
load_dotenv()
MASTODON_CLIENT_KEY = os.getenv("MASTODON_CLIENT_KEY")
MASTODON_CLIENT_SECRET = os.getenv("MASTODON_CLIENT_SECRET")
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
MASTODON_API_BASE_URL = os.getenv("MASTODON_API_BASE_URL", "https://mastodonuet.duckdns.org/")
LISTEN_HASHTAG = "tuyendungAI"

# --- Khởi tạo API ---
mastodon = Mastodon(
    client_id=MASTODON_CLIENT_KEY,
    client_secret=MASTODON_CLIENT_SECRET,
    access_token=MASTODON_ACCESS_TOKEN,
    api_base_url=MASTODON_API_BASE_URL
)

# --- Run bot ---
if __name__ == "__main__":
    try:
        my_info = mastodon.me()
        print(f"🤖 Bot '{my_info['username']}' đang chạy...")
        print(f"   > Lắng nghe #{LISTEN_HASHTAG} trên {MASTODON_API_BASE_URL}")
        mastodon.stream_hashtag(LISTEN_HASHTAG, RecruitmentListener(mastodon, LISTEN_HASHTAG), reconnect_async=True)
    except Exception as e:
        print(f"❌ Lỗi khởi động bot: {e}")

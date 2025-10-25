"""CV post listener for #cv hashtag."""

import os
import uuid
import requests
from mastodon import StreamListener
from loguru import logger

from logic.resume_parser import parse_resume
from logic.cv_job_matcher import find_matching_jobs_for_cv
from db.cv_storage import save_cv_to_database
from utils.file_utils import create_temp_file, cleanup_temp_file
from utils.mastodon_utils import send_cv_confirmation, send_job_matches, send_cv_error


class CVListener(StreamListener):
    """Listens for CV posts with #cv hashtag."""
    
    def on_update(self, status):
        """Handle new status updates."""
        # 1️⃣ Filter posts with #cv hashtag
        hashtags = [t["name"].lower() for t in status["tags"]]
        if "cv" not in hashtags:
            return

        owner = status["account"]["acct"]
        post_url = status["url"]
        created_at = status["created_at"]
        attachments = status["media_attachments"]

        # Skip if no attachments
        if not attachments:
            logger.warning(f"@{owner} posted #cv but no attachments found")
            return

        logger.info(f"📥 Found #cv post from @{owner}")

        # 2️⃣ Download first attachment
        attachment = attachments[0]
        url = attachment["url"]
        ext = os.path.splitext(url)[1]
        tmp_path = create_temp_file(owner, ext)

        try:
            # Download file
            r = requests.get(url)
            with open(tmp_path, "wb") as f:
                f.write(r.content)

            # 3️⃣ Parse CV and save to database
            cv_data = parse_resume(tmp_path)
            cv_data["posted_at"] = created_at
            
            cv_id = save_cv_to_database(cv_data, owner, post_url)
            
            if cv_id:
                logger.info(f"✅ Successfully saved CV for @{owner} (ID: {cv_id})")
                
                # 4️⃣ Find matching jobs for this CV
                self._find_and_send_job_matches(cv_data, owner, status["id"])
            else:
                logger.error(f"❌ Failed to save CV for @{owner}")
                send_cv_error(owner, "Failed to process CV")
                
        except Exception as e:
            logger.error(f"❌ Error processing CV for @{owner}: {e}")
            send_cv_error(owner, f"Error processing CV: {str(e)}")
        finally:
            # 5️⃣ Clean up temp file
            cleanup_temp_file(tmp_path)
    
    def _find_and_send_job_matches(self, cv_data: dict, owner: str, status_id: int):
        """Find matching jobs for the CV and send results."""
        try:
            # Send confirmation message
            send_cv_confirmation(owner, status_id)
            
            # Find matching jobs
            matching_jobs = find_matching_jobs_for_cv(cv_data, max_jobs=5)
            
            if matching_jobs:
                logger.info(f"Found {len(matching_jobs)} matching jobs for @{owner}")
                send_job_matches(owner, matching_jobs)
            else:
                logger.info(f"No matching jobs found for @{owner}")
                send_job_matches(owner, [])  # Send "no matches" message
                
        except Exception as e:
            logger.error(f"Error finding job matches for @{owner}: {e}")
            send_cv_error(owner, f"Error finding job matches: {str(e)}")

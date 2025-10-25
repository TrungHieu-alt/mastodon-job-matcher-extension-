"""Mastodon API utilities."""

import time
from typing import List, Dict, Any
from loguru import logger

from bot.mastodon_client import mastodon_client


def send_confirmation(poster_account: Dict[str, Any], status_id: int):
    """Send confirmation message to the poster."""
    try:
        content = (
            f"@{poster_account['acct']} Đã nhận yêu cầu tuyển dụng. "
            f"Bắt đầu quá trình phân tích và sàng lọc. Vui lòng chờ kết quả trong DM!"
        )
        
        mastodon_client.post_status(
            content=content,
            visibility='public',
            in_reply_to_id=status_id
        )
        
        logger.info(f"Sent confirmation to @{poster_account['acct']}")
    except Exception as e:
        logger.error(f"Failed to send confirmation message: {e}")


def send_candidate_results(poster_account: Dict[str, Any], candidates: List[Dict[str, Any]]):
    """Send matching results to the poster."""
    try:
        if not candidates:
            send_no_candidates_message(poster_account)
            return
        
        # Send introduction message
        send_introduction_message(poster_account)
        time.sleep(1)
        
        # Send individual candidate messages
        for i, candidate in enumerate(candidates):
            send_candidate_message(poster_account, candidate, i + 1)
            time.sleep(1)  # Avoid rate limiting
        
        logger.info(f"Sent {len(candidates)} candidate results to @{poster_account['acct']}")
        
    except Exception as e:
        logger.error(f"Error sending matching results: {e}")


def send_no_candidates_message(poster_account: Dict[str, Any]):
    """Send message when no candidates found."""
    content = f"@{poster_account['acct']} Rất tiếc, không tìm thấy ứng viên phù hợp nào trong cơ sở dữ liệu."
    mastodon_client.post_status(content=content, visibility='direct')


def send_introduction_message(poster_account: Dict[str, Any]):
    """Send introduction message."""
    content = f"@{poster_account['acct']} ✅ Đã xử lý xong! Dưới đây là bảng xếp hạng các ứng viên phù hợp nhất:"
    mastodon_client.post_status(content=content, visibility='direct')


def send_candidate_message(poster_account: Dict[str, Any], candidate: Dict[str, Any], rank: int):
    """Send individual candidate message."""
    try:
        eval_data = candidate.get('llm_evaluation', {})
        name = candidate.get('name', 'N/A')
        owner = candidate.get('owner', 'Unknown')
        
        message = (
            f"🏆 HẠNG {rank}: {name} (@{owner})\n"
            f"Điểm: {eval_data.get('score', 'N/A')}/100\n"
            f"Đánh giá kinh nghiệm: {eval_data.get('experience_match', 'N/A')}\n\n"
            f"Lý do: {eval_data.get('rationale', 'N/A')}"
        )
        
        content = f"@{poster_account['acct']} {message}"
        mastodon_client.post_status(content=content, visibility='direct')
        
        logger.info(f"Sent candidate {rank}: {name}")
        
    except Exception as e:
        logger.error(f"Error sending candidate message: {e}")


def send_error_message(poster_account: Dict[str, Any], error_msg: str):
    """Send error message to poster."""
    try:
        content = f"@{poster_account['acct']} Rất tiếc, đã có lỗi xảy ra: {error_msg}. Vui lòng thử lại sau."
        mastodon_client.post_status(content=content, visibility='direct')
    except Exception as e:
        logger.error(f"Failed to send error message: {e}")


# CV-specific utility functions
def send_cv_confirmation(owner: str, status_id: int):
    """Send confirmation message for CV processing."""
    try:
        content = (
            f"@{owner} Đã nhận CV của bạn! "
            f"Đang phân tích và tìm kiếm công việc phù hợp. Vui lòng chờ kết quả trong DM!"
        )
        
        mastodon_client.post_status(
            content=content,
            visibility='public',
            in_reply_to_id=status_id
        )
        
        logger.info(f"Sent CV confirmation to @{owner}")
    except Exception as e:
        logger.error(f"Failed to send CV confirmation: {e}")


def send_job_matches(owner: str, matching_jobs: List[Dict[str, Any]]):
    """Send job matches to CV poster."""
    try:
        if not matching_jobs:
            send_no_jobs_message(owner)
            return
        
        # Send introduction message
        send_jobs_introduction_message(owner)
        time.sleep(1)
        
        # Send individual job messages
        for i, job in enumerate(matching_jobs):
            send_job_message(owner, job, i + 1)
            time.sleep(1)  # Avoid rate limiting
        
        logger.info(f"Sent {len(matching_jobs)} job matches to @{owner}")
        
    except Exception as e:
        logger.error(f"Error sending job matches: {e}")


def send_no_jobs_message(owner: str):
    """Send message when no matching jobs found."""
    content = f"@{owner} Rất tiếc, không tìm thấy công việc phù hợp nào cho CV của bạn. Hãy thử lại sau!"
    mastodon_client.post_status(content=content, visibility='direct')


def send_jobs_introduction_message(owner: str):
    """Send introduction message for job matches."""
    content = f"@{owner} ✅ Đã phân tích xong CV! Dưới đây là các công việc phù hợp nhất:"
    mastodon_client.post_status(content=content, visibility='direct')


def send_job_message(owner: str, job: Dict[str, Any], rank: int):
    """Send individual job message."""
    try:
        eval_data = job.get('llm_evaluation', {})
        job_metadata = job.get('metadata', {})
        job_title = job_metadata.get('title', 'Unknown Position')
        company = job_metadata.get('company', 'Unknown Company')
        
        message = (
            f"💼 CÔNG VIỆC {rank}: {job_title} tại {company}\n"
            f"Điểm phù hợp: {eval_data.get('score', 'N/A')}/100\n"
            f"Đánh giá kinh nghiệm: {eval_data.get('experience_match', 'N/A')}\n"
            f"Đánh giá học vấn: {eval_data.get('education_match', 'N/A')}\n\n"
            f"Lý do: {eval_data.get('rationale', 'N/A')}\n"
            f"Đề xuất: {eval_data.get('recommendation', 'N/A')}"
        )
        
        content = f"@{owner} {message}"
        mastodon_client.post_status(content=content, visibility='direct')
        
        logger.info(f"Sent job {rank}: {job_title}")
        
    except Exception as e:
        logger.error(f"Error sending job message: {e}")


def send_cv_error(owner: str, error_msg: str):
    """Send error message for CV processing."""
    try:
        content = f"@{owner} Rất tiếc, đã có lỗi xảy ra khi xử lý CV: {error_msg}. Vui lòng thử lại sau."
        mastodon_client.post_status(content=content, visibility='direct')
    except Exception as e:
        logger.error(f"Failed to send CV error message: {e}")

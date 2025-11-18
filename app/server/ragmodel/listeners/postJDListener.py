from mastodon import StreamListener
import re, time
from logics.matchingLogic import find_best_candidates

class RecruitmentListener(StreamListener):
    def __init__(self, mastodon, listen_hashtag):
        super().__init__()
        self.mastodon = mastodon
        self.LISTEN_HASHTAG = listen_hashtag

    def on_update(self, status):
        try:
            my_username = self.mastodon.me()['username']
            if status['account']['username'] == my_username:
                return
        except Exception as e:
            print(f"[ERR] Không thể xác thực bot: {e}")
            return

        hashtags = [tag['name'].lower() for tag in status['tags']]
        if self.LISTEN_HASHTAG.lower() not in hashtags:
            return

        print(f"🔥 Bài đăng mới từ @{status['account']['acct']}")
        jd_text = re.sub(r'<.*?>', '', status['content']).strip()
        jd_text = jd_text.replace(f"#{self.LISTEN_HASHTAG}", "").strip()

        poster_account = status['account']

        self.mastodon.status_post(
            f"@{poster_account['acct']} Đã nhận yêu cầu tuyển dụng. Vui lòng chờ kết quả trong DM!",
            in_reply_to_id=status['id']
        )

        try:
            print(f"   > Đang xử lý JD: {jd_text[:80]}...")
            final_ranking = find_best_candidates(jd_text)

            if not final_ranking:
                self.mastodon.status_post(
                    f"@{poster_account['acct']} Không tìm thấy ứng viên phù hợp.",
                    visibility='direct'
                )
                return

            self.mastodon.status_post(
                f"@{poster_account['acct']} ✅ Dưới đây là bảng xếp hạng ứng viên:",
                visibility='direct'
            )
            time.sleep(1)

            for i, result in enumerate(final_ranking):
                eval_data = result.get('detailed_evaluation', {})
                msg = (
                    f"🏆 HẠNG {i+1}: {result.get('name', 'N/A')}\n"
                    f"Điểm: {eval_data.get('score', 'N/A')}/100\n"
                    f"Kinh nghiệm: {eval_data.get('experience_match', 'N/A')}\n\n"
                    f"Lý do: {eval_data.get('rationale', 'N/A')}"
                )
                print(msg)
                self.mastodon.status_post(f"@{poster_account['acct']} {msg}", visibility='direct')
                print(f"   > Gửi xong Hạng {i+1}")
                time.sleep(1)
            
            print(f"✅ Hoàn tất gửi DM cho @{poster_account['acct']}")

        except Exception as e:
            print(f"❌ Lỗi xử lý JD: {e}")
            self.mastodon.status_post(
                f"@{poster_account['acct']} ❌ Đã có lỗi xảy ra, vui lòng thử lại sau.",
                visibility='direct'
            )

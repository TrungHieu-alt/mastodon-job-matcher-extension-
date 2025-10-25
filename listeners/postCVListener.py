from mastodon import StreamListener
from logic.resume_parser import parse_resume
from db.save_db import save_resume_to_chroma
import requests, os, uuid


class CVListener(StreamListener):
    def on_update(self, status):
        # 1️⃣ Lọc bài có hashtag #cv
        hashtags = [t["name"].lower() for t in status["tags"]]
        if "cv" not in hashtags:
            return

        owner = status["account"]["acct"]
        post_url = status["url"]
        created_at = status["created_at"]
        attachments = status["media_attachments"]

        # Không có file đính kèm thì bỏ qua
        if not attachments:
            print(f"⚠️ @{owner} đăng #cv nhưng không có file đính kèm.")
            return

        print(f"📥 Bắt được bài #cv từ @{owner}")

        # 2️⃣ Lấy file đầu tiên và tải vào temp folder - up cv chỉ được 1 file 
        attachment = attachments[0]
        url = attachment["url"]
        ext = os.path.splitext(url)[1]
        tmp_path = f"/tmp/{owner}_{uuid.uuid4().hex[:6]}{ext}"

        r = requests.get(url)
        with open(tmp_path, "wb") as f:
            f.write(r.content)

        # 3️⃣ Parse CV -> thêm metadata -> lưu DB
        cv_data = parse_resume(tmp_path)
        cv_data["posted_at"] = created_at
        save_resume_to_chroma(cv_data, owner=owner, source_url=post_url)

        # 4️⃣ Xoá file tạm
        os.remove(tmp_path)
        print(f"✅ Hoàn tất lưu CV cho @{owner}\n")

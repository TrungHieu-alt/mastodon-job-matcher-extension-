from mastodon import StreamListener
from logics.resumeParser import parse_resume
from db.saveDB import save_to_db
import requests, os, uuid, json

class postCVListener(StreamListener):
    def on_update(self, status):
        hashtags = [t["name"].lower() for t in status["tags"]]
        if "cv" not in hashtags:
            return

        owner = status["account"]["acct"]
        print(f"📥 Bắt được bài #cv từ @{owner}")

        for attachment in status["media_attachments"]:
            url = attachment["url"]
            ext = os.path.splitext(url)[1]
            tmp_path = f"/tmp/{uuid.uuid4().hex[:6]}{ext}"
            r = requests.get(url)
            with open(tmp_path, "wb") as f:
                f.write(r.content)

            parsed = parse_resume(tmp_path)
            parsed["uploader"] = owner
            save_to_db("cv", parsed)
            print(f"✅ Lưu CV của @{owner}")

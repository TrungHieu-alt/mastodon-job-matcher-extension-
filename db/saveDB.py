from db.collections import get_cv_collection
from logic.utils_text import create_embedding_content_from_json  # nếu m có hàm này
import uuid

def save_resume_to_chroma(cv_data: dict, owner: str, source_url: str = None):
    """
    Lưu một bản CV đã parse (cv_data) vào Chroma DB.
    """
    if not isinstance(cv_data, dict) or not cv_data:
        print("❌ Dữ liệu CV không hợp lệ, không thể lưu.")
        return None

    cv_data["owner"] = owner
    cv_data["source_url"] = source_url
    cv_data["id"] = f"cv_{owner}_{uuid.uuid4().hex[:8]}"

    # Tạo nội dung text để embedding
    from logic.utils_text import create_embedding_content_from_json
    embedding_text = create_embedding_content_from_json(cv_data)

    # Lấy collection Chroma
    collection = get_cv_collection()

    # Lưu vào DB
    collection.add(
        ids=[cv_data["id"]],
        documents=[embedding_text],
        metadatas=[cv_data]
    )

    print(f"✅ Đã lưu CV của {cv_data.get('name', 'N/A')} vào Chroma (owner={owner})")
    return cv_data["id"]

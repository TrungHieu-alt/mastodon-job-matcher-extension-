# li_adapter.py  ✅ fix metadata flatten for LlamaIndex >= 0.10.x

from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb, json
from typing import Dict, Any
from logics.embedder import json_to_text_auto

# --- Persistent Chroma client ---
_chroma_client = chromadb.PersistentClient(path="chroma_db")

# --- Embedding model setup ---
_embed = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# --- Global settings ---
Settings.embed_model = _embed
Settings.chunk_size = 512


# Internal helper
def _get_vector_store(collection_name: str) -> ChromaVectorStore:
    collection = _chroma_client.get_or_create_collection(collection_name)
    return ChromaVectorStore(chroma_collection=collection)


# =======================================================
# 🧠 Public API
# =======================================================

def upsert_json_doc(collection_name: str, data: Dict[str, Any], metadata: Dict[str, Any]) -> str:
    """
    Convert JSON → text → embed → upsert vào Chroma (qua LlamaIndex).
    Metadata giờ phải là flat dict (str, int, float, None)
    """
    text = json_to_text_auto(data)
    if not text.strip():
        raise ValueError("Empty text after JSON conversion")

    vector_store = _get_vector_store(collection_name)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # ✅ flatten _raw_json để tránh lỗi ValueError
    flat_meta = metadata.copy()
    flat_meta["_raw_json"] = json.dumps(data, ensure_ascii=False)

    doc = Document(text=text, metadata=flat_meta)

    index = VectorStoreIndex.from_documents(
        [doc],
        storage_context=storage_context,
        show_progress=False,
    )

    storage_context.persist()
    print(f"✅ Indexed document into '{collection_name}' | meta: {metadata.get('filename','N/A')}")
    return metadata.get("external_id", "")


def query_topk(collection_name: str, query_text: str, top_k: int = 10):
    """
    Query top-k similar nodes using LlamaIndex + Chroma.
    """
    vector_store = _get_vector_store(collection_name)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
    )

    qe = index.as_query_engine(similarity_top_k=top_k)
    resp = qe.query(query_text)
    return resp.source_nodes  # list[NodeWithScore]

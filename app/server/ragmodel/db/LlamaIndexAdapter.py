# ======================================================
#        CHROMA MULTI-FIELD VECTOR STORE (FINAL)
# ======================================================

import chromadb
import numpy as np
import json
from typing import Dict, Any, List

chroma = chromadb.PersistentClient(path="chroma_multi")

# 5 collections cho 5 field
CV_COLLECTIONS = {
    "summary": chroma.get_or_create_collection("cv_summary"),
    "skills": chroma.get_or_create_collection("cv_skills"),
    "experience": chroma.get_or_create_collection("cv_experience"),
    "projects": chroma.get_or_create_collection("cv_projects"),
    "full": chroma.get_or_create_collection("cv_full"),
}

JD_COLLECTIONS = {
    "description": chroma.get_or_create_collection("jd_description"),
    "skills": chroma.get_or_create_collection("jd_skills"),
    "responsibilities": chroma.get_or_create_collection("jd_responsibilities"),
    "techstack": chroma.get_or_create_collection("jd_techstack"),
    "full": chroma.get_or_create_collection("jd_full"),
}


# ======================================================
#  UP SERT CV
# ======================================================

def upsert_cv(cv_id: str, cv_json: Dict[str, Any], cv_emb: Dict[str, np.ndarray]):
    """
    cv_emb keys:
        emb_summary, emb_skills, emb_experience, emb_projects, emb_full
    """
    CV_COLLECTIONS["summary"].upsert(
        ids=[f"{cv_id}_summary"],
        embeddings=[cv_emb["emb_summary"].tolist()],
        metadatas=[{"cv_id": cv_id}]
    )
    CV_COLLECTIONS["skills"].upsert(
        ids=[f"{cv_id}_skills"],
        embeddings=[cv_emb["emb_skills"].tolist()],
        metadatas=[{"cv_id": cv_id}]
    )
    CV_COLLECTIONS["experience"].upsert(
        ids=[f"{cv_id}_experience"],
        embeddings=[cv_emb["emb_experience"].tolist()],
        metadatas=[{"cv_id": cv_id}]
    )
    CV_COLLECTIONS["projects"].upsert(
        ids=[f"{cv_id}_projects"],
        embeddings=[cv_emb["emb_projects"].tolist()],
        metadatas=[{"cv_id": cv_id}]
    )
    CV_COLLECTIONS["full"].upsert(
        ids=[f"{cv_id}_full"],
        embeddings=[cv_emb["emb_full"].tolist()],
        metadatas=[{"cv_id": cv_id, "_raw_json": json.dumps(cv_json)}]
    )

    print(f"✅ Upserted CV {cv_id} (5 vectors)")


# ======================================================
#  UP SERT JD
# ======================================================

def upsert_jd(jd_id: str, jd_json: Dict[str, Any], jd_emb: Dict[str, np.ndarray]):
    JD_COLLECTIONS["description"].upsert(
        ids=[f"{jd_id}_description"],
        embeddings=[jd_emb["emb_description"].tolist()],
        metadatas=[{"jd_id": jd_id}]
    )
    JD_COLLECTIONS["skills"].upsert(
        ids=[f"{jd_id}_skills"],
        embeddings=[jd_emb["emb_required_skills"].tolist()],
        metadatas=[{"jd_id": jd_id}]
    )
    JD_COLLECTIONS["responsibilities"].upsert(
        ids=[f"{jd_id}_responsibilities"],
        embeddings=[jd_emb["emb_responsibilities"].tolist()],
        metadatas=[{"jd_id": jd_id}]
    )
    JD_COLLECTIONS["techstack"].upsert(
        ids=[f"{jd_id}_techstack"],
        embeddings=[jd_emb["emb_techstack"].tolist()],
        metadatas=[{"jd_id": jd_id}]
    )
    JD_COLLECTIONS["full"].upsert(
        ids=[f"{jd_id}_full"],
        embeddings=[jd_emb["emb_full"].tolist()],
        metadatas=[{"jd_id": jd_id, "_raw_json": json.dumps(jd_json)}]
    )

    print(f"✅ Upserted JD {jd_id} (5 vectors)")


# ======================================================
#  GET ALL (for brute-force)
# ======================================================

def get_all_cv_ids() -> List[str]:
    ids = set()
    for col in CV_COLLECTIONS.values():
        for m in col.get(include=["metadatas"])["metadatas"]:
            ids.add(m["cv_id"])
    return list(ids)


def get_all_jd_ids() -> List[str]:
    ids = set()
    for col in JD_COLLECTIONS.values():
        for m in col.get(include=["metadatas"])["metadatas"]:
            ids.add(m["jd_id"])
    return list(ids)


# ======================================================
#  QUERY single field (summary, skills, ...)
# ======================================================

def query_cv_field(field: str, vector: np.ndarray, top_k=5):
    col = CV_COLLECTIONS[field]
    res = col.query(query_embeddings=[vector.tolist()], n_results=top_k)
    return res

def query_jd_field(field: str, vector: np.ndarray, top_k=5):
    col = JD_COLLECTIONS[field]
    res = col.query(query_embeddings=[vector.tolist()], n_results=top_k)
    return res

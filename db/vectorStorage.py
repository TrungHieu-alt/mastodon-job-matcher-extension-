from LlamaIndexAdapter import upsert_json_doc, query_topk

def add_document(collection_name: str, data: dict, metadata: dict):
    return upsert_json_doc(collection_name, data, metadata)

def query_collection(collection_name: str, query_text: str, top_k=3):
    return query_topk(collection_name, query_text, top_k)

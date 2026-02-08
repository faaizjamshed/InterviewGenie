import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
stored_resumes = []

def index_resumes(processed_data):
    global index, stored_resumes
    stored_resumes = processed_data
    texts = [item['text'] for item in processed_data]
    embeddings = model.encode(texts)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))

def search_best_candidates(job_description, top_k=5):
    global index, stored_resumes
    if index is None or not stored_resumes:
        return []

    query_vector = model.encode([job_description])
    distances, indices = index.search(np.array(query_vector).astype('float32'), top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1 and idx < len(stored_resumes):
            # Distance ko 0-100 score mein convert karna
            score = max(0, min(100, 100 - distances[0][i]))
            results.append({
                "filename": stored_resumes[idx]['filename'],
                "score": round(float(score), 2)
            })
    return results
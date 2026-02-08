import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Model load (Small & Fast)
model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
stored_resumes = []

def index_resumes(processed_data):
    global index, stored_resumes
    stored_resumes = processed_data
    
    # Text ko numbers (embeddings) mein convert karna
    texts = [item['text'] for item in processed_data]
    embeddings = model.encode(texts)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))

def search_best_candidates(job_description, top_k=5):
    global index, stored_resumes
    if index is None or not stored_resumes:
        return []

    # Job description ko vector banana
    query_vector = model.encode([job_description])
    
    # Search top candidates
    distances, indices = index.search(np.array(query_vector).astype('float32'), top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1 and idx < len(stored_resumes):
            # Distance ko percentage score mein badalna
            raw_score = distances[0][i]
            # FAISS distance L2 hai, score jitna kam utna behtar (inverted logic)
            final_score = max(50, 100 - (raw_score * 10)) 
            
            results.append({
                "filename": stored_resumes[idx]['filename'],
                "score": round(float(min(99, final_score)), 2)
            })
            
    # Score ke hisab se sort karna
    return sorted(results, key=lambda x: x['score'], reverse=True)
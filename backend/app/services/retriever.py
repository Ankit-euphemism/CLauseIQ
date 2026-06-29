import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import settings
"""
Retriever service for finding similar chunks based on a question.
"""
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") # Fast + good quality

def retrieve_chunks(question: str, index, chunks: list[str]) -> list[str]:
    """Embed question → find top-k closest chunks from FAISS."""
    q_embedding = np.asarray(model.encode([question]), dtype="float32")
    distances, indices = index.search(q_embedding, settings.top_k)

    results = []
    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])
    return results
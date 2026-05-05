import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.vectors = []
        self.metadata = []

    def add(self, vector, meta):
        self.index.add(np.array([vector]))
        self.vectors.append(vector)
        self.metadata.append(meta)

    def search(self, query_vector, k=3):
        distances, indices = self.index.search(
            np.array([query_vector]), k
        )
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

from Tools.EmbedSys import EmbedSys
import numpy as np
import faiss
import os
import pickle

class RagTool :
    def __init__(self, vector_db_path="./VectorDb"):

        self.index = faiss.read_index(os.path.join(vector_db_path, "index.faiss"))
        with open(os.path.join(vector_db_path, "documents.pkl"), "rb") as f:
            self.KB = pickle.load(f)

        self.embed_model = EmbedSys()


    def get_rag_context(self, queries, top_k=5, threshold=0.5):
        answer = {}
        for query in queries:
            query_embedding = np.array([self.embed_model(query)])

            # Search in FAISS
            similarities, top_indices = self.index.search(query_embedding, top_k)

            chunks = []
            for sim, idx in zip(similarities[0], top_indices[0]):
                if sim >= threshold:      # <--- APPLY THRESHOLD HERE
                    chunks.append(self.KB[idx].page_content)

            answer[query] = "\n\n".join(chunks) if chunks else ""

        return answer

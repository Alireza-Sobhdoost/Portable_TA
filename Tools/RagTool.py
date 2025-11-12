from Tools.EmbedSys import EmbedSys
import numpy as np
import faiss
import os
import pickle

class RagTool :
    def __init__(self, vector_db_path="./VectorDB"):

        self.index = faiss.read_index(os.path.join(vector_db_path, "index.faiss"))
        with open(os.path.join(vector_db_path, "documents.pkl"), "rb") as f:
            self.KB = pickle.load(f)

        self.embed_model = EmbedSys()


    def get_rag_context(self, query, top_k=5):
        query_embedding = self.embed_model(query)
        query_embedding = np.array([query_embedding])
        _, top_indices = self.index.search(query_embedding, top_k)
        top_chunks = [self.KB[i].page_content for i in top_indices[0]]
        return "\n\n".join(top_chunks)
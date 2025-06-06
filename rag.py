from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import numpy as np
import os
import pickle

embed = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1",
    trust_remote_code=True
)

def load_documents(folder_path: str):
    texts = []
    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        if file.endswith(".txt"):
            docs = TextLoader(path).load()
            # TextLoader returns list of Document objects; extract text
            texts.extend([doc.page_content for doc in docs])
        elif file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs = loader.load()
            # Extract text from each page/document object
            texts.extend([doc.page_content for doc in docs])
    return texts

folder_path = "./teaching/books"  # Your folder with PDFs and/or txt files
documents = load_documents(folder_path)

print(f"Loaded {len(documents)} text chunks from documents")

# Now embed documents, which is a list of strings
doc_embeddings = np.array(embed.encode(documents, normalize_embeddings=True, batch_size=8))
if doc_embeddings.ndim == 3:
    doc_embeddings = doc_embeddings.squeeze(1)
# Save both documents and embeddings
with open("./teaching/teaching.pkl", "wb") as f:
    pickle.dump({
        "documents": documents,
        "embeddings": doc_embeddings
    }, f)
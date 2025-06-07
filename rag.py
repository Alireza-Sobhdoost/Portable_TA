import os
import pickle
import numpy as np
import faiss

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def build_vector_db(folder_path, embedding_model_name, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Load model
    embed_model = SentenceTransformer(embedding_model_name, trust_remote_code=True)

    # Load and chunk documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_chunks = []

    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            docs = TextLoader(path).load()
        elif filename.endswith(".pdf"):
            docs = PyPDFLoader(path).load()
        else:
            continue

        for doc in docs:
            doc.metadata["source"] = filename

        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)

    print(f"✅ Loaded and split into {len(all_chunks)} chunks.")

    # Get texts for embedding
    texts = [doc.page_content for doc in all_chunks]

    # Embed
    print("🔍 Embedding...")
    embeddings = embed_model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=True)
    embeddings = np.array(embeddings)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    # Save index and data
    faiss.write_index(index, os.path.join(output_dir, "index.faiss"))

    with open(os.path.join(output_dir, "documents.pkl"), "wb") as f:
        pickle.dump(all_chunks, f)

    print("✅ Saved FAISS index and documents.")

# Usage
build_vector_db(
    folder_path="./teaching/books",
    embedding_model_name="nomic-ai/nomic-embed-text-v1",
    output_dir="./teaching/vector_db"
)

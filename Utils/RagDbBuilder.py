import os
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

# ==================================================================
# 1. Embedding Model (GPU)
# ==================================================================
embed = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v1",
    trust_remote_code=True,
    device="cuda"
)
dim = embed.get_sentence_embedding_dimension()

# ==================================================================
# 2. Chunking
# ==================================================================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len
)

# ==================================================================
# 3. Load existing FAISS + documents.pkl
# ==================================================================
pkl_path = "./VectorDb/documents.pkl"
faiss_path = "./VectorDb/index.faiss"

if os.path.exists(pkl_path):
    print("Loading existing documents.pkl ...")
    with open(pkl_path, "rb") as f:
        old_documents = pickle.load(f)
else:
    print("No previous dataset found. Starting fresh...")
    old_documents = []

if os.path.exists(faiss_path):
    print("Loading existing FAISS index ...")
    index = faiss.read_index(faiss_path)
else:
    print("Creating new FAISS index ...")
    index = faiss.IndexFlatIP(dim)  # cosine similarity

# ==================================================================
# 4. Load new files and create chunks
# ==================================================================
def load_new_documents(folder_path: str):
    new_chunks = []

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file.endswith(".txt"):
            docs = TextLoader(path).load()
        elif file.endswith(".pdf"):
            docs = PyPDFLoader(path).load()
        else:
            continue

        for doc in docs:
            doc.metadata["source"] = file
            chunks = splitter.split_documents([doc])
            new_chunks.extend(chunks)

    return new_chunks

folder_path = "./books"
new_chunks = load_new_documents(folder_path)
print(f"Loaded {len(new_chunks)} new chunks.")

# ==================================================================
# 5. Embed new chunks (GPU + batching)
# ==================================================================
BATCH_SIZE = 64
def embed_in_batches(docs):
    texts = [doc.page_content for doc in docs]
    embeddings = []
    
    for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Embedding batches"):
        batch = texts[i:i+BATCH_SIZE]
        emb = embed.encode(
            batch,
            convert_to_numpy=True,
            normalize_embeddings=True,
            device="cuda"
        )
        embeddings.append(emb)
    
    return np.vstack(embeddings) if embeddings else np.zeros((0, dim))

if new_chunks:
    print("Embedding new chunks on GPU...")
    new_embeddings = embed_in_batches(new_chunks)
else:
    new_embeddings = np.zeros((0, dim))

print("New embeddings shape:", new_embeddings.shape)

# ==================================================================
# 6. Append to FAISS + pickle
# ==================================================================
if len(new_chunks) > 0:
    # Append chunks to old documents
    updated_documents = old_documents + new_chunks

    # Add new embeddings to FAISS
    index.add(new_embeddings.astype("float32"))

    # Save updated pickle
    with open(pkl_path, "wb") as f:
        pickle.dump(updated_documents, f)

    # Save updated FAISS index
    faiss.write_index(index, faiss_path)

    print(f"✅ Added {len(new_chunks)} new chunks.")
    print(f"FAISS index now contains {index.ntotal} vectors.")
else:
    print("No new chunks found. Nothing updated.")

print("🔥 Update complete!")

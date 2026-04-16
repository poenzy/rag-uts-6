import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. Konfigurasi (Agar memenuhi syarat UTS) 
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def load_pdf(file_path):
    # Logika membaca PDF [cite: 65, 68]
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def manual_splitter(text, size, overlap):
    # Logika chunking manual [cite: 37, 66]
    chunks = []
    # Implementasikan loop untuk memotong teks di sini
    return chunks

# 2. Proses Indexing [cite: 60, 71, 73]
def create_index(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    
    # Inisialisasi FAISS 
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Simpan index secara lokal 
    faiss.write_index(index, "data/vector_db.index")
    # Simpan teks chunks ke file terpisah untuk referensi saat query
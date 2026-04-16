import os
import json
import numpy as np
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Konfigurasi Chunking (Sesuai rubrik UTS)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def read_documents(data_dir):
    """Membaca semua file PDF dan TXT di folder data/"""
    text_data = []
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.endswith('.pdf'):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            text_data.append({"source": filename, "text": text})
        elif filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            text_data.append({"source": filename, "text": text})
    return text_data

def chunk_text(text_data, chunk_size, overlap):
    """Memotong teks manual (From Scratch)"""
    chunks = []
    for doc in text_data:
        text = doc['text']
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_content = text[start:end]
            chunks.append({
                "source": doc['source'],
                "text": chunk_content
            })
            start += chunk_size - overlap
    return chunks

def build_vector_db():
    print("1. Membaca dokumen...")
    raw_docs = read_documents("data")
    
    print("2. Memotong teks (Chunking)...")
    chunks = chunk_text(raw_docs, CHUNK_SIZE, CHUNK_OVERLAP)
    
    print("3. Mengubah teks jadi vektor (Embedding)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_texts = [c['text'] for c in chunks]
    embeddings = model.encode(chunk_texts)
    
    print("4. Menyimpan ke FAISS Vector DB...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Buat folder jika belum ada
    os.makedirs("vector_db", exist_ok=True)
    
    # Simpan Index
    faiss.write_index(index, "vector_db/agri_index.faiss")
    
    # Simpan teks asli agar AI bisa membacanya nanti
    with open("vector_db/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)
        
    print(f"Selesai! {len(chunks)} potongan teks berhasil disimpan.")

if __name__ == "__main__":
    build_vector_db()
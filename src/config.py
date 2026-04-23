# src/config.py

# Konfigurasi Chunking (Optimasi untuk Pencarian Mendalam)
# Ukuran potongan teks yang lebih besar menjaga alur konteks paragraf.
CHUNK_SIZE = 1500 
CHUNK_OVERLAP = 400 

# Konfigurasi Pencarian (Retrieval)
# Mengambil lebih banyak potongan dokumen agar LLM memiliki referensi yang kaya.
TOP_K = 10

MODEL_NAME = "gemini-3-flash-preview"

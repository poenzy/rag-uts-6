import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv
from src.config import TOP_K, MODEL_NAME

# Load API Key dari .env
load_dotenv()

# Inisialisasi client Gemini (NEW API)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Embedding model tetap
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def load_db():
    index = faiss.read_index("vector_db/agri_index.faiss")
    with open("vector_db/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return index, chunks

def get_answer(user_query, top_k=TOP_K):
    try:
        index, chunks = load_db()
    except:
        return "Error: Database belum dibuat. Jalankan indexing.py terlebih dahulu.", []

    # 1. Embedding
    query_vector = embed_model.encode([user_query])

    # 2. Similarity search
    distances, indices = index.search(np.array(query_vector).astype('float32'), top_k)

    retrieved_chunks = []
    context_text = ""
    for i, idx in enumerate(indices[0]):
        chunk = chunks[idx]
        chunk_with_score = chunk.copy()
        chunk_with_score['score'] = float(distances[0][i])
        retrieved_chunks.append(chunk_with_score)
        context_text += f"\nSumber: {chunk['source']}\nIsi: {chunk['text']}\n"

    # 3. Prompt (Dioptimasi agar lebih cerdas)
    prompt = f"""Kamu adalah "CultivaGuide", Asisten Ahli Pertanian yang profesional.
Tugasmu adalah menjawab pertanyaan pengguna berdasarkan konteks dokumen yang diberikan di bawah ini. 

Gunakan konteks tersebut sebagai referensi utama. Jika jawaban tidak ditemukan secara eksplisit tetapi bisa disimpulkan dari informasi yang ada, berikan jawaban yang logis. 
Namun, jika benar-benar tidak ada kaitan sama sekali dengan dokumen, katakan: "Maaf, informasi tersebut tidak ada dalam dokumen panduan."

Konteks Dokumen:
{context_text}

Pertanyaan Pengguna: {user_query}

Berikan jawaban yang jelas, terstruktur (gunakan bullet points jika perlu), dan sebutkan nama file sumbernya di bagian akhir jawaban.
"""

    # 4. CALL GEMINI
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text, retrieved_chunks
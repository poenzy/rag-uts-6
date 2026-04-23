"""
=============================================================
ANTARMUKA STREAMLIT — RAG UTS Data Engineering
=============================================================

Jalankan dengan: streamlit run ui/app.py
=============================================================
"""

import sys
import os
from pathlib import Path

# Mencari jalur folder utama (Project Root)
# Karena file ini ada di 'ui/app.py', parents[1] adalah root proyek
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

# Masukkan folder root ke dalam urutan pertama sys.path
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Sekarang baru panggil library lainnya
import streamlit as st
from src.query import get_answer
from dotenv import load_dotenv

load_dotenv()

# ─── Konfigurasi Halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="CultivaGuide — Asisten Pertanian",
    page_icon="🌱",
    layout="wide"
)

# ─── Kustomisasi CSS (Aura Tenang Biru Pastel) ───────────────────────────────
st.markdown("""
<style>
    /* Latar belakang utama (Hijau sangat pucat) */
    .stApp {
        background-color: #F4FDF4;
    }
    
    /* Warna Sidebar (Hijau pastel kalem) */
    [data-testid="stSidebar"] {
        background-color: #E8F8E8 !important;
        border-right: 2px solid #D6F0D6;
    }
    
    /* Warna teks (Hijau gelap keabu-abuan agar nyaman dibaca) */
    h1, h2, h3, h4, p, span, div {
        color: #2E4030;
    }
    
    /* Warna tombol utama */
    .stButton>button {
        background-color: #8CD996;
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #72C97E;
        color: white;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Warna area chat pengguna */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 15px;
        border: 1px solid #E6F9E8;
    }
    
    /* Mempercantik kotak input chat di bawah */
    .stChatInputContainer {
        border: 1px solid #8CD996 !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🌱 CultivaGuide")
st.caption("Asisten Ahli Pertanian yang siap membantu menjawab pertanyaanmu.")
st.divider()

# ─── Sidebar: Info & Konfigurasi ─────────────────────────────────────────────
with st.sidebar:
    st.header("Konfigurasi")
    
    top_k = st.slider(
        "Jumlah dokumen relevan (top-k)",
        min_value=1, max_value=10, value=3,
        help="Berapa banyak chunk yang diambil dari vector database"
    )
    
    show_context = st.checkbox("Tampilkan konteks yang digunakan", value=True)
    
    st.divider()
    st.header("Info Sistem")
    
    st.markdown("""
    **Kelompok:** Alvin, Fachrozi, Hanif 
    **Domain:** Pertanian
    **LLM:** Gemini (gemini-3-flash-preview)
    **Vector DB:** FAISS  
    **Embedding:** all-MiniLM-L6-v2
    """)
    
    st.divider()
    st.info("💡 Tip: Mulai dengan menanyakan seputar panduan pertanian kepada CultivaGuide.")


# ─── Load Vector Store (Cek DB) ────────────────────────────────────────────────
@st.cache_resource
def check_db():
    """Cek vector store sekali saja."""
    try:
        from src.query import load_db
        load_db()
        return None
    except Exception as e:
        return f"Error: {e}"


# ─── Main Content ──────────────────────────────────────────────────────────────
error = check_db()

if error:
    st.error(f" {error}")
    st.info("Jalankan terlebih dahulu: `python src/indexing.py`")
    st.stop()

# ─── Chat Interface ───────────────────────────────────────────────────────────
# Simpan riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Aku CultivaGuide. Ada yang bisa aku bantu seputar pertanian hari ini?"}
    ]

# Tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and show_context and "contexts" in msg:
            with st.expander("Konteks yang digunakan"):
                for i, ctx in enumerate(msg["contexts"], 1):
                    score_text = f" Skor relevansi: {ctx['score']:.4f}" if "score" in ctx else ""
                    st.markdown(f"**[{i}]{score_text}** | `{ctx.get('source', 'Unknown')}`")
                    st.text(ctx.get("text", "")[:300] + "...")
                    st.divider()

# Input pertanyaan baru
if question := st.chat_input("Ketik pesan untuk CultivaGuide di sini..."):
    
    # Tampilkan pertanyaan user
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    
    # Generate jawaban
    with st.chat_message("assistant"):
        with st.spinner("CultivaGuide sedang memikirkan jawaban..."):
            try:
                from src.query import get_answer
                # Kirim parameter top_k dari slider ke fungsi RAG
                answer, contexts = get_answer(question, top_k=top_k)
                
                if answer.startswith("Error:"):
                    st.error(answer)
                    st.stop()
                
                st.write(answer)
                
                # Tampilkan konteks jika diaktifkan
                if show_context:
                    with st.expander("📚 Konteks yang digunakan"):
                        for i, ctx in enumerate(contexts, 1):
                            score_text = f" Skor relevansi: {ctx['score']:.4f}" if "score" in ctx else ""
                            st.markdown(f"**[{i}]{score_text}** | `{ctx.get('source', 'Unknown')}`")
                            st.text(ctx.get("text", "")[:300] + "...")
                            st.divider()
                
                # Simpan ke riwayat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "contexts": contexts
                })
                
            except Exception as e:
                error_msg = f"Error: {e}\n\nPastikan API key sudah diatur di file .env"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# ─── Tombol Reset Chat ────────────────────────────────────────────────────────
if st.session_state.messages:
    if st.button("Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()
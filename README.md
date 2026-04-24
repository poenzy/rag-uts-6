# 🌱 CultivaGuide

---

## 👥 Identitas Kelompok

| Nama | NIM | Tugas Utama |
|------|-----|-------------|
| Achmad Alvin Al Fallah  | 244311031 | Data Analyst         |
| Fachrozi Rizky Wibowo   | 244311041 | Project Manager      |
| Mohammad Hanif Huda Afrizal  | 244311049 | Data Engineer        |

**Topik Domain:** *Pertanian*  
**Stack yang Dipilih:** *From Scratch*  
**LLM yang Digunakan:** *Gemini*  
**Vector DB yang Digunakan:** *FAISS*

---

## 🗂️ Struktur Proyek

```
cultivaguide/
├── .devcontainer/           # Konfigurasi development container
├── data/                    # Dokumen sumber pertanian (PDF, TXT)
│   ├── BUDIDAYA TANAMAN PADI.pdf
│   ├── Budidaya-cabe-di-perkotaan_watermark.pdf
│   └── Pedoman_Penanganan_Pascapanen_Sayuran.txt
├── data-backup/             # Backup dokumen sumber
├── evaluation/              # File evaluasi hasil pengujian
│   └── evaluasi.csv         # Tabel evaluasi pengujian pertanyaan
├── src/                     # Direktori source code utama
│   ├── config.py            # Konfigurasi aplikasi & LLM
│   ├── indexing.py          # Pipeline indexing dan chunking
│   └── query.py             # Pipeline query dan retrieval RAG
├── ui/                      # Direktori antarmuka pengguna
│   ├── app.py               # Antarmuka web menggunakan Streamlit
│   └── cli.py               # Antarmuka baris perintah (CLI)
├── vector_db/               # Penyimpanan database vektor FAISS lokal
├── venv/                    # Virtual environment Python
├── .env                     # Environment variables (tersimpan lokal)
├── .env.example             # Template environment variables
├── .gitignore               # Konfigurasi file yang diabaikan git
├── requirements.txt         # Daftar dependency package Python
└── README.md                # File dokumentasi utama proyek ini
```

---

## ⚡ Cara Memulai (Quickstart)

### 1. Clone & Setup

```bash
# Clone repository ini
git clone https://github.com/Poezy/rag-uts-6.git
cd rag-uts-6

# Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# atau 
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Konfigurasi API Key

```bash
# Salin template env
cp .env.example .env

# Edit .env dan isi API key Anda
# JANGAN commit file .env ke GitHub!
```

### 3. Siapkan Dokumen

Letakkan dokumen sumber Anda di folder `data/`:
```bash
# Contoh: salin PDF atau TXT ke folder data
cp dokumen-saya.pdf data/
```

### 4. Jalankan Indexing (sekali saja)

```bash
python src/indexing.py
```

### 5. Jalankan Sistem RAG

```bash
# Dengan Streamlit UI
streamlit run ui/app.py

# Atau via CLI
python ui/cli.py
```

---

## 🔧 Konfigurasi

Semua konfigurasi utama ada di `src/config.py` (atau langsung di setiap file):

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `CHUNK_SIZE` | 1500 | Ukuran setiap chunk teks (karakter) |
| `CHUNK_OVERLAP` | 400 | Overlap antar chunk |
| `TOP_K` | 10 | Jumlah dokumen relevan yang diambil |
| `MODEL_NAME` | `gemini-3-flash-preview` | Nama model LLM yang digunakan |

---

## 📊 Hasil Evaluasi

Detail hasil evaluasi dari 10 pertanyaan pengujian dapat dilihat secara lengkap pada file: [evaluation/evaluasi.csv](evaluation/evaluasi.csv)

**Rata-rata Skor:** 4.4  

**Analisis:** Berdasarkan hasil evaluasi, sistem RAG menunjukkan performa yang sangat baik dengan rata-rata skor 4.4 dari 5. Sistem mampu memberikan jawaban yang akurat, relevan, dan terstruktur sesuai dengan referensi dokumen (8 pertanyaan mendapatkan skor maksimal 5). Meskipun demikian, sistem memiliki kelemahan saat menangani pertanyaan yang memerlukan informasi sangat spesifik dari lampiran atau tabel (seperti indeks ketuaan dan kemasan perforasi), sehingga mengindikasikan perlunya penyempurnaan teknik *chunking* agar ekstraksi dari bagian dokumen yang terstruktur menjadi lebih presisi.

---

## 🏗️ Arsitektur Sistem



<img width="816" height="1600" alt="WhatsApp Image 2026-04-23 at 3 35 31 PM" src="https://github.com/user-attachments/assets/0e60f946-8d11-4e54-9079-b1165c5debd5" />



---

## 📚 Referensi & Sumber

- Framework: *From Scratch*
- LLM: *Gemini*
- Vector DB: *FAISS*
- Tutorial yang digunakan: Dokumentasi Streamlit, Langchain, dan FAISS

---

## 👨‍🏫 Informasi UTS

- **Mata Kuliah:** Data Engineering
- **Program Studi:** D4 Teknologi Rekayasa Perangkat Lunak
- **Deadline:** *23 April 2026*

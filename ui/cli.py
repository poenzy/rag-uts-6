import os
from query import get_answer

def main():
    # Tampilan Header Terminal
    print("="*60)
    print("🌱 CULTIVAGUIDE AI")
    print("="*60)

    # Looping interaksi tanya jawab
    while True:
        # 1. Mengambil input dari pengguna
        user_input = input("\nMasukkan pertanyaan: ")
        
        # Cek jika user ingin keluar dari program
        if user_input.lower() in ['keluar', 'exit', 'quit', 'q']:
            print("\n🌱 Terima kasih telah menggunakan CultivaGuide. Selamat bertani! \n")
            break
            
        # Lewati jika input kosong
        if not user_input.strip():
            continue

        print("\n🌱 Bentar lagi cari referensi di database dan merumuskan jawaban...")
        
        # 2. Panggil fungsi dari query.py
        answer, sources = get_answer(user_input)
        
        # 3. Tampilkan Jawaban AI
        print("\n" + "="*60)
        print("🌱 JAWABAN CULTIVAGUIDE:")
        print("-" * 60)
        print(answer)
        print("-" * 60)
        
        # 4. Tampilkan Sumber Dokumen (Untuk Bonus Poin UTS)
        if sources:
            print("📚 SUMBER REFERENSI:")
            for i, doc in enumerate(sources):
                print(f"[{i+1}] {doc['source']}")
                # Tampilkan 150 karakter pertama sebagai cuplikan bukti
                snippet = doc['text'][:150].replace('\n', ' ')
                print(f"    Kutipan: \"{snippet}...\"")
        print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Menangani jika user menekan Ctrl+C
        print("\n\nProgram dihentikan secara paksa. Sampai jumpa! 🌱")
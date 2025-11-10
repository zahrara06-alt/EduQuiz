import json
import os
import sys


LEADERBOARD_FILE = "leaderboard.json" 



def _get_file_path(filename):
    """Mendapatkan jalur file relatif terhadap lokasi leaderboar.py"""
    folder_saat_ini = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder_saat_ini, filename)

def load_json(filename):
    """Memuat data JSON dari file. Mengembalikan [] jika file kosong/rusak."""
    jalur_file = _get_file_path(filename)
    
    if not os.path.exists(jalur_file):
        return []
        
    try:
        with open(jalur_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception:
        return []

def save_json(filename, data):
    """Menyimpan data ke file JSON."""
    jalur_file = _get_file_path(filename)
    
    try:
        with open(jalur_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan data ke {filename}: {e}")


def simpan_skor(nama_pengguna, skor):
    """Menambahkan skor baru ke leaderboard."""
    entri_baru = {"nama": nama_pengguna, "skor": skor}
    
    data_leaderboard = load_json(LEADERBOARD_FILE)
    
    if not isinstance(data_leaderboard, list):
        data_leaderboard = [entri_baru]
    else:
        data_leaderboard.append(entri_baru)

    try:
        save_json(LEADERBOARD_FILE, data_leaderboard) 
        print(f"\n[INFO] Skor {skor} oleh {nama_pengguna} berhasil disimpan!")
    except Exception as e:
        print(f"\n[ERROR] Gagal menulis skor: {e}")


def tampilkan_leaderboard():
    """Menampilkan ranking user berdasarkan skor tertinggi."""
    os.system("cls" if os.name == "nt" else "clear") 
    print("\n" + "="*40)
    print("      🏆 LEADERBOARD SKOR TERTINGGI 🏆")
    print("="*40)

    data_leaderboard = load_json(LEADERBOARD_FILE)
    
    if not data_leaderboard or not isinstance(data_leaderboard, list):
        print("\nLeaderboard masih kosong. Belum ada skor yang tersimpan.")
        input("\nTekan ENTER untuk kembali ke Menu Utama...")
        return
        
    try:
        leaderboard_terurut = sorted(
            data_leaderboard, 
            key=lambda user: user.get('skor', 0),
            reverse=True
        )
    except Exception:
        print("\n[PERINGATAN] Error saat mengurutkan skor. Menampilkan data mentah.")
        leaderboard_terurut = data_leaderboard 
        
    top_10 = leaderboard_terurut[:10]

    if not top_10:
        print("\nLeaderboard kosong.")
    else:
        for rank, user in enumerate(top_10, 1):
            nama = user.get('nama', 'Anonim')
            skor = user.get('skor', 0)
            
            if rank == 1:
                gelar = "👑 Juara 1"
            elif rank == 2:
                gelar = "🥈 Juara 2"
            elif rank == 3:
                gelar = "🥉 Juara 3"
            else:
                gelar = f"Peringkat #{rank}"

            print("-" * 40)
            print(f"{gelar:<15}")
            print(f"  Nama Pengguna: {nama}")
            print(f"  Total Skor   : {skor}")

    print("\n" + "="*40)
    input("Tekan ENTER untuk kembali ke Menu Utama...")
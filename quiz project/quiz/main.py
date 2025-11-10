import json
import os
import sys 
from datetime import datetime

# ==========================================================
# === PENTING: PENGATURAN PATH UNTUK IMPOR MODULAR ===
# ==========================================================
# Solusi Paling Andal: Menavigasi 2 level ke atas untuk menemukan folder 'leaderboard'
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigasi ke atas 2 level untuk mencapai folder root EduQuiz (root/quiz project/quiz -> root)
    root_dir = os.path.dirname(os.path.dirname(current_dir)) 
    
    if root_dir not in sys.path:
        sys.path.append(root_dir)
        
except Exception as e:
    # Ini akan mencegah kegagalan total, tetapi fokus pada impor di bawah.
    print(f"DEBUG: Error setting sys.path: {e}")
    
# ==========================================================
# === IMPOR MODUL DAN FUNGSI ===
# ==========================================================

from quiz_saintek import SOAL

# === IMPOR LEADERBOARD TANPA TRY/EXCEPT ===
# Jika ini gagal, Python akan menampilkan error yang sebenarnya (ModuleNotFoundError)
from leaderboard import simpan_skor, tampilkan_leaderboard
# =========================================


# ==========================================================
# ======== SISTEM UTAMA: LOGIN, QUIZ, HISTORY ==============
# ==========================================================

# ----------------------
# FUNGSI JSON (Tidak ada perubahan)
# ----------------------
def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ----------------------
# SISTEM LOGIN / REGISTER (Tidak ada perubahan)
# ----------------------
def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

def register():
    print("\n=== REGISTER ===")
    users = load_users()
    username = input("Masukkan username baru: ")
    if any(u["username"] == username for u in users):
        print("❌ Username sudah digunakan.")
        return None
    password = input("Masukkan password: ")
    users.append({"username": username, "password": password, "role": "user"})
    save_users(users)
    print("✅ Akun berhasil dibuat!")
    return username

def login():
    print("\n=== LOGIN ===")
    users = load_users()
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    for u in users:
        if u["username"] == username and u["password"] == password:
            print(f"✅ Login berhasil! Selamat datang, {username} 👋")
            return {"username": username, "role": u.get("role", "user")}
    print("❌ Username atau password salah.")
    return None

# ==========================================================
# =============== SISTEM HISTORY TERINTEGRASI (Tidak ada perubahan) ==============
# ==========================================================

class HistorySystem:
    def __init__(self, current_user):
        self.current_user = current_user
        self.history_file = "data/history.json"

        os.makedirs("data", exist_ok=True)

    def add_history(self, activity, details=""):
        if not self.current_user:
            return
        history_data = load_json(self.history_file)
        history_entry = {
            "username": self.current_user["username"],
            "activity": activity,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "details": details
        }
        history_data.append(history_entry)
        save_json(self.history_file, history_data)

    def show_user_history(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n" + "=" * 50)
        print(f"           HISTORY - {self.current_user['username'].upper()}")
        print("=" * 50)

        history_data = load_json(self.history_file)
        user_history = [h for h in history_data if h["username"] == self.current_user["username"]]

        if not user_history:
            print("Belum ada riwayat aktivitas.")
            input("Tekan Enter untuk kembali ke menu...")
            return

        user_history.sort(key=lambda x: x["timestamp"], reverse=True)
        print(f"Total aktivitas: {len(user_history)}")
        print("-" * 50)

        for i, entry in enumerate(user_history[:10], 1):
            print(f"{i}. [{entry['timestamp']}] {entry['activity']}")
            if entry["details"]:
                print(f"  {entry['details']}")
        input("\nTekan Enter untuk kembali ke menu...")

# ==========================================================
# =================== SISTEM QUIZ SAINTEK (Diubah untuk Leaderboard) ==================
# ==========================================================

def jalankan_quiz(mapel, user, history_system):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"=== QUIZ {mapel.upper()} ===")

    soal_list = SOAL[mapel]
    skor = 0

    for i, s in enumerate(soal_list, start=1):
        print(f"\nSoal {i}: {s['soal']}")
        for pilihan in s["pilihan"]:
            print(pilihan)
        jawaban = input("Jawaban kamu (A/B/C/D): ").upper().strip()
        if jawaban == s["jawaban"]:
            print("✅ Benar!")
            skor += 1
        else:
            print(f"❌ Salah! Jawaban benar adalah {s['jawaban']}.")

    total = len(soal_list)
    persentase = (skor / total) * 100
    print("\n=== HASIL AKHIR ===")
    print(f"Skor kamu: {skor}/{total}")
    print(f"Persentase: {persentase:.1f}%")

    # === TAMBAHAN INTEGRASI LEADERBOARD ===
    skor_leaderboard = skor * 10 
    simpan_skor(user['username'], skor_leaderboard)
    # ======================================

    # Simpan ke history
    history_system.add_history(
        f"Menyelesaikan Quiz {mapel}",
        f"Skor: {skor}/{total} ({persentase:.1f}%)"
    )

    input("\nTekan Enter untuk kembali ke menu utama...")

# ==========================================================
# ====================== MENU UTAMA (Diubah untuk Leaderboard) ========================
# ==========================================================

def menu_utama(user):
    history_system = HistorySystem(user)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"=== MENU UTAMA (User: {user['username']}) ===")
        print("1. Quiz Saintek TKA")
        print("2. Lihat History")
        print("3. Lihat Leaderboard")
        print("4. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            print("\n=== PILIH MATA PELAJARAN ===")
            for i, mapel in enumerate(SOAL.keys(), start=1):
                print(f"{i}. {mapel}")
            print("0. Kembali")
            pilih = input("Pilih: ").strip()

            if pilih == "0":
                continue

            mapel_list = list(SOAL.keys())
            if pilih.isdigit() and 1 <= int(pilih) <= len(mapel_list):
                jalankan_quiz(mapel_list[int(pilih)-1], user, history_system)
            else:
                print("❌ Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")

        elif pilihan == "2":
            history_system.show_user_history()
            
        elif pilihan == "3":  # HANDLE OPSI LEADERBOARD
            tampilkan_leaderboard()
            
        elif pilihan == "4": 
            print("👋 Logout berhasil.")
            break
            
        else:
            print("⚠️ Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")

# ==========================================================
# ======================== MAIN (Tidak diubah) ============================
# ==========================================================

def main():
    print("=== SELAMAT DATANG DI PROGRAM QUIZ SAINTEK CLI ===")

    while True:
        print("\n1. Login")
        print("2. Register")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            user = login()
            if user:
                menu_utama(user)
        elif pilihan == "2":
            username = register()
            if username:
                menu_utama({"username": username, "role": "user"})
        elif pilihan == "0":
            print("Terima kasih telah menggunakan program ini! 👋")
            break
        else:
            print("⚠️ Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()
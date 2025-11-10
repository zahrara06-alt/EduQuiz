import json
import random
import os

# Baca file JSON berisi soal
def load_quiz_data(filename="latihan_soall.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Fungsi utama untuk menjalankan kuis
def run_quiz(quiz):
    score = 0
    total = len(quiz)
    random.shuffle(quiz)

    for i, q in enumerate(quiz, 1):
        print(f"\nSoal {i}/{total}: {q['question']}")
        for option in q["options"]:
            print(option)

        answer = input("Jawaban kamu (A/B/C/D): ").strip().upper()
        if answer == q["answer"]:
            print("✅ Benar!")
            score += 1
        else:
            print(f"❌ Salah. Jawaban yang benar adalah {q['answer']}")

    print(f"\n🎯 Skor akhir kamu: {score}/{total}")
    print(f"Persentase benar: {score/total*100:.1f}%")

# Menu utama
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("=== QUIZ SAINS TKA ===")
    print("1. Fisika")
    print("2. Kimia")
    print("3. Biologi")
    print("4. Matematika Wajib")
    pilihan_mapel = input("Pilih mata pelajaran (1/2): ").strip()

    if pilihan_mapel == "1":
        subject = "fisika"
    elif pilihan_mapel == "2":
        subject = "kimia"
    elif pilihan_mapel == "3":
        subject = "biologi"
    elif pilihan_mapel == "4":
        subject = "matematika wajib"
    else:
        print("Pilihan tidak valid.")
        return

    print("\nTingkat kesulitan:")
    print("1. Mudah")
    print("2. Sedang")
    print("3. Sulit")
    tingkat = input("Pilih tingkat kesulitan (1/2/3): ").strip()

    if tingkat == "1":
        level = "mudah"
    elif tingkat == "2":
        level = "sedang"
    elif tingkat == "3":
        level = "sulit"
    else:
        print("Pilihan tidak valid.")
        return

    data = load_quiz_data()
    if subject not in data or level not in data[subject]:
        print("Data soal tidak ditemukan.")
        return

    print(f"\nMulai kuis {subject.capitalize()} ({level.capitalize()}) 🔥\n")
    run_quiz(data[subject][level])

if __name__ == "__main__":
    main()
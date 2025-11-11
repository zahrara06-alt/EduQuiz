import google.generativeai as genai
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def clean_text (text):
    text = re.sub(r'\*{1,2}', '', text)
    text = re.sub(r'\$', '', text)
    text = re.sub(r'\\frac', '(', text)
    text = text.replace('\\', '')
    text = text.replace('**', '')
    text = text.replace('*', '-')
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()

def run_chatbot(username=None):
    genai.configure(api_key=API_KEY)
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    chat = model.start_chat(history=[{
        "role": "user",
        "parts": [
            "Mulai dari sekarang, kamu adalah 'Quizzy', chatbot edukasi untuk siswa SMA dalam mempersiapkan TKA SAINTEK.",
            "jawabanmu harus selalu rapi, terstruktur, dan mudah dipahami.",
            "gunakan format seperti ini:\n",
            "1️⃣ Langkah-langkah jelas\n",
            "💡 Rumus atau konsep penting diberi penjelasan singkat\n",
            "✅ Akhiri dengan kesimpulan atau hasil akhir.\n",
            "Gunakan markdown sederhana untuk menonjolkan poin penting, tetapi jangan terlalu banyak teks dekoratif."
        ]
    }])
    
    
    print("=" * 60)
    print(" 🤖  Welcome to Quizzy — where learning hits different. ")
    print("=" * 60)
    print("Hey there! I'm Quizzy, your quiz partner-in-crime. 🕵️")
    print("Ask me questions, test your brain, or just talk — I don’t mind being your study buddy.")
    print("Type 'exit' anytime if you’re done, but hey... winners don’t quit that easily 😉\n")

    while True :
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Quizzy: Catch you later, genius. 🫵😉")
            break
        
        try:
            if all(c in "0123456789+-*/(). " for c in user_input):
                print("Quizzy:", eval(user_input))
                continue
        except:
            pass

        response = chat.send_message(user_input)
        print("Quizzy:", clean_text(response.text))

if __name__ == "__main__":
    run_chatbot()
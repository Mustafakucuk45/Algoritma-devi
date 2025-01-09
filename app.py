import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
import requests

# OpenRouter API'yi entegre etme
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Mesaj gönderiliyor etiketi için güncelleme
def send_message():
    user_message = user_input.get()

    # Kullanıcı mesajını ekranda göster
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "You: " + user_message + "\n")
    chat_display.config(state=tk.DISABLED)

    # Scroll'u son mesaja odakla
    chat_display.see(tk.END)

    # "Mesaj Gönderiliyor..." yazısını göster
    status_label.config(text="Mesaj Gönderiliyor...", fg="blue")
    root.update()

    # API'ye istek gönder
    try:
        completion = client.chat.completions.create(
            model="google/learnlm-1.5-pro-experimental:free",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        bot_message = completion.choices[0].message.content
    except Exception as e:
        bot_message = "Error: " + str(e)

    # Bot cevabını ekranda göster
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Bot: " + bot_message + "\n")
    chat_display.config(state=tk.DISABLED)

    # Scroll'u son mesaja odakla
    chat_display.see(tk.END)

    # "Mesaj Gönderildi" yazısını göster
    status_label.config(text="Mesaj Gönderildi", fg="green")

    # Mesaj kutusunu temizle
    user_input.delete(0, tk.END)

# Pencerenin yeniden boyutlandırıldığında bileşenleri yeniden boyutlandırma
def resize_components(event):
    chat_display.config(width=event.width // 10, height=event.height // 30)
    user_input.config(width=event.width // 25)

# GUI ayarları
root = tk.Tk()
root.title("Chatbot")
root.configure(bg="#f0f0f0")  # Arka plan rengi
root.geometry("800x600")  # Başlangıç boyutu
root.minsize(600, 400)  # Minimum boyut

# Chat penceresi
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, bg="#ffffff", fg="#000000")
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Kullanıcı mesajı girecek alan
user_input = tk.Entry(root, bg="#e6e6e6", fg="#000000")
user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Gönder butonu
send_button = tk.Button(root, text="Send", command=send_message, bg="#4caf50", fg="white")
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Durum etiketi
status_label = tk.Label(root, text="", bg="#f0f0f0", fg="black")
status_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

# Satır ve sütunları genişletilebilir hale getirme
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

# Pencere boyutlandırma olayını bağlama
root.bind("<Configure>", resize_components)

# Tkinter arayüzünü başlat
root.mainloop()

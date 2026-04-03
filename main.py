import requests
from bs4 import BeautifulSoup
import time
import json
import os

# Telegram Bot Token ve Chat ID
TOKEN = "8761053450:AAEtCKoJdW5bgv5U7mVtKR_MdYzmcWaD-nM"
CHAT_ID = "6680927334"

# Kaydedilecek ilanların ID veya detayları
KAYIT_DOSYASI = "ilanlar.json"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

def load_previous_list():
    if os.path.exists(KAYIT_DOSYASI):
        with open(KAYIT_DOSYASI, "r") as f:
            return json.load(f)
    return []

def save_current_list(ilanlar):
    with open(KAYIT_DOSYASI, "w") as f:
        json.dump(ilanlar, f)

def fetch_listings():
    url = "https://www.sahibinden.com/samsun-kiralik-daire"  # Örnek link, kendi kriterlerinize göre değiştirin
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    ilanlar = []

    # Bu kısmı, sayfadaki ilanların HTML yapısına göre düzenlemeniz gerekebilir
    for ilan in soup.find_all("a", class_="classifiedTitle"):
        ilan_basligi = ilan.get_text(strip=True)
        ilan_link = "https://www.sahibinden.com" + ilan['href']
        ilan_id = ilan_link  # veya ilan içeriğinden farklı bir ID alınabilir
        ilanlar.append({
            "id": ilan_id,
            "baslik": ilan_basligi,
            "link": ilan_link
        })
    return ilanlar

def main():
    eski_ilanlar = load_previous_list()
    eski_ids = [ilan["id"] for ilan in eski_ilanlar]

    yeni_ilanlar = fetch_listings()

    # Yeni ilanları bul
    fark = [ilan for ilan in yeni_ilanlar if ilan["id"] not in eski_ids]

    if fark:
        for ilan in fark:
            mesaj = f"Yeni ilan!\n{ilan['baslik']}\n{ilan['link']}"
            send_telegram_message(mesaj)
        # Güncel listeyi kaydet
        save_current_list(yeni_ilanlar)
    else:
        print("Yeni ilan yok.")

if __name__ == "__main__":
    main()
send_telegram_message("Test mesajı: Script çalışıyor!")

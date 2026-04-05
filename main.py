import requests
from bs4 import BeautifulSoup
import json
import os

# ENV (Railway Variables kısmına bunları ekle)
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DB_FILE = "db.json"

# Kayıtlı ilanlar
try:
    with open(DB_FILE, "r") as f:
        seen = json.load(f)
except:
    seen = []

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

# ✅ HEPSIEMLAK (çalışma ihtimali yüksek)
def hepsiemlak():
    url = "https://www.hepsiemlak.com/samsun-kiralik"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ilanlar = soup.select(".list-view-item")

    print("Hepsiemlak ilan sayısı:", len(ilanlar))

    liste = []

    for ilan in ilanlar:
        try:
            baslik = ilan.select_one(".list-view-title").text.strip()
            fiyat = ilan.select_one(".list-view-price").text.strip()
            link = "https://www.hepsiemlak.com" + ilan.select_one("a")["href"]

            liste.append((baslik, fiyat, link))
        except:
            continue

    return liste

def gonder(ilanlar):
    global seen

    for b, f, l in ilanlar:
        if l in seen:
            continue

        mesaj = f"{b}\n💰 {f}\n{l}"
        print("GÖNDERİLİYOR:", mesaj)

        send_telegram(mesaj)
        seen.append(l)

    with open(DB_FILE, "w") as f:
        json.dump(seen, f)

def main():
    print("BOT BAŞLADI")

    ilanlar = []
    ilanlar += hepsiemlak()

    print("Toplam ilan:", len(ilanlar))

    if not ilanlar:
        print("İlan bulunamadı")
        return

    gonder(ilanlar)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("HATA:", e)

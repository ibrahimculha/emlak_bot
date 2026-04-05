import requests
import json
import os

TOKEN = os.getenv("8761053450:AAEtCKoJdW5bgv5U7mVtKR_MdYzmcWaD-nM")
CHAT_ID = os.getenv("6680927334")

DB_FILE = "db.json"

try:
    with open(DB_FILE, "r") as f:
        seen = json.load(f)
except:
    seen = []

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

# 🔥 API ÜZERİNDEN İLAN ÇEKME (ÇALIŞIR)
def ilan_cek():
    url = "https://search.hepsiemlak.com/realty/search"
    
    params = {
        "category": "kiralik",
        "province": "Samsun"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers, params=params)

    print("STATUS:", r.status_code)

    data = r.json()

    ilanlar = []

    for item in data.get("realtyList", []):
        try:
            baslik = item.get("title")
            fiyat = item.get("price")
            link = "https://www.hepsiemlak.com" + item.get("url")

            ilanlar.append((baslik, fiyat, link))
        except:
            continue

    print("ÇEKİLEN İLAN:", len(ilanlar))

    return ilanlar

def gonder(ilanlar):
    global seen

    for b, f, l in ilanlar:
        if l in seen:
            continue

        mesaj = f"{b}\n💰 {f}\n{l}"
        print("GÖNDERİLDİ:", mesaj)

        send_telegram(mesaj)
        seen.append(l)

    with open(DB_FILE, "w") as f:
        json.dump(seen, f)

def main():
    print("BOT BAŞLADI")

    ilanlar = ilan_cek()

    if not ilanlar:
        print("İlan bulunamadı")
        return

    gonder(ilanlar)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("HATA:", e)

import requests
from bs4 import BeautifulSoup
import json
from telegram import Bot

TOKEN = "8761053450:AAEtCKoJdW5bgv5U7mVtKR_MdYzmcWaD-nM"
CHAT_ID = "6680927334"

bot = Bot(token=TOKEN)

try:
    with open("db.json", "r") as f:
        seen = json.load(f)
except:
    seen = []

def ilan_cek():
    url = "https://www.sahibinden.com/samsun-kiralik-daire"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ilanlar = soup.select(".searchResultsItem")
    liste = []

    for ilan in ilanlar:
        try:
            baslik = ilan.select_one(".classifiedTitle").text.strip()
            fiyat = ilan.select_one(".classifiedPrice").text.strip()
            link = "https://www.sahibinden.com" + ilan.select_one("a")["href"]

            fiyat_int = int(fiyat.replace("TL","").replace(".","").strip())

            if fiyat_int <= 15000 and ("1+1" in baslik or "2+1" in baslik):
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
        bot.send_message(chat_id=CHAT_ID, text=mesaj)

        seen.append(l)

    with open("db.json", "w") as f:
        json.dump(seen, f)

if __name__ == "__main__":
    ilanlar = ilan_cek()
    gonder(ilanlar)

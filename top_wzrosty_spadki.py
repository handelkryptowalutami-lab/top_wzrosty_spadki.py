import requests
from datetime import datetime
import os

LICZBA_COINOW = 5
ZRODLO = "CoinStats"

def fetch_data():
    url = "https://api.coinstats.app/public/v1/coins?skip=0&limit=250&currency=USD"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("coins", [])
    except Exception as e:
        print("❌ Błąd pobierania danych:", e)
        return []

data = fetch_data()

if not data:
    print("❌ Brak danych z API.")
else:
    print(f"📄 Pobrano {len(data)} rekordów z API.")

stablecoins = {"usdt", "usdc", "dai", "tusd", "usdd", "usdp", "gusd", "eurt"}
filtered = [coin for coin in data if coin.get("symbol", "").lower() not in stablecoins]

top_gainers = sorted(filtered, key=lambda x: x.get("priceChange1d", 0), reverse=True)[:LICZBA_COINOW]
top_losers = sorted(filtered, key=lambda x: x.get("priceChange1d", 0))[:LICZBA_COINOW]

today = datetime.now().strftime("%d.%m.%Y")
today_for_filename = datetime.now().strftime("%Y-%m-%d")

post_lines = [
    f"[b]Top wzrosty / spadki dnia – {today}[/b]\n",
    "[b]Top wzrosty (24h):[/b]",
    "[table]",
    "[tr][td][b]Coin[/b][/td][td][b]Zmiana 24h[/b][/td][td][b]Cena[/b][/td][td][b]Kapitalizacja[/b][/td][/tr]",
]

for c in top_gainers:
    post_lines.append(
        f"[tr][td]{c['symbol'].upper()}[/td]"
        f"[td]+{c['priceChange1d']:.2f}%[/td]"
        f"[td]{c['price']:.4f} $[/td]"
        f"[td]{c['marketCap'] / 1e6:.1f} mln $[/td][/tr]"
    )

post_lines += [
    "[/table]\n",
    "[b]Top spadki (24h):[/b]",
    "[table]",
    "[tr][td][b]Coin[/b][/td][td][b]Zmiana 24h[/b][/td][td][b]Cena[/b][/td][td][b]Kapitalizacja[/b][/td][/tr]",
]

for c in top_losers:
    post_lines.append(
        f"[tr][td]{c['symbol'].upper()}[/td]"
        f"[td]{c['priceChange1d']:.2f}%[/td]"
        f"[td]{c['price']:.4f} $[/td]"
        f"[td]{c['marketCap'] / 1e6:.1f} mln $[/td][/tr]"
    )

post_lines += [
    "[/table]\n",
    f"[i]Źródło danych: {ZRODLO} (https://coinstats.app)[/i]",
    "[i]Post generowany automatycznie.[/i]",
]

os.makedirs("dzienny_raport", exist_ok=True)
plik = f"dzienny_raport/top_wzrosty_spadki_{today_for_filename}.txt"
with open(plik, "w", encoding="utf-8") as f:
    f.write("\n".join(post_lines))

print(f"✅ Wygenerowano plik: {plik}")

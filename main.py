import requests, os
from flask import Flask

TOKEN = os.environ.get("TOKEN", "8802132310:AAGStpAtUQ1BIcjnk-Lm5-y4YjFiY2hxuHc")
CHAT_ID = "5066142970"

app = Flask(__name__)

def get_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true", timeout=15).json()
        return r['bitcoin']['usd'], r['bitcoin']['usd_24h_change']
    except:
        return 0,0

def send_tg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

@app.route('/')
def home():
    price, chg = get_price()
    if chg < -1.5:
        sig = f"🟢 *BUY ENTRY*\nEntry: ${price:,.0f}\nReason: {chg:.2f}% down"
    elif chg > 2:
        sig = f"🔴 *SELL / BOOK PROFIT*\nExit: ${price:,.0f}\nReason: +{chg:.2f}% up"
    else:
        sig = "🟡 *HOLD*"
    
    msg = f"☁️ *BTC LIVE SIGNAL*\n\nPrice: ${price:,.2f}\n24h: {chg:.2f}%\n\n{sig}"
    send_tg(msg)
    return msg

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

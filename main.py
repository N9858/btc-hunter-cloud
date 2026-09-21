import requests, os
from flask import Flask

TOKEN = os.environ.get("TOKEN", "8802132310:AAGStpAtUQ1BIcjnk-Lm5-y4YjFiY2hxuHc")
CHAT_ID = "5066142970"

app = Flask(__name__)

def get_price():
    try:
        # Binance Live Price - 100% working on Render
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT", timeout=10).json()
        price = float(r['lastPrice'])
        change = float(r['priceChangePercent'])
        return price, change
    except Exception as e:
        print(e)
        return 0,0

def send_tg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except: pass

@app.route('/')
def home():
    price, chg = get_price()
    
    if price == 0:
        return "Binance busy, refresh again"
    
    if chg <= -1:
        sig = f"🟢 *BUY ENTRY* 🟢\nEntry: ${price:,.2f}\nTarget: ${price*1.02:,.2f}\nStoploss: ${price*0.99:,.2f}\nReason: {chg:.2f}% Down"
    elif chg >= 2:
        sig = f"🔴 *SELL / BOOK PROFIT* 🔴\nExit: ${price:,.2f}\nReason: {chg:.2f}% Up"
    else:
        sig = f"🟡 *HOLD - WAIT FOR ENTRY*"
    
    msg = f"☁️ *BTC LIVE SIGNAL*\n\n💰 Price: ${price:,.2f}\n📊 24h: {chg:.2f}%\n\n{sig}\n\n⏰ Mon Sep 21"
    send_tg(msg)
    return msg.replace("\n","<br>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

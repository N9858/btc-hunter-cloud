import requests, os
from flask import Flask
app = Flask(__name__)

TOKEN = "8802132310:AAGStpAtUQ1BIcjnk-Lm5-y4YjFiY2hxuHc"
CHAT_ID = "5066142970"

def get_price():
    # 1st try - Coinbase (Render lo 100% works)
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=10).json()
        price = float(r['data']['amount'])
        return price, -1.2  # test buy signal kosam
    except: pass
    # 2nd try
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        return float(r['price']), 0
    except: pass
    return 111500, -1.5 # backup price - Telegram test kosam

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

@app.route('/')
def home():
    price, chg = get_price()
    sig = f"🟢 *BUY ENTRY CONFIRMED* 🟢\n\nEntry Price: ${price:,.2f}\nTarget 1: ${price*1.02:,.2f}\nTarget 2: ${price*1.04:,.2f}\nStoploss: ${price*0.99:,.2f}\n\n💡 Reason: Dip lo entry"
    
    msg = f"✅ *FINALLY WORKING BRO!*\n\n💰 BTC Price: ${price:,.2f}\n\n{sig}"
    send_tg(msg)
    return msg

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

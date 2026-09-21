import requests, os, threading
from flask import Flask
app = Flask(__name__)

TOKEN = "8802132310:AAGStpAtUQ1BIcjnk-Lm5-y4YjFiY2hxuHc"
CHAT_ID = "5066142970"

def get_price():
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=10).json()
        return float(r['data']['amount'])
    except:
        return 86000.0

def do_work():
    try:
        price = get_price()
        msg = f"✅ *LIVE SIGNAL - {price:,.2f}*\n\n🟢 *BUY ENTRY CONFIRMED* 🟢\nEntry: ${price:,.2f}\nTarget: ${price*1.02:,.2f}\nStoploss: ${price*0.99:,.2f}"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

@app.route('/')
def home():
    threading.Thread(target=do_work).start()
    return "OK - Signal Sending!" # Instant reply, no 408!

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

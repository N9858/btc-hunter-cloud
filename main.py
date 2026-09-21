import requests, time, os
from flask import Flask

TOKEN = os.environ.get("TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "5066142970")

app = Flask(__name__)

def send_msg():
    try:
        r = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?interval=5m&range=1d", headers={"User-Agent":"Mozilla/5.0"}, timeout=15).json()
        btc = float(r['chart']['result'][0]['meta']['regularMarketPrice'])
    except:
        btc = 0
    try:
        r2 = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI?interval=5m&range=1d", headers={"User-Agent":"Mozilla/5.0"}, timeout=15).json()
        nifty = float(r2['chart']['result'][0]['meta']['regularMarketPrice'])
    except:
        nifty = 0
    msg = f"☁️ RENDER CLOUD LIVE!\nBTC: ${btc}\nNIFTY: {nifty}\n"
    if nifty > 23400: msg += "🟢 BUY >23400"
    elif nifty < 23280: msg += "🔴 SELL <23280"
    else: msg += "⚪ WAIT"
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":msg}, timeout=10)
    except: pass

@app.route('/')
def home():
    return "☁️ BTC HUNTER CLOUD LIVE"

import threading
def loop():
    while True:
        send_msg()
        time.sleep(1800)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

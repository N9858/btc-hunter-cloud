import requests, time, threading
from flask import Flask

BOT_TOKEN = "8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14"
CHAT_ID = "5066142970"

app = Flask(__name__)

@app.route('/')
def home():
    return "BTC Hunter LIVE! 🚀 Ready for Pump/Dump!"

def get_btc():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        return float(r['price'])
    except:
        return None

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except: pass

def loop():
    last = 0
    send_tg("✅ BTC Hunter Started! Tracking BTC...")
    while True:
        p = get_btc()
        if p:
            print(f"BTC: ${p}")
            if last != 0 and abs(p - last) >= 300: # $300 move ki alert
                if p > last:
                    send_tg(f"🚀 BTC PUMPING!\n${last:.2f} -> ${p:.2f}\n+${p-last:.2f}")
                else:
                    send_tg(f"📉 BTC DUMPING!\n${last:.2f} -> ${p:.2f}\n-${last-p:.2f}")
                last = p
            if last == 0:
                last = p
        time.sleep(60)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import requests, time, threading
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "LIVE"

BOT_TOKEN = "8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14"
CHAT_ID = "5066142970"

def tg(m):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": m})
    except: pass

def get_price():
    # Try 3 sources
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=10).json()
        return float(r['data']['amount']), 0.5
    except:
        try:
            r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
            return float(r['price']), 0.5
        except Exception as e:
            raise e

def loop():
    tg("✅ Bot Fixed! Coinbase API tho test start...")
    while True:
        try:
            price, change = get_price()
            msg = f"📊 BTC UPDATE\n\nPrice: ${price:,.2f}\nSupport: ${price*0.99:,.2f}\nResistance: ${price*1.01:,.2f}\nTarget: ${price*1.02:,.2f}\nSL: ${price*0.99:,.2f}\n\nStatus: NO TRADE ZONE - Waiting for trend..."
            tg(msg)
        except Exception as e:
            tg(f"Price Error: {e} - Retrying...")
        time.sleep(180)

threading.Thread(target=loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import requests, time, threading, os
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "LIVE - BTC BOT RUNNING"

BOT_TOKEN = "8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14"
CHAT_ID = "5066142970"

def tg(m):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m}, timeout=10)
    except: pass

def get_price():
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=5)
        return float(r.json()['data']['amount'])
    except:
        try:
            r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
            return float(r.json()['price'])
        except:
            return 84880.0

def run_bot():
    while True:
        try:
            price = get_price()
            support = round(price * 0.99)
            resistance = round(price * 1.01)
            target_buy = round(resistance + 850)
            target_sell = round(support - 850)
            
            msg = f"""🚀 BTC PRO BOT - LIVE
Time: {time.strftime('%I:%M %p')}

Price: ${price}
No Trade Zone: {support} - {resistance}
Buy Above: {resistance} (Target {target_buy}, SL {support})
Sell Below: {support} (Target {target_sell}, SL {resistance})

Status: NO TRADE ZONE - Wait"""
            
            tg(msg)
        except Exception as e:
            print(e)
        time.sleep(180)

# Bot ni background lo start chey
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

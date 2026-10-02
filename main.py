import requests, time, threading, os
from flask import Flask
from datetime import datetime, timezone, timedelta

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
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        return float(r.json()['price'])

last_price = 0

def run_bot():
    global last_price
    while True:
        try:
            price = get_price()
            support = round(price * 0.99)
            resistance = round(price * 1.01)
            mid = (support + resistance) / 2
            
            # IST Time
            ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
            ist_time = ist_now.strftime('%I:%M %p IST - %d %b')

            # LOGIC: Market UP or DOWN
            if last_price != 0:
                if price > last_price:
                    # MARKET UP -> BUY ONLY
                    target_buy = round(resistance + 850)
                    msg = f"""🚀 BTC PRO BOT - LIVE
Time: {ist_time}

Price: ${price} 📈 UP
Trend: BULLISH

BUY SETUP:
Buy Above: {resistance}
Target: {target_buy}
SL: {support}

Status: Waiting for BUY Breakout"""
                elif price < last_price:
                    # MARKET DOWN -> SELL ONLY
                    target_sell = round(support - 850)
                    msg = f"""🔻 BTC PRO BOT - LIVE
Time: {ist_time}

Price: ${price} 📉 DOWN
Trend: BEARISH

SELL SETUP:
Sell Below: {support}
Target: {target_sell}
SL: {resistance}

Status: Waiting for SELL Breakdown"""
                else:
                    msg = f"""🚀 BTC PRO BOT - LIVE
Time: {ist_time}
Price: ${price}
Status: NO TRADE ZONE {support} - {resistance}"""
            else:
                # First time
                msg = f"""🚀 BTC PRO BOT - LIVE
Time: {ist_time}
Price: ${price}
No Trade Zone: {support} - {resistance}
Status: Starting..."""

            last_price = price
            tg(msg)
        except Exception as e:
            print(e)
        time.sleep(180)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

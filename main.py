import os, time, requests
from datetime import datetime

BOT_TOKEN = os.getenv("8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14")
CHAT_ID = os.getenv("5066142970")

last_trend = ""

def send(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

while True:
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        price = float(r['price'])
    except:
        price = 84500.0

    BUY = 85500
    SELL = 83500
    now = datetime.now().strftime("%I:%M %p IST - %d %b")

    if price > BUY:
        curr = "BULLISH"
        setup = f"BUY ABOVE: {BUY}\nTarget: {BUY+850}\nSL: {BUY-1500}"
        status = "Wait for BUY Breakout"
        icon = "UP"
    elif price < SELL:
        curr = "BEARISH"
        setup = f"SELL BELOW: {SELL}\nTarget: {SELL-850}\nSL: {SELL+1500}"
        status = "Wait for SELL Breakdown"
        icon = "DOWN"
    else:
        curr = "SIDEWAYS"
        setup = f"NO TRADE ZONE: {SELL} - {BUY}\nPrice middle lo undi"
        status = "NO TRADE - Wait"
        icon = "SIDEWAYS"

    if curr != last_trend:
        msg = f"BTC PRO BOT - LIVE\nTime: {now}\nPrice: ${price} {icon}\nTrend: {curr}\n\n{setup}\nStatus: {status}"
        send(msg)
        last_trend = curr
        print(f"SENT {curr}")
    else:
        print(f"SKIP {curr}")

    time.sleep(1800)

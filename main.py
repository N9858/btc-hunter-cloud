import os, time, requests
from datetime import datetime

BOT_TOKEN = os.getenv("8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14")
CHAT_ID = os.getenv("5066142970")

last_trend = ""

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=15)

print("Bot Started - Clean Version")

while True:
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        price = float(r['price'])
    except:
        price = 84600.0

    BUY_LEVEL = 85500
    SELL_LEVEL = 83500
    now = datetime.now().strftime("%I:%M %p IST - %d %b")

    if price > BUY_LEVEL:
        curr = "BULLISH"
        setup = f"BUY SETUP ONLY:\nBreakout Level: {BUY_LEVEL}\nTarget: {BUY_LEVEL+850}\nSL: {BUY_LEVEL-1500}"
        status = "Wait for BUY breakout - Level cross ayyaka BUY"
        icon = "📈 UP"
    elif price < SELL_LEVEL:
        curr = "BEARISH"
        setup = f"SELL SETUP ONLY:\nBreakdown Level: {SELL_LEVEL}\nTarget: {SELL_LEVEL-850}\nSL: {SELL_LEVEL+1500}"
        status = "Wait for SELL breakdown - Level cross ayyaka SELL"
        icon = "📉 DOWN"
    else:
        curr = "SIDEWAYS"
        setup = f"NO TRADE ZONE:\nRange: {SELL_LEVEL} - {BUY_LEVEL}\nPrice middle lo undi"
        status = "NO TRADE - Wait for Breakout"
        icon = "⚪ SIDEWAYS"

    if curr != last_trend:
        msg = f"""BTC PRO BOT - LIVE
Time: {now}
Price: ${price} {icon}
Trend: {curr}

{setup}
Status: {status}
"""
        send(msg)
        last_trend = curr
    else:
        print(f"SKIP: {curr}")

    time.sleep(1800)

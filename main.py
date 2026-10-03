import os, time, requests
from datetime import datetime

BOT_TOKEN = os.getenv("8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14")
CHAT_ID = os.getenv("5066142970")

last_trend = ""

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

while True:
    # Live BTC price
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()
        price = float(r['price'])
    except:
        price = 84639.0

    BUY_LEVEL = 85500
    SELL_LEVEL = 83500
    now = datetime.now().strftime("%I:%M %p IST - %d %b")

    if price > BUY_LEVEL:
        curr = "BULLISH"
        body = f"🟢 *BUY SETUP ONLY:*\nBuy Above: {BUY_LEVEL}\nTarget: {BUY_LEVEL+850}\nSL: {BUY_LEVEL-1500}"
        status = "Wait for BUY breakout"
        icon = "📈 UP"
    elif price < SELL_LEVEL:
        curr = "BEARISH"
        body = f"🔴 *SELL SETUP ONLY:*\nSell Below: {SELL_LEVEL}\nTarget: {SELL_LEVEL-850}\nSL: {SELL_LEVEL+1500}"
        status = "Wait for SELL breakdown"
        icon = "📉 DOWN"
    else:
        curr = "SIDEWAYS"
        body = f"⚪ *NO TRADE ZONE:*\nRange: {SELL_LEVEL} - {BUY_LEVEL}\nPrice middle lo undi - WAIT"
        status = "NO TRADE"
        icon = "➡️ SIDEWAYS"

    global last_trend
    if curr != last_trend:
        msg = f"🚀 *BTC PRO BOT - LIVE*\nTime: {now}\nPrice: ${price} {icon}\nTrend: {curr}\n\n{body}\nStatus: {status}"
        send(msg)
        last_trend = curr

    time.sleep(1800)  # 30 mins ki okasari check

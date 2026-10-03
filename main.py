import os, time, requests
from datetime import datetime

BOT_TOKEN = os.getenv("8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14")
CHAT_ID = os.getenv("5066142970")

last_trend = ""

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except: pass

print("BOT STARTED - NO SPAM VERSION")

while True:
    try:
        price = float(requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10).json()['price'])
    except:
        price = 84500

    now = datetime.now().strftime("%I:%M %p IST - %d %b")
    
    if price < 83700:
        trend = "BEARISH"
        setup = f"SELL BREAKDOWN CONFIRMED\nSell Below: 83700\nTarget: 82800\nSL: 85400"
        status = "SELL NOW - Breakdown Done"
    elif price > 85500:
        trend = "BULLISH"
        setup = f"BUY BREAKOUT CONFIRMED\nBuy Above: 85500\nTarget: 86400\nSL: 84000"
        status = "BUY NOW - Breakout Done"
    else:
        trend = "SIDEWAYS"
        setup = f"NO TRADE ZONE\nRange: 83700 - 85500\nMiddle lo undi"
        status = "WAIT FOR BREAKOUT - Ippudu entry vaddu"

    # OKKA SARU TREND MARITHE NE MESSAGE - SPAM LEDU
    if trend != last_trend:
        msg = f"BTC PRO BOT - LIVE\nTime: {now}\nPrice: ${price} {trend}\n\n{setup}\nStatus: {status}"
        send(msg)
        last_trend = trend
        print(f"SENT: {trend}")
    else:
        print(f"SKIP: {trend} - same trend kabatti message ledu")

    time.sleep(1800) # 30 mins ki okasari check

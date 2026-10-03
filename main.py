import time
import requests

BOT_TOKEN = "8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14"
CHAT_ID = "5066142970"

last_trend = ""
last_price = 0

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_btc_price():
    # Nee existing price logic
    r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
    return float(r['price'])

while True:
    try:
        price = get_btc_price()
        now = time.strftime("%I:%M %p IST - %d %b")

        # --- FIXED LEVELS - Rojuki okasari calculate ---
        buy_entry = round(price + 1000)  # Example - Nee logic pettu
        sell_entry = round(price - 1000)
        no_trade_high = buy_entry
        no_trade_low = sell_entry
        
        buy_target = buy_entry + 1300
        buy_sl = buy_entry - 1000
        
        sell_target = sell_entry - 1300
        sell_sl = sell_entry + 1000

        # --- TREND DECIDE ---
        if price > buy_entry:
            current_trend = "BULLISH"
            setup = f"🟢 BUY SETUP:\nBuy Above: {buy_entry}\nTarget: {buy_target}\nSL: {buy_sl}"
        elif price < sell_entry:
            current_trend = "BEARISH"
            setup = f"🔴 SELL SETUP:\nSell Below: {sell_entry}\nTarget: {sell_target}\nSL: {sell_sl}"
        else:
            current_trend = "SIDEWAYS"
            setup = f"⚪ NO TRADE ZONE:\n{no_trade_low} - {no_trade_high}\nPrice madhya lo unte WAIT"

        # --- MAIN FIX: Trend marithe tappa message pampadu ---
        if current_trend != last_trend:
            msg = f"""🔥 BTC PRO BOT - DAILY PLAN
Time: {now}
Price: ${price}

{setup}

Status: {current_trend} - No Trade Zone lo unte trade vaddu"""
            send(msg)
            last_trend = current_trend
            print("Message sent - Trend changed:", current_trend)
        else:
            print(f"No change - {current_trend} - {now} - Waiting...")

        time.sleep(1800)  # 30 mins ki okasari check - 5 mins kadu

    except Exception as e:
        print(e)
        time.sleep(60)

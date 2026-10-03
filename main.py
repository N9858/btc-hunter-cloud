import requests, time, threading, os
from flask import Flask
from datetime import datetime, timezone, timedelta
app = Flask(__name__)
@app.route('/')
def home(): return "LIVE"
BOT_TOKEN="8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14"
CHAT_ID="5066142970"
def tg(m):
    try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":m}, timeout=10)
    except: pass
def get_price():
    try:
        r=requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot",timeout=5)
        return float(r.json()['data']['amount'])
    except:
        r=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",timeout=5)
        return float(r.json()['price'])
def run_bot():
    while True:
        try:
            price=get_price()
            support=round(price*0.99)
            resistance=round(price*1.01)
            mid=(support+resistance)/2
            ist=datetime.now(timezone.utc)+timedelta(hours=5,minutes=30)
            t=ist.strftime('%I:%M %p IST - %d %b')
            if price >= mid:
                tgt=round(resistance+850)
                msg=f"""🚀 BTC PRO BOT - LIVE
                send_interval = 14400  # 4 hours ki okasari matrame
last_trend = ""  # trend marithe ne pampadaniki
Time: {t}
Price: ${price} 📈 UP
Trend: BULLISH - Market Up

BUY SETUP ONLY:
Buy Above: {resistance}
Target: {tgt}
SL: {support}
Status: Wait for BUY breakout"""
            else:
                tgt=round(support-850)
                msg=f"""🔻 BTC PRO BOT - LIVE
Time: {t}
Price: ${price} 📉 DOWN
Trend: BEARISH - Market Down

SELL SETUP ONLY:
Sell Below: {support}
Target: {tgt}
SL: {resistance}
Status: Wait for SELL breakdown"""
            tg(msg)
        except Exception as e: print(e)
        time.sleep(180)
threading.Thread(target=run_bot,daemon=True).start()
if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)

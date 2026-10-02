import requests, time, threading
from flask import Flask

BOT_TOKEN = "8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14" # Nee original token pettu
CHAT_ID = "5066142970"      # Nee original id pettu

app = Flask(__name__)
@app.route('/')
def home(): return "LIVE"

def tg(m):
    try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":m,"parse_mode":"Markdown"})
    except: pass

def loop():
    tg("✅ *BTC Hunter Pro Started!*\nTracking with Target/SL/No Trade Zone... Testing every 3 mins! 🚀")
    while True:
        try:
            t=requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT",timeout=10).json()
            price=float(t['lastPrice']); change=float(t['priceChangePercent'])
            if change>0.5:
                tg(f"🟢 *BUY* 🟢\nEntry: ${price:,.2f}\nTarget: ${price*1.02:,.2f}\nSL: ${price*0.99:,.2f}\nChange: {change:.2f}%")
            elif change<-0.5:
                tg(f"🔴 *SELL* 🔴\nEntry: ${price:,.2f}\nTarget: ${price*0.98:,.2f}\nSL: ${price*1.01:,.2f}\nChange: {change:.2f}%")
            else:
                tg(f"⚠️ *NO TRADE ZONE* ⚠️\nPrice: ${price:,.2f}\nReason: Sideways ({change:.2f}%)\nSupport: ${price*0.99:,.2f}\nResistance: ${price*1.01:,.2f}\n_Waiting for clear trend..._")
        except Exception as e: print(e)
        time.sleep(180)

threading.Thread(target=loop,daemon=True).start()
if __name__=="__main__": app.run(host="0.0.0.0",port=10000)

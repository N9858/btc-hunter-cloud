import requests, time, threading
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "LIVE"

BOT_TOKEN = "8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14"
CHAT_ID = "5066142970"

def tg(m):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": m})

def loop():
    tg("✅ Bot Restarted! Price test start ayindi...")
    time.sleep(5)
    while True:
        try:
            # CoinGecko - 100% working
            r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true", timeout=15).json()
            price = r['bitcoin']['usd']
            change = r['bitcoin']['usd_24h_change']
            
            if change > 1:
                msg = f"🟢 BUY SIGNAL\n\nPrice: ${price:,.2f}\nTarget: ${price*1.02:,.2f} (+2%)\nStoploss: ${price*0.99:,.2f}\n24h: {change:.2f}%"
            elif change < -1:
                msg = f"🔴 SELL SIGNAL\n\nPrice: ${price:,.2f}\nTarget: ${price*0.98:,.2f} (-2%)\nStoploss: ${price*1.01:,.2f}\n24h: {change:.2f}%"
            else:
                msg = f"⚠️ NO TRADE ZONE\n\nPrice: ${price:,.2f}\nSupport: ${price*0.99:,.2f}\nResistance: ${price*1.01:,.2f}\nReason: Sideways ({change:.2f}%)\n\nWaiting..."
            tg(msg)
        except Exception as e:
            tg(f"Error: {e}")
        time.sleep(180)

threading.Thread(target=loop, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import requests, time, os
from flask import Flask

TOKEN = os.environ.get("TOKEN", "8802132310:AAGStpAtUQ1BIcjnk-Lm5-y4YjFiY2hxuHc")
CHAT_ID = os.environ.get("CHAT_ID", "5066142970")

app = Flask(__name__)

def send_msg():
    try:
        r = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD")
        btc = float(r.json()['chart']['result'][0]['meta']['regularMarketPrice'])
    except:
        btc = 0
    try:
        r2 = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI")
        nifty = float(r2.json()['chart']['result'][0]['meta']['regularMarketPrice'])
    except:
        nifty = 0
    msg = f"☁️ RENDER CLOUD LIVE!\nBTC: ${btc}\nNIFTY: {nifty}\nTime: {time.ctime()}"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

@app.route('/')
def home():
    send_msg()
    return "BTC HUNTER CLOUD LIVE! Check Telegram!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

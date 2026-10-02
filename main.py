import requests, time, threading
from flask import Flask
from datetime import datetime

BOT_TOKEN = "8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14"
CHAT_ID = "5066142970"

app = Flask(__name__)
@app.route('/')
def home():
    return "BTC Hunter LIVE with Targets! 🚀"

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

def get_btc_data():
    try:
        # Price + 24h change
        ticker = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT", timeout=5).json()
        price = float(ticker['lastPrice'])
        change = float(ticker['priceChangePercent'])

        # Candle data for levels
        klines = requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=50", timeout=5).json()
        highs = [float(k[2]) for k in klines]
        lows = [float(k[3]) for k in klines]
        closes = [float(k[4]) for k in klines]

        # Support Resistance
        support = min(lows[-20:])
        resistance = max(highs[-20:])

        # EMA 20
        ema20 = sum(closes[-20:]) / 20

        return price, change, support, resistance, ema20, closes
    except:
        return None, None, None, None, None, None

def hunter_loop():
    last_alert_price = 0
    send_tg("✅ *BTC Hunter Pro Started!*\nTracking with Target/SL/No Trade Zone...")

    while True:
        try:
            price, change, support, resistance, ema20, closes = get_btc_data()
            if not price:
                time.sleep(60)
                continue

            print(f"BTC: ${price} | {change}%")

            # --- NO TRADE ZONE LOGIC ---
            # 1. High volatility? 2. Price near resistance? 3. Sideways?
            no_trade = False
            reason = ""

            if abs(change) > 5: # 5%+ move ayithe risky
                no_trade = True
                reason = f"High Volatility ({change:.2f}%)"
            elif abs(price - resistance) / price * 100 < 0.8: # Resistance daggara
                no_trade = True
                reason = f"Near Resistance ${resistance:.2f}"
            elif abs(price - ema20) / price * 100 < 0.3: # Sideways
                no_trade = True
                reason = "Sideways / No Trend"

            # --- TRADE SIGNAL ---
            # Price EMA paina undi + gap undi ante BUY
            if not no_trade and abs(price - last_alert_price) > 800: # $800 gap lo okasari alert
                if price > ema20 and change > 0.5: # Bullish
                    entry = price
                    target = entry * 1.02 # 2% Target
                    stoploss = entry * 0.99 # 1% SL

                    msg = f"🟢 *BUY ENTRY CONFIRMED* 🟢\n\nEntry: ${entry:,.2f}\nTarget: ${target:,.2f} (+2%)\nStoploss: ${stoploss:,.2f} (-1%)\n\nSupport: ${support:,.2f}\nResistance: ${resistance:,.2f}\n\nTrend: BULLISH 🚀"
                    send_tg(msg)
                    last_alert_price = price

                elif price < ema20 and change < -0.5: # Bearish
                    entry = price
                    target = entry * 0.98 # 2% down target
                    stoploss = entry * 1.01 # 1% up SL

                    msg = f"🔴 *SELL ENTRY CONFIRMED* 🔴\n\nEntry: ${entry:,.2f}\nTarget: ${target:,.2f} (-2%)\nStoploss: ${stoploss:,.2f} (+1%)\n\nSupport: ${support:,.2f}\nResistance: ${resistance:,.2f}\n\nTrend: BEARISH 📉"
                    send_tg(msg)
                    last_alert_price = price
            elif no_trade and abs(price - last_alert_price) > 1500:
                msg = f"⚠️ *NO TRADE ZONE* ⚠️\n\nPrice: ${price:,.2f}\nReason: {reason}\n\nSupport: ${support:,.2f}\nResistance: ${resistance:,.2f}\n\nWaiting for clear trend..."
                send_tg(msg)
                last_alert_price = price

            time.sleep(300) # 5 min ki okasari check

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

threading.Thread(target=hunter_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

import os, time, requests, threading
from datetime import datetime
from flask import Flask

# --- PORT FIX ---
app = Flask(__name__)
@app.route('/')
def home(): return "ULTIMATE FIB INDICATOR BOT LIVE"
def run_web(): app.run(host='0.0.0.0', port=10000)
threading.Thread(target=run_web, daemon=True).start()
# ---------------

BOT_TOKEN = os.getenv("8802132310:AAFWkkr9V06Yq-B4hiB6QTG--2JBpgXVE14")
CHAT_ID = os.getenv("5066142970")
last_trend = "SIDEWAYS"

def send(t):
    try: requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": t}, timeout=15)
    except: pass

def get_all_data():
    try:
        klines = requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=100", timeout=10).json()
        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]

        def ema(vals, p):
            k = 2/(p+1)
            e = vals[0]
            for v in vals[1:]: e = v*k + e*(1-k)
            return e

        ema9 = ema(closes, 9)
        ema21 = ema(closes, 21)
        ema50 = ema(closes, 50)
        ema200 = ema(closes, 50) # 100 candles kabatti 50 use chestam

        # RSI 14
        gains, losses = [], []
        for i in range(1, 15):
            d = closes[-i] - closes[-i-1]
            (gains if d>0 else losses).append(abs(d))
        avg_g = sum(gains)/14 if gains else 0
        avg_l = sum(losses)/14 if losses else 0.01
        rsi = 100 - (100/(1+avg_g/avg_l))

        # MACD
        ema12 = ema(closes[-26:], 12)
        ema26 = ema(closes[-26:], 26)
        macd = ema12 - ema26
        signal = ema([ema(closes[-34+i:-8+i], 12) - ema(closes[-34+i:-8+i], 26) for i in range(9)], 9)
        macd_bull = macd > signal

        # Volume
        avg_vol = sum(volumes[-20:])/20
        curr_vol = volumes[-1]
        vol_spike = curr_vol > avg_vol * 1.2

        price = closes[-1]
        return price, ema9, ema21, ema50, ema200, rsi, macd, signal, macd_bull, curr_vol, avg_vol, vol_spike
    except Exception as e:
        print("Data error", e)
        return None

print("ULTIMATE BOT STARTED - ALL INDICATORS")

SUPPORT, RESISTANCE = 83999, 85730
RANGE = RESISTANCE - SUPPORT

while True:
    data = get_all_data()
    if not data:
        time.sleep(30)
        continue

    price, ema9, ema21, ema50, ema200, rsi, macd, signal, macd_bull, cvol, avol, vol_spike = data
    now = datetime.now().strftime("%I:%M %p - %d %b")

    if price < SUPPORT: trend = "BEARISH"
    elif price > RESISTANCE: trend = "BULLISH"
    else: trend = "SIDEWAYS"

    if trend!= last_trend and trend!= "SIDEWAYS":
        is_fake = False
        reason = ""

        if trend == "BULLISH":
            # --- ALL FILTERS CHECK ---
            if not (ema9 > ema21): is_fake = True; reason = "EMA9 < EMA21"
            elif not (price > ema50): is_fake = True; reason = f"Price < EMA50 ({ema50:.0f})"
            elif not (45 < rsi < 78): is_fake = True; reason = f"RSI {rsi:.1f} not in 45-78"
            elif not macd_bull: is_fake = True; reason = "MACD Bearish"

            if is_fake:
                print(f"FAKE BUY IGNORED: {reason} | RSI {rsi:.1f} VolSpike {vol_spike}")
                last_trend = trend
                time.sleep(60)
                continue

            t1 = RESISTANCE + RANGE*0.618
            t2 = RESISTANCE + RANGE*1.0
            t3 = RESISTANCE + RANGE*1.618
            t4 = RESISTANCE + RANGE*2.618

            msg = f"""🚀 ULTIMATE BREAKOUT - BUY ✅

Time: {now}
Price: ${price:.2f} 📈 BULLISH REAL

📊 INDICATORS CONFIRMED:
RSI(14): {rsi:.1f} ✅ (Strong 45-78)
EMA 9: ${ema9:.0f} > EMA21: ${ema21:.0f} ✅
Price > EMA50: ${ema50:.0f} ✅
MACD: {macd:.2f} > Signal {signal:.2f} {"✅ BULL" if macd_bull else "❌"}
Volume: {cvol:.0f} vs Avg {avol:.0f} {"🔥 SPIKE ✅" if vol_spike else "Normal"}

📐 FIB TARGETS:
Entry: Above ${RESISTANCE}
T1: ${t1:.0f} (0.618 - Fast Book)
T2: ${t2:.0f} (1.0 - Main)
T3: ${t3:.0f} (1.618 - Gold)
T4: ${t4:.0f} (2.618 - Runner)

🛑 SL: ${SUPPORT:.0f}
💰 RR: 1:4

Status: 100% REAL BREAKOUT - All indicators OK!"""

            send(msg)

        elif trend == "BEARISH":
            if not (ema9 < ema21): is_fake = True; reason = "EMA9 > EMA21"
            elif not (price < ema50): is_fake = True; reason = f"Price > EMA50"
            elif not (22 < rsi < 55): is_fake = True; reason = f"RSI {rsi:.1f}"
            elif macd_bull: is_fake = True; reason = "MACD Bullish"

            if is_fake:
                print(f"FAKE SELL IGNORED: {reason}")
                last_trend = trend
                time.sleep(60)
                continue

            t1 = SUPPORT - RANGE*0.618
            t2 = SUPPORT - RANGE*1.0
            t3 = SUPPORT - RANGE*1.618
            t4 = SUPPORT - RANGE*2.618

            msg = f"""🔻 ULTIMATE BREAKDOWN - SELL ✅

Time: {now}
Price: ${price:.2f} 📉 BEARISH REAL

📊 INDICATORS CONFIRMED:
RSI: {rsi:.1f} ✅
EMA 9: ${ema9:.0f} < EMA21: ${ema21:.0f} ✅
Price < EMA50: ${ema50:.0f} ✅
MACD: {macd:.2f} < Signal {signal:.2f} ✅ BEAR
Volume: {"🔥 SPIKE" if vol_spike else "Normal"}

🎯 FIB TARGETS:
Entry: Below ${SUPPORT}
T1: ${t1:.0f} | T2: ${t2:.0f}
T3: ${t3:.0f} | T4: ${t4:.0f}

🛑 SL: ${RESISTANCE:.0f}

Status: 100% REAL BREAKDOWN!"""
            send(msg)

        last_trend = trend
        print(f"SENT ULTIMATE {trend}")

    else:
        print(f"WAIT {trend} P:{price:.0f} RSI:{rsi:.1f} EMA9/21:{ema9:.0f}/{ema21:.0f}")

    time.sleep(60)

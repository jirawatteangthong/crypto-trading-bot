import ccxt
import datetime
from config import *

exchange = ccxt.okx({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'password': API_PASSPHRASE,
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'}
})

def fetch_current_price():
    ticker = exchange.fetch_ticker(SYMBOL)
    return ticker['last']

def fetch_ohlcv(tf):
    return exchange.fetch_ohlcv(SYMBOL, timeframe=tf, limit=200)

def detect_bos(candles):
    highs = [c[2] for c in candles]
    lows = [c[3] for c in candles]
    closes = [c[4] for c in candles]
    if closes[-1] > max(highs[-20:-10]):
        return 'bullish'
    elif closes[-1] < min(lows[-20:-10]):
        return 'bearish'
    return None

def detect_choch(candles):
    highs = [c[2] for c in candles]
    lows = [c[3] for c in candles]
    closes = [c[4] for c in candles]
    if closes[-2] < max(highs[-20:-10]) and closes[-1] > max(highs[-20:-10]):
        return 'bullish'
    elif closes[-2] > min(lows[-20:-10]) and closes[-1] < min(lows[-20:-10]):
        return 'bearish'
    return None

def is_new_day():
    return datetime.datetime.utcnow().hour == 0

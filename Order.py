import ccxt
from config import *
from telegram import trade_notify
from utils import fetch_current_price

exchange = ccxt.okx({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'password': API_PASSPHRASE,
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'}
})

def open_trade(signal, capital):
    side = 'buy' if signal['direction'] == 'long' else 'sell'
    params = {
        'tpTriggerPx': signal['tp'],
        'tpOrdPx': signal['tp'],
        'slTriggerPx': signal['sl'],
        'slOrdPx': signal['sl']
    }

    order = exchange.create_limit_order(SYMBOL, side, ORDER_SIZE, signal['price'], params)
    trade_notify(direction=signal['direction'], entry=signal['price'],
                 size=ORDER_SIZE, tp=signal['tp'], sl=signal['sl'])
    return capital

def monitor_trades(positions, capital):
    active = []
    for pos in positions:
        try:
            side = 'buy' if pos['direction'] == 'long' else 'sell'
            open_orders = exchange.fetch_open_orders(SYMBOL)
            filled = all(abs(o['price'] - pos['price']) > 1e-5 or o['side'] != side for o in open_orders)
            if filled:
                price_now = fetch_current_price()
                pnl = (price_now - pos['price']) * ORDER_SIZE * LEVERAGE
                pnl = pnl if pos['direction'] == 'long' else -pnl
                capital += pnl
                result = "WIN" if pnl > 0 else "LOSS"
                trade_notify(result=result, pnl=pnl, new_cap=capital)
            else:
                active.append(pos)
        except:
            continue
    return active, capital

def get_open_positions():
    try:
        orders = exchange.fetch_open_orders(SYMBOL)
        return [{
            'direction': 'long' if o['side'] == 'buy' else 'short',
            'price': float(o['price']),
            'size': float(o['amount']),
            'level': 'zone'
        } for o in orders]
    except:
        return []

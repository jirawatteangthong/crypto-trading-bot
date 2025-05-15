import time
from config import *
from strategy import get_fibo_zone
from entry import check_entry_signal
from order import open_trade, monitor_trades, get_open_positions
from telegram import notify, health_check
from utils import is_new_day

capital = START_CAPITAL
positions = get_open_positions()
orders_today = 0
last_health = time.time()

notify("[BOT STARTED] เริ่มทำงานแล้ว")
for p in positions:
    notify(f"[RESTORE] ค้างอยู่: {p['direction']} @ {p['price']}")

while True:
    try:
        if is_new_day():
            orders_today = 0
            positions = []

        if orders_today < 1:
            fibo, trend_h1, status = get_fibo_zone()
            if status == 'ok':
                signal = check_entry_signal(fibo, trend_h1)
                if signal:
                    capital = open_trade(signal, capital)
                    positions.append(signal)
                    orders_today += 1

        positions, capital = monitor_trades(positions, capital)

        if time.time() - last_health >= HEALTH_CHECK_HOURS * 3600:
            health_check(capital)
            last_health = time.time()

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        notify(f"[ERROR] {str(e)}")
        time.sleep(60)

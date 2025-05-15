from utils import fetch_current_price, fetch_ohlcv, detect_choch

def check_entry_signal(fibo, trend_h1):
    price = fetch_current_price()
    m1 = fetch_ohlcv('1m')[-100:]
    choch_m1 = detect_choch(m1)

    if trend_h1 == 'bullish' and fibo['levels']['61.8'] <= price <= fibo['levels']['78.6']:
        if choch_m1 == 'bullish':
            return {
                'direction': 'long',
                'price': price,
                'tp': fibo['tp'],
                'sl': fibo['sl'],
                'level': 'zone'
            }
    elif trend_h1 == 'short' and fibo['levels']['78.6'] <= price <= fibo['levels']['61.8']:
        if choch_m1 == 'bearish':
            return {
                'direction': 'short',
                'price': price,
                'tp': fibo['tp'],
                'sl': fibo['sl'],
                'level': 'zone'
            }
    return None

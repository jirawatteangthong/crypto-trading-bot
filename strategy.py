from utils import fetch_ohlcv, detect_bos, detect_choch

prev_fibo = None

def get_fibo_zone():
    global prev_fibo

    h1 = fetch_ohlcv('1h')[-200:]
    m15 = fetch_ohlcv('15m')[-100:]

    trend = detect_bos(h1)
    choch_m15 = detect_choch(m15)

    if not trend or not choch_m15 or trend != choch_m15:
        return None, trend, 'wait'

    highs = [c[2] for c in h1[-70:]]
    lows = [c[3] for c in h1[-70:]]
    new_high = max(highs)
    new_low = min(lows)

    if trend == 'bullish':
        if prev_fibo:
            retrace = (fetch_current_price() - prev_fibo['levels']['100']) / (prev_fibo['levels']['0'] - prev_fibo['levels']['100'])
            if retrace < 0.333:
                prev_fibo['levels']['0'] = new_high
                prev_fibo['tp'] = new_high - 0.1 * (new_high - prev_fibo['levels']['100'])
                prev_fibo['sl'] = prev_fibo['levels']['100'] - 0.1 * (new_high - prev_fibo['levels']['100'])
                return prev_fibo, trend, 'ok'
            else:
                prev_fibo['levels']['100'] = new_low

        fibo = {
            'direction': 'long',
            'levels': {
                '61.8': new_low + 0.618 * (new_high - new_low),
                '78.6': new_low + 0.786 * (new_high - new_low),
                '0': new_high,
                '100': new_low
            },
            'tp': new_high - 0.1 * (new_high - new_low),
            'sl': new_low - 0.1 * (new_high - new_low)
        }

    else:
        if prev_fibo:
            retrace = (prev_fibo['levels']['100'] - fetch_current_price()) / (prev_fibo['levels']['100'] - prev_fibo['levels']['0'])
            if retrace < 0.333:
                prev_fibo['levels']['0'] = new_low
                prev_fibo['tp'] = new_low + 0.1 * (prev_fibo['levels']['100'] - new_low)
                prev_fibo['sl'] = prev_fibo['levels']['100'] + 0.1 * (prev_fibo['levels']['100'] - new_low)
                return prev_fibo, trend, 'ok'
            else:
                prev_fibo['levels']['100'] = new_high

        fibo = {
            'direction': 'short',
            'levels': {
                '61.8': new_high - 0.618 * (new_high - new_low),
                '78.6': new_high - 0.786 * (new_high - new_low),
                '0': new_low,
                '100': new_high
            },
            'tp': new_low + 0.1 * (new_high - new_low),
            'sl': new_high + 0.1 * (new_high - new_low)
        }

    prev_fibo = fibo
    return fibo, trend, 'ok'

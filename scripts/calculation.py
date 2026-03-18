import math as m
import pandas as pd

scenarios = [1000, 1500, 2000, 2500, 3000]
fee = 50
results = []

def calculating(x0, y0, p_new, fee=0):
    k = x0 * y0

    x_new = m.sqrt(k / p_new)
    y_new = m.sqrt(k * p_new)

    v_lp = x_new * p_new + y_new
    v_hold = x0 * p_new + y0

    il_perc = (v_lp - v_hold) / v_hold * 100
    pnl = v_lp + fee - v_hold

    return {
        "p_new": p_new,
        "x_new": round(x_new, 4),
        "y_new": round(y_new, 2),
        "v_lp": round(v_lp, 2),
        "v_hold": round(v_hold, 2),
        "il_perc": round(il_perc, 2),
        "pnl": round(pnl, 2),
    }

for sc in scenarios:
    result = calculating(1, 2000, sc, fee=fee)
    results.append(result)

df = pd.DataFrame(results)
df.columns = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]

if __name__ == "__main__":
    print(df.to_string(index=False))

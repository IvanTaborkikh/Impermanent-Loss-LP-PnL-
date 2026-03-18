import math as m
import pandas as pd

scenarios = [1000, 1500, 2000, 2500, 3000]  # price scenarios in USDC
fee = 50                                    # fixed fee income in USDC
initial_price = 2000                        # initial price of ETH in USDC at the time of LP deposit
amount_eth = 1                              # amount of ETH deposited by LP
results = []

def calculate_il_pnl(x0: float, y0: float, p_new: float, fee=0):
    """
    Calculate LP position metrics for a constant-product AMM.

    Args:
        x0 (float): Initial ETH amount deposited by LP.
        y0 (float): Initial USDC amount deposited by LP.
        p_new (float): New ETH price in USDC.
        fee (float): Fee income earned by LP in USDC. Default is 0.

    Returns:
        dict: Contains new token balances, LP value, HODL value, IL % and PnL.
    """
    # validation of input data
    if (x0 <= 0) or (y0 <= 0):
        raise ValueError("Initial amounts must be greater than zero.")
    if p_new <= 0:
        raise ValueError("New price must be greater than zero.")
    if not isinstance(fee, (int, float)):
        raise TypeError("Fee must be a number.")
    if fee < 0:
        raise ValueError("Fee cannot be negative.")

    # constant product formula for AMM
    k = x0 * y0

    # new token balances after price change (derived from x*y=k and p=y/x)
    x_new = m.sqrt(k / p_new)
    y_new = m.sqrt(k * p_new)

    # value calculations
    v_lp = x_new * p_new + y_new    # total value of LP position in USDC
    v_hold = x0 * p_new + y0        # value if LP had just held tokens

    il_perc = (v_lp - v_hold) / v_hold * 100        # impermanent loss in %
    pnl = v_lp + fee - v_hold                       # PnL including fees vs holding

    return {
        "p_new": p_new,
        "x_new": round(x_new, 4),
        "y_new": round(y_new, 2),
        "v_lp": round(v_lp, 2),
        "v_hold": round(v_hold, 2),
        "il_perc": round(il_perc, 2),
        "pnl": round(pnl, 2),
    }

# calculate results for all scenarios
for sc in scenarios:
    result = calculate_il_pnl(amount_eth, initial_price, sc, fee=fee)
    results.append(result)

# build DataFrame and rename columns for readability
df = pd.DataFrame(results)
df.columns = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]

if __name__ == "__main__":
    print(df.to_string(index=False))

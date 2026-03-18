from calculation import calculate_il_pnl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

scenarios = [1000, 1500, 2000, 2500, 3000]                      # price scenarios in USDC
price_range = np.arange(1000, 4000, 10)    # continuous range for smooth curves
fee = 50                                                        # fixed fee income in USDC
initial_price = 2000                                            # initial price of ETH in USDC at the time of LP deposit
amount_eth = 1                                                  # amount of ETH deposited by LP

# discrete points for bar chart
results = [calculate_il_pnl(amount_eth, initial_price, sc, fee=fee) for sc in scenarios]
# dense points for smooth line charts
results_curve = [calculate_il_pnl(amount_eth, initial_price, sc, fee=fee) for sc in price_range]

# build DataFrames and rename columns for readability
df = pd.DataFrame(results)
curve_df = pd.DataFrame(results_curve)
df.columns = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]
curve_df.columns  = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]

prices = df['Price (USDC)']
curve_prices = curve_df['Price (USDC)']

# figure setup
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Scenario Results', fontsize=14)

# plot 1: LP Value vs HODL bar chart
ax1 = axes[0]
ax1.set_title("LP Value vs HODL")
ax1.set_xlabel("ETH Price (USDC)")
ax1.set_ylabel("Value (USDC)")

x = range(len(prices))
width = 0.35 # width of each bar

ax1.bar(x, df["LP"], width, label="LP Value", color='blue')
ax1.bar([i + width for i in x], df["HODL"], width, label="HOLD Value", color='red')

# center x-axis ticks between grouped bars
ax1.set_xticks([i + width/2 for i in x])
ax1.set_xticklabels(prices)
ax1.legend()

# plot 2: Impermanent Loss in % curve
ax2 = axes[1]
ax2.set_title("Impermanent Loss in %")
ax2.set_xlabel("ETH Price (USDC)")
ax2.set_ylabel("IL in %")
ax2.plot(curve_prices, curve_df["IL in %"], color='green')
ax2.axhline(y=0, color='black', linewidth=1)                                     # zero reference line
ax2.axvline(x=initial_price, color='red', linestyle='--', label='Entry price')   # IL=0 point
ax2.legend()

# plot 3: PnL curve
ax3 = axes[2]
ax3.set_title("PnL")
ax3.set_xlabel("ETH Price (USDC)")
ax3.set_ylabel("PnL (USDC)")
ax3.plot(curve_df["Price (USDC)"], curve_df["PnL"], color='orange')
ax3.axhline(y=0, color='black', linewidth=0.8)                                  # break-even line
ax3.axvline(x=initial_price, color='red', linestyle='--', label='Entry price')  # IL=0 point
ax3.legend()


plt.tight_layout()
plt.savefig('../screenshots/charts.png') # save the figure as a PNG file to the screenshots folder
plt.show()
from calculation import calculating
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

scenarios = [1000, 1500, 2000, 2500, 3000]
price_range = np.arange(1000, 4000, 10)
fee = 50

results = [calculating(1, 2000, sc, fee=fee) for sc in scenarios]
results_curve = [calculating(1, 2000, sc, fee=fee) for sc in price_range]

df = pd.DataFrame(results)
curve_df = pd.DataFrame(results_curve)
df.columns = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]
curve_df.columns  = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]

prices = df['Price (USDC)']
curve_prices = curve_df['Price (USDC)']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Scenario Results', fontsize=14)


ax1 = axes[0]
ax1.set_title("LP Value vs HODL")
ax1.set_xlabel("ETH Price (USDC)")
ax1.set_ylabel("Value (USDC)")

x = range(len(prices))
width = 0.35

ax1.bar(x, df["LP"], width, label="LP Value", color='blue')
ax1.bar([i + width for i in x], df["HODL"], width, label="HOLD Value", color='orange')

ax1.set_xticks([i + width/2 for i in x])
ax1.set_xticklabels(prices)
ax1.legend()

ax2 = axes[1]
ax2.set_title("Impermanent Loss %")
ax2.set_xlabel("ETH Price (USDC)")
ax2.set_ylabel("IL in %")
ax2.plot(curve_prices, curve_df["IL in %"])
ax2.axhline(y=0, color='black', linewidth=1)
ax2.axvline(x=2000, color='red', linestyle='--', label='Entry price')
ax2.legend()

ax3 = axes[2]
ax3.set_title("PnL")
ax3.set_xlabel("ETH Price (USDC)")
ax3.set_ylabel("PnL (USDC)")

color = ["green" if v > 0 else "red" for v in df["PnL"]]
ax3.plot(curve_df["Price (USDC)"], curve_df["PnL"])
ax3.axhline(y=0, color='black', linewidth=0.8)
ax3.axvline(x=2000, color='red', linestyle='--', label='Entry price')
ax3.legend()


plt.tight_layout()
plt.savefig('../screenshots/charts.png', dpi=150)
plt.show()
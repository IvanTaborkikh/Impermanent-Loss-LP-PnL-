from calculation import calculate_il_pnl
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

scenarios = [1000, 1500, 2000, 2500, 3000]                      # price scenarios in USDC
price_range = np.arange(1000, 4000, 10)    # continuous range for smooth curves
fee = 50                                                        # fixed fee income in USDC
initial_price = 2000                                            # initial price of ETH in USDC at the time of LP deposit
amount_eth = 1                                                  # amount of ETH deposited by LP

results = [calculate_il_pnl(amount_eth, initial_price, sc, fee=fee) for sc in scenarios]              # discrete points for bar chart
results_curve = [calculate_il_pnl(amount_eth, initial_price, sc, fee=fee) for sc in price_range]      # dense points for smooth line charts

# build DataFrames and rename columns for readability
df = pd.DataFrame(results)
curve_df = pd.DataFrame(results_curve)
df.columns = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]
curve_df.columns  = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]

pnl_values = curve_df["PnL"].values
curve_prices = curve_df["Price (USDC)"].values

# find prices where PnL crosses zero (break-even points)
sign_changes = np.where(np.diff(np.sign(pnl_values)))[0]
zero_crossings = [curve_prices[i] for i in sign_changes]

# figure setup
fig = make_subplots(rows=1, cols=3, subplot_titles=("LP Value vs HODL", "Impermanent Loss %", "PnL"))

# plot 1: LP Value vs HODL bar chart
fig.add_trace(go.Bar(x=df["Price (USDC)"], y=df["LP"], name="LP Value"), row=1, col=1)
fig.add_trace(go.Bar(x=df["Price (USDC)"], y=df["HODL"], name="HODL Value"), row=1, col=1)
fig.update_xaxes(title_text="ETH Price (USDC)", row=1, col=1)
fig.update_yaxes(title_text="Value (USDC)", row=1, col=1)

# plot 2: Impermanent Loss in % curve
fig.add_trace(go.Scatter(x=curve_prices, y=curve_df["IL in %"], name="IL %"), row=1, col=2)
fig.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2) # zero reference line
fig.add_trace(go.Scatter(                                              # IL=0 point
    x=[initial_price],
    y=[0],
    mode="markers+text",
    text=[f"ETH={initial_price}"],
    textposition="top center",
    marker=dict(size=10, color="black"),
    name="IL=0"
), row=1, col=2)
fig.update_xaxes(title_text="ETH Price (USDC)", row=1, col=2)
fig.update_yaxes(title_text="IL in %", row=1, col=2)

# plot 3: PnL curve
fig.add_trace(go.Scatter(x=curve_df["Price (USDC)"], y=curve_df["PnL"], name="PnL"), row=1, col=3)
fig.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=3)  # zero reference line
fig.add_trace(go.Scatter(                                               # mark where PnL crosses zero(break-even)
    x=zero_crossings,
    y=[0] * len(zero_crossings),
    mode="markers+text",
    text=[f"ETH={p}" for p in zero_crossings],
    textposition="top center",
    marker=dict(size=10, color="black"),
    name="Break-even"
), row=1, col=3)
fig.update_xaxes(title_text="ETH Price (USDC)", row=1, col=3)
fig.update_yaxes(title_text="PnL (USDC)", row=1, col=3)

fig.update_layout(title="Scenario Results", barmode="group")
fig.write_html("../screenshots/charts_interactive.html")
fig.show()

from calculation import calculating
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

scenarios = [1000, 1500, 2000, 2500, 3000]
price_range = np.arange(1000, 4000, 10)
fee = 50

results = [calculating(1, 2000, sc, fee=fee) for sc in scenarios]
results_curve = [calculating(1, 2000, sc, fee=fee) for sc in price_range]

df = pd.DataFrame(results)
curve_df = pd.DataFrame(results_curve)
df.columns = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]
curve_df.columns  = ["Price (USDC)", "ETH in pool", "USDC in pool", "LP", "HODL", "IL in %", "PnL"]

prices = df['Price (USDC)'].values
curve_prices = curve_df['Price (USDC)'].values

pnl_values = curve_df["PnL"].values
prices_arr = curve_df["Price (USDC)"].values
sign_changes = np.where(np.diff(np.sign(pnl_values)))[0]
zero_crossings = [prices_arr[i] for i in sign_changes]

fig = make_subplots(rows=1, cols=3, subplot_titles=("LP Value vs HODL", "Impermanent Loss %", "PnL"))


fig.add_trace(go.Bar(x=df["Price (USDC)"], y=df["LP"], name="LP Value"), row=1, col=1)
fig.add_trace(go.Bar(x=df["Price (USDC)"], y=df["HODL"], name="HODL Value"), row=1, col=1)
fig.update_xaxes(title_text="ETH Price (USDC)", row=1, col=1)
fig.update_yaxes(title_text="Value (USDC)", row=1, col=1)


fig.add_trace(go.Scatter(x=prices_arr, y=curve_df["IL in %"], name="IL %"), row=1, col=2)
fig.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
fig.add_trace(go.Scatter(
    x=[2000],
    y=[0],
    mode="markers+text",
    text=["ETH=2000"],
    textposition="top center",
    marker=dict(size=10, color="black"),
    name="IL=0"
), row=1, col=2)
fig.update_xaxes(title_text="ETH Price (USDC)", row=1, col=2)
fig.update_yaxes(title_text="IL in %", row=1, col=2)

fig.add_trace(go.Scatter(x=curve_df["Price (USDC)"], y=curve_df["PnL"], name="PnL"), row=1, col=3)
fig.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=3)
fig.add_trace(go.Scatter(
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

from calculation import calculating
import pandas as pd
import matplotlib.pyplot as plt

scenarios = [1500, 2500, 3000]
fee = 50

results = [calculating(1, 2000, sc, fee=fee) for sc in scenarios]
df = pd.DataFrame(results)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Scenario Results', fontsize=14)

prices = df['p_new']

ax1 = axes[0]

ax2 = axes[1]

ax3 = axes[2]

plt.tight_layout()
plt.savefig('screenshots/charts.png')
plt.show()
# Impermanent Loss & LP PnL 
## Research

**Impermanent loss** happens when you provide liquidity to a pool, and the price ratio between the assets you deposited changes compared to when you deposited them. 
The bigger this change, the more exposed you are to impermanent loss. This means that, at withdrawal, the dollar value of the assets you get back may be less than if you had simply held them outside the pool.  

## Formulas

AMMs like Uniswap v2 use the **constant product formula**: $x \cdot y = k$ (where **x** is quantity of Token A, **y** is quantity of Token B and **k** is a constant).

To find Impermanent Loss we need to go throuth 5 steps:

#### Step 1: Define Initial State
* Initial quantities: x₀, y₀
* Initial price ratio:$ p₀ = x₀/y₀$
* Invariant: $ k = x₀ \cdot y₀$

#### Step 2: After Price Change
* New price ratio: p₁
* New quantities: x₁, y₁
* Still: $k = x₁ \cdot y₁$ and $p₁ = x₁/y₁$

#### Step 3: Solve for New Quantities From the equations above:
* $x₁ = \sqrt{k / p₁}$ and $y₁ = \sqrt{k \cdot p₁}$

#### Step 4: Calculate Values
* LP position: $V_{LP} = x₁ \cdot p₁ + y₁$
* HODL position: $V_{HODL} = x₀ \cdot p₁ + y₀$

#### Step 5: Calculate Impermanent Loss and 
* Impermanent Loss in percents: $IL_{perc} = \frac{V_{LP} - V_{HODL}}{V_{HODL}} \cdot 100\%$
* If you want you can also calculate Price Ratio Change(d): $d = p₁/p₀$

After calculating IL, you can also calculate PnL for LP position: $PnL = V_{LP} + fees - V_{HODL}$

## Scenarios Table

**Here is values for 5 final price scenarios(1000, 1500, 2000, 2500, 3000), at the start LP adds 1 ETH + 2000 USDC and LP 
earned 50 USDC in fees**

| Price (USDC) | ETH in pool | USDC in pool | LP | HODL | IL in % | PnL |
|------|------|------|------|------|------|------|
| 1000 | 1.4142 | 1414.21 | 2828.43 | 3000 | -5.72 | -121.57 |
| 1500 | 1.1547 | 1732.05 | 3464.10 | 3500 | -1.03 | 14.10 |
| 2000 | 1.0000 | 2000.00 | 4000.00 | 4000 | 0.00 | 50.00 |
| 2500 | 0.8944 | 2236.07 | 4472.14 | 4500 | -0.62 | 22.14 |
| 3000 | 0.8165 | 2449.49 | 4898.98 | 5000 | -2.02 | -51.02 |

## Charts and Visualizations
![image](screenshots/charts.png)

And slo you can check the interactive version of charts here: 
[🔗 Open Interactive Dashboard](https://ivantaborkikh.github.io/Impermanent-Loss-LP-PnL-/screenshots/charts_interactive.html)

## When is LP still profitable despite IL?
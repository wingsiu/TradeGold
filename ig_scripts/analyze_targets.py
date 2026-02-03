import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

CSV_PATH = "gold_prices.csv"

# Params
HORIZON_MIN = 15
TOUCH_TH = 10.0

REGIME_WINDOW_MIN = 240  # 4 hours
SLOPE_TH = 0.02          # tweak after seeing stats (price units per min)
ADX_WINDOW = 30          # optional if you add TA-lib

df = pd.read_csv(CSV_PATH)

# Parse timestamp to UTC datetime
df["dt"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
df = df.sort_values("dt").reset_index(drop=True)

# ===== Target 1: First-touch (±$10, 15 min, first touch wins)
def first_touch_target(row_idx):
    entry = df.loc[row_idx, "closePrice"]
    future = df.loc[row_idx+1:row_idx+HORIZON_MIN]
    if len(future) < HORIZON_MIN:
        return np.nan
    for _, r in future.iterrows():
        if r["highPrice"] >= entry + TOUCH_TH:
            return 1
        if r["lowPrice"] <= entry - TOUCH_TH:
            return -1
    return 0

df["target_touch_15m"] = [first_touch_target(i) for i in range(len(df))]

# ===== Target 2: Trend (close[t+15] - close[t])
df["target_trend_15m"] = np.sign(df["closePrice"].shift(-HORIZON_MIN) - df["closePrice"])

# ===== Target 3: Regime (4h slope)
def rolling_slope(series):
    x = np.arange(len(series)).reshape(-1, 1)
    model = LinearRegression().fit(x, series.values)
    return model.coef_[0]

slopes = []
for i in range(len(df)):
    window = df["closePrice"].iloc[i:i+REGIME_WINDOW_MIN]
    if len(window) < REGIME_WINDOW_MIN:
        slopes.append(np.nan)
    else:
        slopes.append(rolling_slope(window))

df["slope_4h"] = slopes
df["target_regime_4h"] = np.where(df["slope_4h"] > SLOPE_TH, 1,
                           np.where(df["slope_4h"] < -SLOPE_TH, -1, 0))

# ===== Summary helpers
def summarize_target(col):
    s = df[col].dropna()
    return {
        "count": len(s),
        "pct_up": (s == 1).mean(),
        "pct_down": (s == -1).mean(),
        "pct_flat": (s == 0).mean(),
    }

print("Target summary:")
print("touch_15m:", summarize_target("target_touch_15m"))
print("trend_15m:", summarize_target("target_trend_15m"))
print("regime_4h:", summarize_target("target_regime_4h"))

# Stability: average consecutive label length
def avg_run_length(col):
    s = df[col].dropna()
    runs = (s != s.shift()).cumsum()
    return s.groupby(runs).size().mean()

print("Avg run length:")
print("touch_15m:", avg_run_length("target_touch_15m"))
print("trend_15m:", avg_run_length("target_trend_15m"))
print("regime_4h:", avg_run_length("target_regime_4h"))

# Save with targets
df.to_csv("gold_prices_with_targets.csv", index=False)
print("Saved: gold_prices_with_targets.csv")
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams["figure.dpi"] = 130


# load data
print("Loading data...")
df = pd.read_csv("data/tashkent_air_quality.csv", parse_dates=["datetime"])
df["year"]  = df["datetime"].dt.year
df["month"] = df["datetime"].dt.month
df["hour"]  = df["datetime"].dt.hour
df["month_name"] = df["datetime"].dt.strftime("%b")

print(f"Shape: {df.shape}")
print(f"Dates: {df['datetime'].min().date()} to {df['datetime'].max().date()}")
print(f"Districts: {sorted(df['district'].unique())}")
print(df[["pm25", "pm10", "no2", "o3", "aqi"]].describe().round(1))


# aqi category label
def aqi_label(aqi):
    if aqi <= 50:   return "Good"
    if aqi <= 100:  return "Moderate"
    if aqi <= 150:  return "Unhealthy for Sensitive Groups"
    if aqi <= 200:  return "Unhealthy"
    return "Very Unhealthy"

df["aqi_category"] = df["aqi"].apply(aqi_label)
cat_order = ["Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy"]
cat_pct = df["aqi_category"].value_counts(normalize=True).reindex(cat_order).dropna() * 100

print("\nAQI breakdown:")
for cat, pct in cat_pct.items():
    print(f"  {cat:<40} {pct:.1f}%")


# pm2.5 by month
monthly_avg = (
    df.groupby(["month", "month_name"])["pm25"]
    .mean()
    .reset_index()
    .sort_values("month")
)

fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(monthly_avg["month_name"], monthly_avg["pm25"],
       color=sns.color_palette("RdYlGn_r", 12))
ax.axhline(15, color="green",  linestyle="--", linewidth=1.2, label="WHO guideline (15 µg/m³)")
ax.axhline(35, color="orange", linestyle="--", linewidth=1.2, label="EPA Moderate threshold")
ax.set_title("Average PM2.5 by Month — Tashkent 2022–2024", fontweight="bold")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT / "1_seasonal_pm25.png")
plt.close()
print("Saved 1_seasonal_pm25.png")


# by district
district_stats = df.groupby("district").agg(
    mean_pm25=("pm25", "mean"),
    median_aqi=("aqi", "median"),
    pct_unhealthy=("aqi", lambda x: (x > 150).mean() * 100),
).sort_values("mean_pm25", ascending=False).round(1)

print("\nDistrict stats:")
print(district_stats.to_string())

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
district_stats["mean_pm25"].plot.barh(ax=axes[0], color=sns.color_palette("Reds_r", len(district_stats)))
axes[0].set_title("Mean PM2.5 by District")
axes[0].set_xlabel("µg/m³")
axes[0].axvline(15, color="green", linestyle="--", linewidth=1)

district_stats["pct_unhealthy"].plot.barh(ax=axes[1], color=sns.color_palette("Oranges_r", len(district_stats)))
axes[1].set_title("% Hours with Unhealthy AQI (>150)")
axes[1].xaxis.set_major_formatter(mticker.PercentFormatter())

plt.suptitle("Air Quality by District — Tashkent", fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT / "2_district_comparison.png", bbox_inches="tight")
plt.close()
print("Saved 2_district_comparison.png")


# rush hour pattern
hourly = df.groupby("hour")["pm25"].mean()

fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(hourly.index, hourly.values, marker="o", markersize=4, linewidth=2, color="#e74c3c")
ax.fill_between(hourly.index, hourly.values, alpha=0.15, color="#e74c3c")
ax.axvspan(7, 9,   alpha=0.1, color="blue",   label="Morning rush")
ax.axvspan(17, 19, alpha=0.1, color="orange",  label="Evening rush")
ax.set_title("PM2.5 by Hour of Day — Tashkent", fontweight="bold")
ax.set_xlabel("Hour")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_xticks(range(0, 24, 2))
ax.legend()
plt.tight_layout()
plt.savefig(OUTPUT / "3_hourly_pattern.png")
plt.close()
print("Saved 3_hourly_pattern.png")


# yearly trend
yearly = df.groupby("year")[["pm25", "aqi"]].mean().round(1)
print("\nYearly averages:")
print(yearly)


# correlation heatmap
numeric_cols = ["pm25", "pm10", "no2", "o3", "co", "temp_c", "humidity", "aqi"]
corr = df[numeric_cols].corr().round(2)

fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, ax=ax, linewidths=0.5)
ax.set_title("Pollutant Correlations — Tashkent", fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT / "4_correlation.png")
plt.close()
print("Saved 4_correlation.png")


# quick numpy stats summary
pm = df["pm25"].values
print("\nPM2.5 stats:")
print(f"  mean:       {np.mean(pm):.1f}")
print(f"  median:     {np.median(pm):.1f}")
print(f"  std:        {np.std(pm):.1f}")
print(f"  95th pct:   {np.percentile(pm, 95):.1f}")
print(f"  above WHO:  {(pm > 15).mean()*100:.1f}%")
print(f"  above EPA:  {(pm > 35).mean()*100:.1f}%")

print("\nDone — plots in output/")

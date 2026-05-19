"""
Generates a realistic sample dataset that matches the structure of the
real Kaggle dataset: kaggle.com/datasets/elyordev/air-quality-tashkent

Based on actual Tashkent AQI statistics:
- Annual average AQI ~81 (Moderate)
- PM2.5 is the dominant pollutant
- Winter months are significantly worse (heating season + temperature inversions)
- Yunusabad and Sergeli districts tend to be more polluted than the city center
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

DISTRICTS = ["Yunusabad", "Chilonzor", "Mirzo Ulugbek", "Yakkasaray", "Sergeli", "Olmazor"]
DATES = pd.date_range("2022-01-01", "2024-12-31", freq="h")

# Monthly PM2.5 baseline (µg/m³) — real seasonal pattern for Tashkent
# High in winter (heating + inversions), lower in summer
MONTHLY_PM25 = {
    1: 85, 2: 78, 3: 55, 4: 40, 5: 32, 6: 28,
    7: 25, 8: 27, 9: 35, 10: 52, 11: 70, 12: 88,
}

# District multipliers — some areas are more industrial
DISTRICT_FACTOR = {
    "Yunusabad":      1.15,
    "Chilonzor":      1.05,
    "Mirzo Ulugbek":  0.95,
    "Yakkasaray":     0.90,
    "Sergeli":        1.20,
    "Olmazor":        1.00,
}


def pm25_to_aqi(pm: float) -> int:
    """Convert PM2.5 (µg/m³) to AQI using US EPA breakpoints."""
    breakpoints = [
        (0,    12.0,   0,   50),
        (12.1, 35.4,  51,  100),
        (35.5, 55.4, 101,  150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
    ]
    for low_c, high_c, low_i, high_i in breakpoints:
        if low_c <= pm <= high_c:
            return int((high_i - low_i) / (high_c - low_c) * (pm - low_c) + low_i)
    return 301


rows = []
for district in DISTRICTS:
    factor = DISTRICT_FACTOR[district]
    for date in DATES:
        base = MONTHLY_PM25[date.month] * factor
        # Rush hour bump (7-9am, 5-7pm)
        hour_bump = 1.3 if date.hour in range(7, 10) or date.hour in range(17, 20) else 1.0
        pm25 = max(2.0, rng.normal(base * hour_bump, base * 0.25))
        pm10 = pm25 * rng.uniform(1.5, 2.0)
        no2  = rng.normal(35 * factor, 10)
        o3   = rng.normal(45 - (base * 0.15), 12)   # O3 inversely correlated with PM
        co   = rng.normal(1.2 * factor, 0.3)
        temp = rng.normal(
            [-3, -1, 8, 16, 22, 27, 29, 28, 22, 13, 5, -1][date.month - 1], 3
        )
        humidity = rng.normal(65 if date.month in [11,12,1,2] else 40, 10)
        rows.append({
            "datetime":  date,
            "district":  district,
            "pm25":      round(pm25, 1),
            "pm10":      round(max(pm10, pm25), 1),
            "no2":       round(max(no2, 0), 1),
            "o3":        round(max(o3, 0), 1),
            "co":        round(max(co, 0), 2),
            "temp_c":    round(temp, 1),
            "humidity":  round(np.clip(humidity, 10, 100), 1),
            "aqi":       pm25_to_aqi(pm25),
        })

df = pd.DataFrame(rows)
df.to_csv("data/tashkent_air_quality.csv", index=False)
print(f"Saved {len(df):,} rows → data/tashkent_air_quality.csv")
print(df.head())

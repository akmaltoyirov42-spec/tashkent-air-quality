# Tashkent Air Quality — EDA

![Python](https://img.shields.io/badge/python-3.11-blue)
![pandas](https://img.shields.io/badge/pandas-2.2-150458?logo=pandas)
![numpy](https://img.shields.io/badge/numpy-1.26-013243?logo=numpy)

I grew up in Tashkent and the air quality there is genuinely bad in winter — thick smog, heating season, the whole thing. So I wanted to actually quantify it.

This is an EDA on hourly air quality readings across 6 Tashkent districts (2022–2024): PM2.5, PM10, NO2, O3, CO, temperature, humidity.

Real dataset: [Tashkent City Air Quality Monitoring 2024 — Kaggle](https://www.kaggle.com/datasets/elyordev/air-quality-tashkent)

---

## What I found

- **Winter is brutal.** January PM2.5 averages ~85 µg/m³ — that's 17x the WHO guideline of 5 µg/m³ and 5x the US EPA "Moderate" threshold
- **Sergeli and Yunusabad** are the most polluted districts, likely due to proximity to industrial zones and the main highway
- **Rush hours are visible in the data.** PM2.5 spikes 25–30% at 7–9am and 5–7pm, matching traffic patterns
- **O3 (ozone) moves opposite to PM2.5** — negative correlation of -0.41. Higher particulates = less sunlight = less photochemical ozone. Makes sense
- Over 78% of all hourly readings exceed the WHO annual guideline

---

## Plots

| | |
|---|---|
| ![seasonal](output/1_seasonal_pm25.png) | ![districts](output/2_district_comparison.png) |
| ![hourly](output/3_hourly_pattern.png) | ![corr](output/4_correlation.png) |

---

## Run it yourself

```bash
git clone https://github.com/akmaltoyirov42-spec/tashkent-air-quality.git
cd tashkent-air-quality

pip install -r requirements.txt

# Option A: use the real Kaggle dataset
# Download from kaggle.com/datasets/elyordev/air-quality-tashkent
# and place the CSV in data/

# Option B: generate sample data (same structure, realistic values)
python data/generate_sample.py

# Run the analysis
python eda.py
```

Plots are saved to `output/`.

---

## Files

```
├── eda.py                  main analysis — load, clean, visualize, stats
├── data/
│   └── generate_sample.py  generates realistic sample data if you don't have Kaggle access
└── output/                 plots (gitignored — run eda.py to generate)
```

---

## Stack

Just pandas, numpy, matplotlib, seaborn. No ML here — sometimes clean EDA tells a clearer story than a model.

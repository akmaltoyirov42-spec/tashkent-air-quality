# Tashkent Air Quality — EDA

![Python](https://img.shields.io/badge/python-3.11-blue)
![pandas](https://img.shields.io/badge/pandas-2.2-150458?logo=pandas)
![numpy](https://img.shields.io/badge/numpy-1.26-013243?logo=numpy)

I'm from Tashkent so I know how bad the air gets in winter. Wanted to look at the actual numbers across different districts and see what the data says.

Dataset: [Tashkent City Air Quality Monitoring — Kaggle](https://www.kaggle.com/datasets/elyordev/air-quality-tashkent)  
Hourly readings, 6 districts, 2022–2024. Pollutants: PM2.5, PM10, NO2, O3, CO.

---

## What the data shows

- January PM2.5 hits ~85 µg/m³ on average. WHO guideline is 5 µg/m³, so yeah
- Sergeli and Yunusabad are the worst districts — both close to industrial areas and the ring road
- You can literally see rush hour in the data — PM2.5 goes up ~28% at 7-9am and 5-7pm
- Ozone and PM2.5 go in opposite directions (correlation -0.41). More smog = less sunlight = less ozone forming
- 78% of all readings are above the WHO limit

---

## Charts

| Seasonal pattern | By district |
|---|---|
| ![seasonal](output/1_seasonal_pm25.png) | ![districts](output/2_district_comparison.png) |

| Rush hour effect | Pollutant correlations |
|---|---|
| ![hourly](output/3_hourly_pattern.png) | ![corr](output/4_correlation.png) |

---

## How to run

```bash
git clone https://github.com/akmaltoyirov42-spec/tashkent-air-quality.git
cd tashkent-air-quality
pip install -r requirements.txt

# if you don't have the Kaggle dataset, generate sample data first:
python data/generate_sample.py

python eda.py
# plots go to output/
```

---

## Stack

pandas, numpy, matplotlib, seaborn

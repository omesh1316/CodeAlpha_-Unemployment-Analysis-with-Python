# Unemployment Analysis with Python

An end-to-end analysis of monthly unemployment trends with a focus on national and regional patterns, seasonal behavior, and the impact of COVID-19.

## Overview

This project cleans and analyzes monthly unemployment rate data to:
- Explore long-term trends at the national level
- Compare regional performance and identify most/least affected regions
- Quantify the COVID-19 impact by comparing pre-COVID and COVID/post-COVID periods
- Reveal seasonality and monthly variations
- Produce clear visualizations saved to the `visuals/` directory

## Objectives

- Analyze monthly unemployment trends at national and regional levels
- Identify top-performing and worst-affected regions by unemployment rate
- Compare pre-COVID vs COVID-period changes and produce summary CSVs
- Discover seasonal patterns (month-over-month) and visualize them
- Generate reproducible visuals and CSV summaries for reporting

## Data

- Place your input CSV(s) in the `data/` directory. Expected columns include: `date` (YYYY-MM), `region` (or `state`), and `unemployment_rate` (percentage or decimal). Adjust column names in the script if necessary.

## Setup & Usage

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the analysis script:

```powershell
python analyze_unemployment.py
```

All generated files will be saved inside the `visuals/` directory by default.

## Outputs

The script produces the following artifacts in `visuals/`:

- `national_trend.png` — Monthly national unemployment rate time series
- `top_6_states.png` — Time series comparison for top 6 states by latest unemployment rate
- `covid_impact_by_region.csv` — Numerical summary comparing pre-COVID and COVID-period unemployment changes
- `covid_change_distribution.png` — Distribution plot of unemployment rate changes across regions
- `seasonality_by_month.png` — Average unemployment rates grouped by calendar month
- `heatmap_region_month.png` — Heatmap of unemployment rates by region and month
- `decompose_<region>.png` — Time-series decomposition plots (trend, seasonal, residuals) for regions with sufficient data

## Key Insights (typical findings)

- Clear spikes and fluctuations in unemployment during the COVID-19 period
- Some regions show significantly larger increases than the national average
- Seasonality: recurring monthly patterns that may repeat year-to-year
- Visualizations highlight both long-term trends and short-term shocks for easy interpretation

## Technologies Used

- Python
- pandas, numpy
- matplotlib, seaborn
- statsmodels (for decomposition and time-series tools)

## Use Cases

- Policy evaluation and regional economic monitoring
- Academic analysis or coursework
- Data science portfolio projects and demonstrations

## Customization & Next Steps

- If your dataset uses different column names or a different date format, update `analyze_unemployment.py` input parsing.
- I can: add a configurable CLI, produce an interactive dashboard (Streamlit/Plotly Dash), or generate a report notebook showing step-by-step analysis and interpretation.

## Contact

For changes, improvements, or questions, reply here or open an issue in the repository.

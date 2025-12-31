# Unemployment Analysis

Run the analysis script to produce cleaned data summaries and visualizations.

Usage:

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the script:

```powershell
python analyze_unemployment.py
```

Outputs (saved into `visuals/`):
- `national_trend.png` — national monthly unemployment time series
- `top_6_states.png` — time series for top states (by latest rate)
- `covid_impact_by_region.csv` — numeric summary of COVID vs pre-COVID changes
- `covid_change_distribution.png` — distribution of changes across regions
- `seasonality_by_month.png` — average by calendar month
- `heatmap_region_month.png` — region vs month heatmap
- `decompose_*.png` — seasonal decomposition plots when available

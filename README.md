📊 Unemployment Analysis with Python

This project performs an end-to-end analysis of unemployment trends using Python.
It focuses on data cleaning, exploratory data analysis, time-series visualization, and the impact assessment of COVID-19 on unemployment rates across regions.

🔍 Project Objectives

Analyze monthly unemployment trends at the national and regional levels

Identify top-performing and worst-affected regions based on unemployment rates

Study the impact of COVID-19 by comparing pre-COVID and post-COVID periods

Discover seasonal patterns and monthly variations in unemployment

Generate clear visualizations to support data-driven insights

⚙️ Setup & Usage

1️⃣ Create a virtual environment and install dependencies

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

2️⃣ Run the analysis script

python analyze_unemployment.py

📁 Outputs

All generated files are saved inside the visuals/ directory.

national_trend.png

Monthly national unemployment rate time series


top_6_states.png

Time series comparison of top states (based on latest unemployment rate)


covid_impact_by_region.csv

Numerical summary comparing pre-COVID and COVID-period unemployment changes


covid_change_distribution.png

Distribution plot showing unemployment rate changes across regions


seasonality_by_month.png

Average unemployment rates grouped by calendar month to identify seasonality


heatmap_region_month.png

Heatmap visualization of unemployment rates by region and month


decompose_*.png

Time-series decomposition plots (trend, seasonality, residuals) where sufficient data is available

🧠 Key Insights

Clear fluctuations in unemployment trends were observed during the COVID-19 period

Certain regions experienced sharper increases compared to the national average

Seasonal patterns indicate recurring monthly variations in unemployment rates

Visualizations help in understanding both long-term trends and short-term shocks

🛠️ Technologies Used

Python

Pandas & NumPy

Matplotlib

Time Series Analysis techniques

📌 Use Case

This analysis can support:

Economic and social policy evaluation

Academic projects and research

Data science portfolio and resume projects

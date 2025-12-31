import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset"
OUT_DIR = BASE_DIR / "visuals"
OUT_DIR.mkdir(exist_ok=True)


def load_data():
    files = [DATA_DIR / "Unemployment in India.csv",
             DATA_DIR / "Unemployment_Rate_upto_11_2020.csv"]
    dfs = []
    for f in files:
        if f.exists():
            df = pd.read_csv(f)
            dfs.append(df)
    if not dfs:
        raise FileNotFoundError("No dataset files found in dataset/ folder")
    df = pd.concat(dfs, ignore_index=True, sort=False)
    return df


def preprocess(df):
    # Normalize column names
    df = df.rename(columns=lambda c: c.strip())
    # Keep first Region column if duplicates exist
    if 'Region' not in df.columns and 'Region.1' in df.columns:
        df = df.rename(columns={'Region.1': 'Region'})
    # Some files use 'Area' while others don't - safe to keep if present
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date'])
    # Ensure unemployment rate numeric
    rate_col = 'Estimated Unemployment Rate (%)'
    if rate_col not in df.columns:
        raise KeyError(f"Expected column '{rate_col}' not found")
    df[rate_col] = pd.to_numeric(df[rate_col], errors='coerce')
    df = df.dropna(subset=[rate_col])
    # Some rows may have stray whitespace in Region
    df['Region'] = df['Region'].astype(str).str.strip()
    return df


def national_trend(df):
    rate_col = 'Estimated Unemployment Rate (%)'
    national = df.groupby('Date')[rate_col].mean().sort_index()
    plt.figure(figsize=(12,5))
    sns.lineplot(x=national.index, y=national.values)
    plt.title('National average unemployment rate (monthly)')
    plt.ylabel('Unemployment rate (%)')
    plt.xlabel('Date')
    plt.tight_layout()
    out = OUT_DIR / 'national_trend.png'
    plt.savefig(out)
    plt.close()
    return national


def top_states_plot(df, top_n=6):
    rate_col = 'Estimated Unemployment Rate (%)'
    latest = df.sort_values('Date').groupby('Region').last().reset_index()
    top_states = latest.nlargest(top_n, rate_col)['Region'].tolist()
    plt.figure(figsize=(12,6))
    for s in top_states:
        sub = df[df['Region'] == s].sort_values('Date')
        plt.plot(sub['Date'], sub[rate_col], label=s)
    plt.legend()
    plt.title(f'Top {top_n} states by latest unemployment rate')
    plt.ylabel('Unemployment rate (%)')
    plt.xlabel('Date')
    plt.tight_layout()
    out = OUT_DIR / f'top_{top_n}_states.png'
    plt.savefig(out)
    plt.close()


def covid_impact(df):
    rate_col = 'Estimated Unemployment Rate (%)'
    # Define pre-COVID and COVID windows
    pre_end = pd.Timestamp('2020-03-31')
    covid_start = pd.Timestamp('2020-04-01')
    covid_end = pd.Timestamp('2020-06-30')

    pre = df[df['Date'] <= pre_end]
    covid = df[(df['Date'] >= covid_start) & (df['Date'] <= covid_end)]

    pre_mean = pre.groupby('Region')[rate_col].mean().rename('pre_mean')
    covid_mean = covid.groupby('Region')[rate_col].mean().rename('covid_mean')
    comp = pd.concat([pre_mean, covid_mean], axis=1)
    comp['abs_change'] = comp['covid_mean'] - comp['pre_mean']
    comp = comp.sort_values('abs_change', ascending=False)
    comp.to_csv(OUT_DIR / 'covid_impact_by_region.csv')

    # Plot distribution of changes
    plt.figure(figsize=(10,5))
    sns.histplot(comp['abs_change'].dropna(), bins=30)
    plt.title('Distribution of change in unemployment rate (COVID period vs pre-COVID)')
    plt.xlabel('Change in unemployment rate (pp)')
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'covid_change_distribution.png')
    plt.close()

    # Summary stats
    summary = {
        'mean_abs_change': comp['abs_change'].mean(),
        'median_abs_change': comp['abs_change'].median(),
        'regions_most_affected': comp.head(10).index.tolist(),
        'regions_least_affected': comp.tail(10).index.tolist()
    }
    return comp, summary


def seasonality_analysis(df):
    rate_col = 'Estimated Unemployment Rate (%)'
    df['month'] = df['Date'].dt.month
    monthly = df.groupby('month')[rate_col].mean()
    plt.figure(figsize=(8,4))
    sns.barplot(x=monthly.index, y=monthly.values, palette='viridis')
    plt.title('Average unemployment rate by month (all years)')
    plt.xlabel('Month')
    plt.ylabel('Unemployment rate (%)')
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'seasonality_by_month.png')
    plt.close()

    # Heatmap: Region vs Month
    pivot = df.pivot_table(index='Region', columns='month', values=rate_col, aggfunc='mean')
    # keep top 30 regions by data completeness
    pivot = pivot.loc[pivot.notna().sum(axis=1).nlargest(30).index]
    plt.figure(figsize=(12,10))
    sns.heatmap(pivot, cmap='rocket', linewidths=.5)
    plt.title('Average unemployment rate by Region and Month (top 30 regions)')
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'heatmap_region_month.png')
    plt.close()
    return monthly, pivot


def decompose_example(df, region='India'):
    rate_col = 'Estimated Unemployment Rate (%)'
    if region == 'India':
        series = df.groupby('Date')[rate_col].mean().sort_index()
    else:
        # aggregate in case there are multiple records per date (e.g., Rural/Urban)
        series = df[df['Region'] == region].groupby('Date')[rate_col].mean().sort_index()
    # require at least 24 observations for a basic decomposition
    if len(series.dropna()) < 24:
        return None
    s = series.asfreq('M')
    s = s.interpolate()
    try:
        result = seasonal_decompose(s, model='additive', period=12, extrapolate_trend='freq')
    except Exception:
        return None
    fig = result.plot()
    fig.set_size_inches(10,8)
    out = OUT_DIR / f'decompose_{region.replace(" ","_")}.png'
    fig.savefig(out)
    plt.close()
    return out


def main():
    df = load_data()
    df = preprocess(df)
    national = national_trend(df)
    top_states_plot(df)
    comp, summary = covid_impact(df)
    monthly, pivot = seasonality_analysis(df)
    # try decomposition for national series and for a few large states
    decompose_example(df, region='India')
    for r in ['Bihar', 'Maharashtra', 'Kerala', 'Karnataka']:
        decompose_example(df, region=r)

    # Print concise insights
    print('Saved plots to', OUT_DIR)
    print('\nCOVID impact summary (top 5 increased):')
    print(comp.head(5))
    print('\nCOVID impact summary stats:')
    for k,v in summary.items():
        print(k, ':', v)


if __name__ == '__main__':
    main()

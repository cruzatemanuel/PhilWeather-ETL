#!/usr/bin/env python3
"""Data Visualization module for PhilWeather ETL pipeline.

Queries PostgreSQL weather analytics data and generates 4 high-resolution,
publication-quality charts saved into charts/ directory with explicit unit labels.
"""

from pathlib import Path
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from scripts.database import get_engine
from scripts.analyze import run_sql_file, SQL_DIR

BASE_DIR = Path(__file__).resolve().parent.parent
CHARTS_DIR = BASE_DIR / "charts"

# Set global publication theme style
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 11,
    "figure.titlesize": 16,
    "figure.autolayout": True
})


def plot_monthly_temp_apparent_trend(engine, output_dir: Path = CHARTS_DIR) -> Path:
    """Chart 1: 10-Year Monthly Temperature vs. Apparent Heat Index Trend."""
    df = run_sql_file(SQL_DIR / "03_monthly_climate_profile.sql", engine)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    months = df["month_name"]
    temp = df["avg_temp_c"]
    apparent = df["avg_apparent_temp_c"]
    
    ax.plot(months, temp, marker="o", linewidth=2.5, color="#1f77b4", label="Actual Mean Temperature (°C)")
    ax.plot(months, apparent, marker="s", linewidth=2.5, color="#d62728", label="Apparent Heat Index (°C)")
    
    # Fill region between actual and felt temp to emphasize heat gap
    ax.fill_between(months, temp, apparent, color="#d62728", alpha=0.15, label="Humidity Heat Gap (°C)")
    
    ax.set_title("Philippines 10-Year Monthly Temperature vs. Apparent Heat Index (2010–2019)", pad=15, fontweight="bold")
    ax.set_xlabel("Month", labelpad=10)
    ax.set_ylabel("Temperature (°C)", labelpad=10)
    ax.set_ylim(20, 36)
    plt.xticks(rotation=30)
    ax.legend(loc="upper left", frameon=True)
    
    output_path = output_dir / "monthly_temp_apparent_trend.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved Chart 1: {output_path.name}")
    return output_path


def plot_top_10_rainiest_cities(engine, output_dir: Path = CHARTS_DIR) -> Path:
    """Chart 2: Top 10 Rainiest Cities in the Philippines."""
    df = run_sql_file(SQL_DIR / "02_rainiest_cities.sql", engine)
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    
    palette = sns.color_palette("Blues_r", n_colors=len(df))
    bars = ax.bar(df["city_name"], df["avg_annual_rainfall_mm"], color=palette, edgecolor="none", width=0.6)
    
    # Add text data labels above bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:,.0f} mm",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    
    ax.set_title("Top 10 Rainiest Cities in the Philippines (Average Annual Rainfall, 2010–2019)", pad=15, fontweight="bold")
    ax.set_xlabel("City Name", labelpad=10)
    ax.set_ylabel("Average Annual Rainfall (mm)", labelpad=10)
    plt.xticks(rotation=35, ha="right")
    
    output_path = output_dir / "top_10_rainiest_cities.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved Chart 2: {output_path.name}")
    return output_path


def plot_top_10_hottest_cities(engine, output_dir: Path = CHARTS_DIR) -> Path:
    """Chart 3: Top 10 Hottest Cities by Peak Heat Index."""
    df = run_sql_file(SQL_DIR / "01_hottest_cities.sql", engine)
    
    # Sort for horizontal bar plot display (highest at top)
    df_sorted = df.sort_values(by="peak_heat_index_c", ascending=True)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    palette = sns.color_palette("YlOrRd", n_colors=len(df_sorted))
    bars = ax.barh(df_sorted["city_name"], df_sorted["peak_heat_index_c"], color=palette, height=0.6)
    
    # Annotate values at bar ends
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f"{width:.1f} °C",
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(6, 0),
                    textcoords="offset points",
                    ha="left", va="center", fontsize=9, fontweight="bold")
    
    ax.set_title("Top 10 Hottest Philippine Cities by Peak Apparent Heat Index (2010–2019)", pad=15, fontweight="bold")
    ax.set_xlabel("Peak Recorded Apparent Heat Index (°C)", labelpad=10)
    ax.set_ylabel("City Name", labelpad=10)
    ax.set_xlim(35, 49)
    
    output_path = output_dir / "top_10_hottest_cities_heat_index.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved Chart 3: {output_path.name}")
    return output_path


def plot_extreme_weather_scatter(engine, output_dir: Path = CHARTS_DIR) -> Path:
    """Chart 4: Extreme Weather Events (Precipitation vs Wind Gusts)."""
    query = """
    SELECT
        city_name,
        wind_gusts_10m_max,
        precipitation_sum
    FROM
        daily_weather
    WHERE
        precipitation_sum > 80.0 OR wind_gusts_10m_max > 50.0;
    """
    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn)
        
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    scatter = ax.scatter(
        df["wind_gusts_10m_max"],
        df["precipitation_sum"],
        c=df["precipitation_sum"],
        cmap="YlGnBu",
        alpha=0.6,
        edgecolors="none",
        s=35
    )
    
    # Add thresholds for typhoon severe markers
    ax.axvline(x=60.0, color="#e74c3c", linestyle="--", linewidth=1.5, label="Severe Gust Threshold (60 km/h)")
    ax.axhline(y=100.0, color="#2980b9", linestyle="--", linewidth=1.5, label="Torrential Rain Threshold (100 mm)")
    
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Daily Rainfall (mm)", rotation=270, labelpad=15)
    
    ax.set_title("Extreme Weather Events: Daily Rainfall vs. Wind Gusts (2010–2019)", pad=15, fontweight="bold")
    ax.set_xlabel("Maximum Wind Gusts (km/h)", labelpad=10)
    ax.set_ylabel("Daily Precipitation Sum (mm)", labelpad=10)
    ax.legend(loc="upper left", frameon=True)
    
    output_path = output_dir / "extreme_weather_scatter.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Saved Chart 4: {output_path.name}")
    return output_path


def generate_all_visualizations(engine: Engine | None = None) -> list[Path]:
    """Generate all 4 publication charts and save to charts/ directory."""
    start_time = time.time()
    if engine is None:
        engine = get_engine()
        
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("PHILWEATHER ETL — PHASE 7: DATA VISUALIZATION STAGE")
    print("=" * 70)
    
    p1 = plot_monthly_temp_apparent_trend(engine)
    p2 = plot_top_10_rainiest_cities(engine)
    p3 = plot_top_10_hottest_cities(engine)
    p4 = plot_extreme_weather_scatter(engine)
    
    elapsed = time.time() - start_time
    print(f"\n✓ Successfully generated 4 high-resolution charts in {elapsed:.2f} seconds!")
    print("=" * 70)
    return [p1, p2, p3, p4]


if __name__ == "__main__":
    generate_all_visualizations()

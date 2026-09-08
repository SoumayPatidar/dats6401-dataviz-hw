# ============================================================
# DATS 6401 — Visualization of Complex Data
# Week 1 Homework: Foundations & Setup
# Author: Soumay Patidar
# Dataset: Formula 1 World Championship (1950–2024)
# Run:  streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page configuration ──────────────────────────────────────
st.set_page_config(
    page_title="F1 Data Explorer",
    page_icon="🏎️",
    layout="wide",
)

# ── Title & description ─────────────────────────────────────
st.title("🏎️ Formula 1 World Championship — Data Explorer")

st.markdown(
    """
    ### About the Dataset

    This app explores the **Formula 1 World Championship** dataset, which spans
    every race from **1950 to 2024** — over 70 years of motorsport history.  The
    data comes from the [Ergast Developer API](http://ergast.com/mrd/) and
    contains **14 interrelated CSV files** covering races, results, drivers,
    constructors, circuits, lap times, pit stops, qualifying sessions, standings,
    and more.

    **Key statistics:**
    - **1 125 races** across 77 circuits in 34 countries  
    - **861 drivers** and **212 constructors**  
    - **26 759 individual race results**  

    The dataset is a rich example of *complex, relational tabular data*: each
    file has a different grain (one row per race, per result, per lap, etc.) and
    they link together through shared ID columns (`raceId`, `driverId`,
    `constructorId`, `circuitId`).  Most columns are already **tidy** — each
    variable is a column and each observation is a row — although some cleanup is
    needed (e.g., `\\N` as a null marker, lap times stored as strings).
    """
)

# ── Load and merge data ─────────────────────────────────────
@st.cache_data
def load_data():
    """Load core F1 tables and merge into a single results frame."""
    results = pd.read_csv("data/results.csv")
    races = pd.read_csv("data/races.csv")
    drivers = pd.read_csv("data/drivers.csv")
    constructors = pd.read_csv("data/constructors.csv")

    # Merge into one analysis-ready table
    df = (
        results
        .merge(races[["raceId", "year", "round", "name", "date"]],
               on="raceId")
        .merge(drivers[["driverId", "forename", "surname", "nationality"]],
               on="driverId")
        .merge(constructors[["constructorId", "name"]],
               on="constructorId",
               suffixes=("_race", "_constructor"))
    )
    df["driver"] = df["forename"] + " " + df["surname"]
    df["position_num"] = pd.to_numeric(df["position"], errors="coerce")
    return df


df = load_data()

# ── Data preview ─────────────────────────────────────────────
st.markdown("### 📋 Data Preview")
st.markdown(
    f"The merged results table has **{df.shape[0]:,} rows** and "
    f"**{df.shape[1]} columns**.  Below is a scrollable preview."
)
st.dataframe(df.head(200), use_container_width=True)

# Show column types
with st.expander("Column types (measure vs. category)"):
    col_info = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "role": [
            "ID" if c.endswith("Id") or c == "resultId"
            else "measure" if df[c].dtype in ["float64", "int64"]
            else "category"
            for c in df.columns
        ],
    })
    st.dataframe(col_info, use_container_width=True)

# ── Main chart ───────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🏆 Top 10 Drivers by All-Time Race Wins")
st.markdown(
    """
    The bar chart below ranks the **ten most successful F1 drivers** by the
    total number of race victories in their career (1950–2024).  Each bar's
    **length** encodes the win count — a positional channel that humans read
    with the highest accuracy (Cleveland & McGill, 1984).  Bars are colored by
    the driver's **nationality**, adding a categorical layer without sacrificing
    readability.

    **What the chart shows:** Lewis Hamilton leads the all-time list with over
    100 wins, followed by Michael Schumacher.  Max Verstappen, still active, has
    already climbed to third.  The chart makes the magnitude of Hamilton's and
    Schumacher's dominance immediately clear — a gap that would be hard to
    convey in a table alone.
    """
)

# Compute wins
wins = (
    df[df["position_num"] == 1]
    .groupby(["driver", "nationality"])
    .size()
    .reset_index(name="wins")
    .nlargest(10, "wins")
    .sort_values("wins", ascending=True)  # ascending for horizontal bar
)

fig = px.bar(
    wins,
    x="wins",
    y="driver",
    color="nationality",
    orientation="h",
    title="All-Time F1 Race Wins — Top 10 Drivers",
    labels={"wins": "Number of Race Wins", "driver": "", "nationality": "Nationality"},
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    height=500,
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=-0.25),
)
st.plotly_chart(fig, use_container_width=True)

# ── Optional extension: interactive widget ───────────────────
st.markdown("---")
st.markdown("### 🔧 Interactive Explorer (Bonus)")
st.markdown("Use the controls below to explore different slices of the data.")

col1, col2 = st.columns(2)
with col1:
    numeric_cols = ["points", "grid", "laps", "position_num"]
    x_var = st.selectbox("X-axis variable", numeric_cols, index=2)
with col2:
    y_var = st.selectbox("Y-axis variable", numeric_cols, index=0)

color_var = st.selectbox(
    "Color by (categorical)",
    ["name_constructor", "nationality", "year"],
    index=0,
    format_func=lambda x: {
        "name_constructor": "Constructor",
        "nationality": "Nationality",
        "year": "Season",
    }.get(x, x),
)

# Use a sample for performance (full dataset is large)
sample = df.dropna(subset=[x_var, y_var]).sample(n=min(2000, len(df)), random_state=42)

fig2 = px.scatter(
    sample,
    x=x_var,
    y=y_var,
    color=color_var,
    opacity=0.5,
    title=f"{y_var.replace('_', ' ').title()} vs {x_var.replace('_', ' ').title()}",
    labels={
        "points": "Championship Points",
        "grid": "Grid Position",
        "laps": "Laps Completed",
        "position_num": "Finishing Position",
        "name_constructor": "Constructor",
        "nationality": "Nationality",
        "year": "Season",
    },
    color_discrete_sequence=px.colors.qualitative.Plotly,
)
fig2.update_layout(height=500, margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig2, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "DATS 6401 · Week 1 Homework · Soumay Patidar · "
    "Data: Ergast F1 Database (1950–2024)"
)


# DATS 6401: Week 1 Homework
## Formula 1 Data Explorer (Streamlit App)

**Author:** Soumay Patidar  
**Course:** Visualization of Complex Data (DATS 6401)  
**Dataset:** Formula 1 World Championship (1950–2024)

---

## What This App Does

- Loads and merges four core F1 CSV files (results, races, drivers, constructors)
- Shows a scrollable data preview with column-type breakdown
- Renders a labeled Plotly bar chart of the **Top 10 F1 Drivers by Race Wins**
- Includes a text panel describing the dataset and the chart
- **Bonus:** An interactive scatter-plot explorer with dropdown selectors

---

## Setup & Run (Local)

### 1. Create a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**.

---

## Project Structure

```
week1_hw/
├── app.py              ← Streamlit application
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── data/
    ├── races.csv
    ├── results.csv
    ├── drivers.csv
    ├── constructors.csv
    └── ... (other F1 CSVs)
```


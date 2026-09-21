# Assignment 2 - Real-Time Data Processing with Pandas and NumPy

## AITU Smart Classroom Energy Stream

This project processes the supplied synthetic classroom sensor stream using Pandas and NumPy. It covers data cleaning, 3-minute rolling statistics, feature engineering, statistical analysis, visualization, testing, and reproducible evidence.

## Files

- `main.py` - main processing workflow
- `classroom_data.csv` - supplied sensor data
- `cleaned_classroom_data.csv` - cleaned source fields
- `processed_classroom_data.csv` - cleaned data with rolling statistics and engineered features
- `test_assignment2.py` - automated tests
- `completed_tables.md` - completed assignment tables
- `plots/` - required plots
- `evidence/` - execution output and calculation evidence
- `Assignment2_Technical_Report_Amankos_Danial_BDA_2405.pdf` - technical report

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The script creates the cleaned and processed datasets and both required plots.

## Tests

```bash
python -m pytest -q
```

## Main processing decisions

- Temperature uses linear interpolation.
- CO2 uses linear interpolation.
- Occupancy uses forward fill.
- Rolling statistics use a 3-row window and start only when three readings are available.
- Occupancy density uses the assignment capacity of 40.
- Comfort is true when CO2 is at most 1000 ppm and temperature is from 20 C to 24 C inclusive.

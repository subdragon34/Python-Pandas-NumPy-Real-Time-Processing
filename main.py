from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA = BASE_DIR / "classroom_data.csv"
CLEANED_DATA = BASE_DIR / "cleaned_classroom_data.csv"
PROCESSED_DATA = BASE_DIR / "processed_classroom_data.csv"
PLOTS_DIR = BASE_DIR / "plots"


def load_data(path=RAW_DATA):
    df = pd.read_csv(path)
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M")
    return df


def missing_value_summary(df):
    return df.isna().sum()


def clean_data(df):
    cleaned = df.copy()
    cleaned["Temp_C"] = cleaned["Temp_C"].interpolate(method="linear")
    cleaned["CO2_ppm"] = cleaned["CO2_ppm"].interpolate(method="linear")
    cleaned["Occupancy"] = cleaned["Occupancy"].ffill().astype(int)
    return cleaned


def validate_cleaned_data(df):
    sensor_cols = ["Temp_C", "CO2_ppm", "Occupancy", "Power_kW"]

    if df[sensor_cols].isna().any().any():
        raise ValueError("Cleaned data still contains missing sensor values")
    if (df["Occupancy"] < 0).any():
        raise ValueError("Occupancy cannot be negative")
    if (df["Power_kW"] < 0).any():
        raise ValueError("Power_kW cannot be negative")

    return True


def add_rolling_statistics(df):
    result = df.copy()

    for column in ["Temp_C", "CO2_ppm", "Power_kW"]:
        result[f"{column}_roll3"] = (
            result[column]
            .rolling(window=3, min_periods=3)
            .mean()
        )

    return result


def add_features(df):
    result = df.copy()

    result["occupancy_density"] = result["Occupancy"] / 40
    result["energy_per_student"] = result["Power_kW"] / result["Occupancy"]
    result["comfort_flag"] = (
        (result["CO2_ppm"] <= 1000)
        & result["Temp_C"].between(20, 24, inclusive="both")
    )

    return result


def calculate_statistics(df):
    max_power_index = df["Power_kW"].idxmax()

    return {
        "temp_mean": float(df["Temp_C"].mean()),
        "temp_median": float(df["Temp_C"].median()),
        "temp_min": float(df["Temp_C"].min()),
        "temp_max": float(df["Temp_C"].max()),
        "co2_mean": float(df["CO2_ppm"].mean()),
        "co2_max": float(df["CO2_ppm"].max()),
        "highest_power_time": df.loc[max_power_index, "Time"].strftime("%H:%M"),
        "highest_power_kw": float(df.loc[max_power_index, "Power_kW"]),
        "occupancy_power_correlation": float(
            df["Occupancy"].corr(df["Power_kW"])
        ),
    }


def save_dataset(df, path):
    output = df.copy()
    output["Time"] = output["Time"].dt.strftime("%H:%M")
    output.to_csv(path, index=False)


def create_plots(df, output_dir=PLOTS_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(
        df["Time"],
        df["Temp_C_roll3"],
        marker="o",
        label="Temperature rolling mean",
    )
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Temperature (C)")
    ax1.tick_params(axis="x", rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(
        df["Time"],
        df["CO2_ppm_roll3"],
        marker="s",
        label="CO2 rolling mean",
    )
    ax2.set_ylabel("CO2 (ppm)")

    ax1.set_title("3-minute Rolling Temperature and CO2")
    fig.tight_layout()
    fig.savefig(output_dir / "rolling_temperature_co2.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["Occupancy"], df["Power_kW"])

    slope, intercept = np.polyfit(df["Occupancy"], df["Power_kW"], 1)
    x_line = np.array([df["Occupancy"].min(), df["Occupancy"].max()])
    ax.plot(x_line, slope * x_line + intercept)

    ax.set_title("Occupancy vs Power Consumption")
    ax.set_xlabel("Occupancy")
    ax.set_ylabel("Power (kW)")
    fig.tight_layout()
    fig.savefig(output_dir / "occupancy_vs_power.png", dpi=180)
    plt.close(fig)


def display_time(df):
    result = df.copy()
    result["Time"] = result["Time"].dt.strftime("%H:%M")
    return result


def main():
    df = load_data()

    print("Missing values before cleaning")
    print(missing_value_summary(df).to_string())

    cleaned = clean_data(df)
    validate_cleaned_data(cleaned)
    save_dataset(cleaned, CLEANED_DATA)

    print("\nCleaned missing-value rows")
    print(
        display_time(cleaned).loc[
            [2, 4, 7],
            ["Time", "Temp_C", "CO2_ppm", "Occupancy"],
        ].to_string(index=False)
    )

    processed = add_rolling_statistics(cleaned)
    processed = add_features(processed)
    save_dataset(processed, PROCESSED_DATA)

    print("\n3-minute rolling statistics")
    print(
        display_time(processed).loc[
            2:6,
            ["Time", "Temp_C_roll3", "CO2_ppm_roll3", "Power_kW_roll3"],
        ].round(3).to_string(index=False)
    )

    print("\nFeature engineering results")
    print(
        display_time(processed).loc[
            [3, 6, 9, 11],
            ["Time", "occupancy_density", "energy_per_student", "comfort_flag"],
        ].round(4).to_string(index=False)
    )

    statistics = calculate_statistics(processed)

    print("\nStatistical analysis")
    print(f'Temperature mean: {statistics["temp_mean"]:.4f}')
    print(f'Temperature median: {statistics["temp_median"]:.2f}')
    print(f'Temperature minimum: {statistics["temp_min"]:.1f}')
    print(f'Temperature maximum: {statistics["temp_max"]:.1f}')
    print(f'CO2 mean: {statistics["co2_mean"]:.4f}')
    print(f'CO2 maximum: {statistics["co2_max"]:.0f}')
    print(
        f'Highest power: {statistics["highest_power_time"]} '
        f'({statistics["highest_power_kw"]:.1f} kW)'
    )
    print(
        "Occupancy-power correlation: "
        f'{statistics["occupancy_power_correlation"]:.4f}'
    )

    create_plots(processed)

    print("\nOperational interpretation")
    print(
        "1. Occupancy and power rise closely together in this synthetic stream. "
        "Occupancy-aware controls could help avoid unnecessary energy demand."
    )
    print(
        "2. Rolling temperature and CO2 rise through the period. "
        "The trend can be used as an early signal to review ventilation "
        "or room-control settings."
    )


if __name__ == "__main__":
    main()

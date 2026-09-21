import numpy as np

from main import (
    add_features,
    add_rolling_statistics,
    calculate_statistics,
    clean_data,
    load_data,
    validate_cleaned_data,
)


def prepared_data():
    df = clean_data(load_data())
    df = add_rolling_statistics(df)
    return add_features(df)


def test_required_missing_values_are_cleaned():
    df = clean_data(load_data())

    assert df.loc[2, "Temp_C"] == 21.9
    assert df.loc[4, "CO2_ppm"] == 750
    assert df.loc[7, "Occupancy"] == 29
    assert validate_cleaned_data(df) is True


def test_rolling_statistics_at_1004():
    df = prepared_data()

    assert np.isclose(df.loc[4, "Temp_C_roll3"], 22.1)
    assert np.isclose(df.loc[4, "CO2_ppm_roll3"], 720.0)
    assert np.isclose(df.loc[4, "Power_kW_roll3"], 3.7666666667)


def test_feature_engineering_at_1009():
    df = prepared_data()

    assert np.isclose(df.loc[9, "occupancy_density"], 0.825)
    assert np.isclose(df.loc[9, "energy_per_student"], 5.1 / 33)
    assert bool(df.loc[9, "comfort_flag"]) is True


def test_statistical_results():
    df = prepared_data()
    result = calculate_statistics(df)

    assert np.isclose(result["temp_mean"], 22.4833333333)
    assert np.isclose(result["temp_median"], 22.55)
    assert result["temp_min"] == 21.5
    assert result["temp_max"] == 23.3
    assert np.isclose(result["co2_mean"], 789.1666666667)
    assert result["co2_max"] == 950
    assert result["highest_power_time"] == "10:11"
    assert result["highest_power_kw"] == 5.7


def test_occupancy_power_correlation_is_strong_positive():
    df = prepared_data()
    result = calculate_statistics(df)

    assert result["occupancy_power_correlation"] > 0.99


def test_comfort_flag_boundary():
    df = prepared_data().copy()
    df.loc[0, "Temp_C"] = 24.0
    df.loc[0, "CO2_ppm"] = 1000

    checked = add_features(df)

    assert bool(checked.loc[0, "comfort_flag"]) is True

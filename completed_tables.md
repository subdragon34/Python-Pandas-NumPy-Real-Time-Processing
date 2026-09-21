# Completed Assignment Tables

## Part A - Data Quality

| Variable | Missing value | Method | Value after cleaning | Justification |
|---|---|---|---:|---|
| Temp_C | 10:02 | Linear interpolation | 21.9 | The missing reading is between 21.7 and 22.1, so interpolation follows the local trend. |
| CO2_ppm | 10:04 | Linear interpolation | 750 | The missing reading is between 720 and 780 ppm, giving 750 ppm. |
| Occupancy | 10:07 | Forward fill | 29 | The latest known occupancy is carried forward until a new sensor reading appears. |

## Part B - 3-Minute Rolling Means

| Time | Temp rolling mean | CO2 rolling mean | Power rolling mean |
|---|---:|---:|---:|
| 10:02 | 21.700 | 653.333 | 3.367 |
| 10:03 | 21.900 | 686.667 | 3.567 |
| 10:04 | 22.100 | 720.000 | 3.767 |
| 10:05 | 22.300 | 750.000 | 4.000 |
| 10:06 | 22.467 | 780.000 | 4.200 |

## Part C - Feature Engineering

| Time | Occupancy density | Energy/student | Comfort flag |
|---|---:|---:|---|
| 10:03 | 0.600 | 0.1583 | True |
| 10:06 | 0.725 | 0.1517 | True |
| 10:09 | 0.825 | 0.1545 | True |
| 10:11 | 0.925 | 0.1541 | True |

Formulas:

- `occupancy_density = Occupancy / 40`
- `energy_per_student = Power_kW / Occupancy`
- `comfort_flag = CO2_ppm <= 1000 and 20 <= Temp_C <= 24`

## Part D - Statistical Analysis

| Metric | Result |
|---|---:|
| Temperature mean | 22.4833 C |
| Temperature median | 22.55 C |
| Temperature minimum | 21.5 C |
| Temperature maximum | 23.3 C |
| CO2 mean | 789.1667 ppm |
| CO2 maximum | 950 ppm |
| Highest power time | 10:11 |
| Highest power consumption | 5.7 kW |
| Occupancy-power correlation | 0.9946 |

Interpretation:

The correlation is very strong and positive in this synthetic sample. Higher occupancy is associated with higher electricity use. It does not prove that occupancy alone causes the increase, but it supports occupancy-aware monitoring and control.

## Part E - Engineering Interpretation

1. Occupancy and power rise together during the observed period. Facility staff could use occupancy-aware schedules or controls to reduce energy use when a room is lightly occupied or empty.
2. Rolling temperature and CO2 increase through the class period. Monitoring the rolling trend can provide an early signal to review ventilation or room-control settings before comfort conditions worsen.

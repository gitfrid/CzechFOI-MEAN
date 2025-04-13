import pandas as pd

# Load the original CSV file
df = pd.read_csv(r"C:\CzechFOI-MEAN\TERRA\PVT_NUM_D.csv")

# Drop the "DAY" column and store separately
days = df["DAY"]
age_columns = df.columns[1:]  # from age 0 to 113

# Initialize dictionary to hold the result
first_nonzero_day = {}

# Iterate over each age column
for age in age_columns:
    nonzero_days = df[df[age] > 0]["DAY"]
    first_day = nonzero_days.iloc[0] if not nonzero_days.empty else 0
    first_nonzero_day[age] = first_day

# Convert the result into a DataFrame (single row)
result_df = pd.DataFrame([first_nonzero_day])

# Save to CSV
result_df.to_csv(r"C:\CzechFOI-MEAN\TERRA\first_nonzero_day_per_age.csv", index=False)

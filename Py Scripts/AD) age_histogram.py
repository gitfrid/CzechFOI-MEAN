import pandas as pd
import numpy as np
import plotly.graph_objects as go

# This script processes data from pivot CSV files located in the TERRA folder, 
# which were generated from a Czech Freedom of Information request (Vesely_106_202403141131.csv). 
# The pivot CSV files were created using the DB Browser for SQLite.
# The file "first_nonzero_day_per_age.csv" was created by using "AD) FirstNonZeroDoseForAge.py"

# Load death data
death_df = pd.read_csv(r"C:\CzechFOI-MEAN\TERRA\PVT_NUM_D.csv")

# Load first nonzero day per age
first_dose_day = pd.read_csv(r"C:\CzechFOI-MEAN\TERRA\first_nonzero_day_per_age.csv")

# day range before and after vax start (to calculate mean and histogram distribution) 
day_range = 31

# Convert to series with age as index
first_dose_day_series = first_dose_day.iloc[0]
first_dose_day_series.index = first_dose_day_series.index.astype(int)

# Ensure death_df is indexed by DAY
death_df = death_df.set_index("DAY")

# Get list of all ages (assumes columns 0–113)
ages = death_df.columns.astype(int)

# Lists to collect death age data
ages_before = []
ages_after = []

# For each age, collect death data
for age in ages:
    day = first_dose_day_series[age]

    # Define window range
    start_before = max(0, day - day_range)
    end_before = day - 1
    start_after = day
    end_after = min(death_df.index.max(), day + (day_range - 1))

    # Get deaths before and after
    deaths_before = death_df.loc[start_before:end_before, str(age)]
    deaths_after = death_df.loc[start_after:end_after, str(age)]

    # Expand death counts into age lists
    ages_before.extend([age] * int(deaths_before.sum()))
    ages_after.extend([age] * int(deaths_after.sum()))

# Calculate mean death ages
mean_age_before = np.mean(ages_before) if ages_before else np.nan
mean_age_after = np.mean(ages_after) if ages_after else np.nan

# Plot using Plotly
fig = go.Figure()

fig.add_trace(go.Histogram(
    x=ages_before,
    name=f"Deaths {day_range} Days Before",
    opacity=0.7,
    marker_color='blue'
))

fig.add_trace(go.Histogram(
    x=ages_after,
    name=f"Deaths {day_range} Days After",
    opacity=0.7,
    marker_color='red'
))

# Add vertical lines for mean ages
fig.add_vline(x=mean_age_before, line=dict(color='blue', width=2, dash='dash'), name="mean age before")
fig.add_vline(x=mean_age_after, line=dict(color='red', width=2, dash='dash'), name="mean age after")

# Annotate mean lines
fig.add_annotation(x=mean_age_before, y=0, text=f"Average age at death Before: {mean_age_before:.1f}", showarrow=True,
                   arrowhead=1, ax=0, ay=-40, font=dict(color="blue"))
fig.add_annotation(x=mean_age_after, y=0, text=f"Average age at death After: {mean_age_after:.1f}", showarrow=True,
                   arrowhead=1, ax=0, ay=-60, font=dict(color="red"))

fig.update_layout(
    title=f"Age Distribution of Deaths Within {day_range} Days Before versus After the Start of Vac (First Dose) for Each Age Group",
    xaxis_title="Age",
    yaxis_title="Death Count",
    barmode='overlay',
    template="plotly_white"
)

# Save plot as HTML
fig.write_html(fr"C:\CzechFOI-MEAN\Plot Results\AD) age_histogram\AD) age_histogram_{day_range}_days.html")
print(fr"Histogram saved as C:\CzechFOI-MEAN\Plot Results\AD) age_histogram\AD) age_histogram_{day_range}_days.html")


# This script processes data from pivot CSV files located in the TERRA folder, 
# which were generated from a Czech Freedom of Information request (Vesely_106_202403141131.csv). 
# The pivot CSV files were created using the DB Browser for SQLite.

import pandas as pd
import plotly.graph_objects as go

# Load death data
death_df = pd.read_csv(r"C:\CzechFOI-MEAN\TERRA\PVT_NUM_D.csv")
death_df = death_df.set_index("DAY")
death_df.columns = death_df.columns.astype(int)

# Load vaccine dose data
dose_df = pd.read_csv(r"C:\CzechFOI-MEAN\TERRA\PVT_NUM_VDA.csv")
dose_df = dose_df.set_index("DAY")
dose_df.columns = dose_df.columns.astype(int)

# 1. Total deaths per day
daily_total_deaths = death_df.sum(axis=1)

# 2. Age-weighted deaths per day
daily_weighted_sum = (death_df * death_df.columns).sum(axis=1)

# 3. Total doses per day
daily_total_doses = dose_df.sum(axis=1)

# 4. Mean age of death per day
mean_age_of_death = daily_weighted_sum / daily_total_deaths

# Rolling means (7-day)
rolling_weighted_deaths = daily_weighted_sum.rolling(window=7, min_periods=1).mean()
rolling_total_doses = daily_total_doses.rolling(window=7, min_periods=1).mean()
rolling_mean_age = mean_age_of_death.rolling(window=7, min_periods=1).mean()

# Determine the first day when total vaccine doses exceed 100
first_vaccine_day = daily_total_doses[daily_total_doses > 100].index.min()

# Create plot
fig = go.Figure()

# Raw data
fig.add_trace(go.Scatter(
    x=daily_total_deaths.index,
    y=daily_total_deaths.values,
    mode='lines',
    name='Total deaths per day',
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=daily_weighted_sum.index,
    y=daily_weighted_sum.values,
    mode='lines',
    name='Age-weighted deaths per day',
    line=dict(color='red')
))

fig.add_trace(go.Scatter(
    x=daily_total_doses.index,
    y=daily_total_doses.values,
    mode='lines',
    name='Total vaccine doses per day',
    line=dict(color='green')
))

# Mean age of death (right Y-axis)
fig.add_trace(go.Scatter(
    x=mean_age_of_death.index,
    y=mean_age_of_death.values,
    mode='lines',
    name='Mean age of death',
    line=dict(color='grey'),
    yaxis='y2'
))

# Rolling means
fig.add_trace(go.Scatter(
    x=rolling_weighted_deaths.index,
    y=rolling_weighted_deaths.values,
    mode='lines',
    name='Weighted deaths (7-day avg)',
    line=dict(color='red', width=0.7)
))

fig.add_trace(go.Scatter(
    x=rolling_total_doses.index,
    y=rolling_total_doses.values,
    mode='lines',
    name='Vac doses (7-day avg)',
    line=dict(color='green', width=0.7)
))

# Rolling mean age of death
fig.add_trace(go.Scatter(
    x=rolling_mean_age.index,
    y=rolling_mean_age.values,
    mode='lines',
    name='Mean age of death (7-day avg)',
    line=dict(color='black', width=0.7),
    yaxis='y2'
))

# Layout with secondary y-axis and vertical marker
fig.update_layout(
    title='Daily Deaths, Age-Weighted Deaths, Vaccine Doses, and Mean Age of Death (7-Day Averages)',
    xaxis_title='Day',
    yaxis=dict(
        title='Count / Weighted Sum',
    ),
    yaxis2=dict(
        title='Mean Age of Death',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend_title='Metric',
    template='plotly_white',
    shapes=[
        dict(
            type='line',
            x0=first_vaccine_day,
            x1=first_vaccine_day,
            y0=0,
            y1=1,
            yref='paper',
            line=dict(color='purple', width=2, dash='dot')
        )
    ],
    annotations=[
        dict(
            x=first_vaccine_day,
            y=1.02,
            xref='x',
            yref='paper',
            text='Start of Vac (>100 doses)',
            showarrow=False,
            font=dict(color='purple'),
            align='center'
        )
    ]
)

# Save plot
fig.write_html(r"C:\CzechFOI-MEAN\Plot Results\AC) age_mean\AC) age_mean_with_doses.html")
print(r"Plot saved as C:\CzechFOI-MEAN\Plot Results\AC) age_mean\AC) age_mean_with_doses.html")

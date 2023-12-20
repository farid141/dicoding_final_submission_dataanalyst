import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import seaborn as sns
import streamlit as st

# Data Wrangling
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Data Cleaning
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# set min max for filter
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()


def create_month_trend_df(df: DataFrame):
    monthly_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_df.index = monthly_df.index.strftime('%Y-%m')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={'dteday': 'month',
                      'cnt': 'total_rent'}, inplace=True)
    return monthly_df


def create_holiday_rent_df(df: DataFrame):
    holiday_rent_df = df.groupby(by="holiday").agg({
        "cnt": ["max", "mean", "min", "sum"]
    }).reset_index()
    return holiday_rent_df


def create_working_day_rent_df(df: DataFrame):
    working_day_rent_df = df.groupby(by="workingday").agg({
        "cnt": ["max", "mean", "min", "sum"]
    }).reset_index()
    return working_day_rent_df


def create_working_day_weather_df(df: DataFrame):
    working_day_weather_df = df.groupby(by=["workingday", "weathersit"]).agg({
        "cnt": ["sum"]
    }).reset_index()
    return working_day_weather_df


def create_hour_mean_trend_df(df: DataFrame):
    hour_mean_trend_df = df.groupby(by=["workingday", "hr"]).agg({
        "cnt": ["mean"]
    }).reset_index()
    return hour_mean_trend_df


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

tmp_day_df = day_df[(day_df["dteday"] >= str(start_date)) &
                    (day_df["dteday"] <= str(end_date))]
tmp_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) &
                      (hour_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe
month_trend_df = create_month_trend_df(tmp_day_df)
holiday_rent_df = create_holiday_rent_df(tmp_day_df)
working_day_rent_df = create_working_day_rent_df(tmp_day_df)
working_day_weather_df = create_working_day_weather_df(tmp_day_df)
hour_mean_trend_df = create_hour_mean_trend_df(tmp_hour_df)

print(month_trend_df)
print(holiday_rent_df)
print(working_day_rent_df)
print(working_day_weather_df)
print(hour_mean_trend_df)


# plot number of daily orders (2021)
st.header('Bike Sharing Analysis :sparkles:')
st.subheader('By: Farid Nubaili')
st.subheader('Daily Orders')

# registered dan casual
col1, col2 = st.columns(2)

with col1:
    casual = month_trend_df["casual"].sum()
    st.metric("Casual", value=casual)

with col2:
    registered = month_trend_df["registered"].sum()
    st.metric("Registered", value=registered)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_trend_df["month"],
    month_trend_df["total_rent"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)

st.pyplot(fig)

# Product Rent holiday
st.subheader("Rent on Holiday")

# holiday
col1, col2 = st.columns(2)

with col1:
    no_holiday = holiday_rent_df[holiday_rent_df["holiday"] == 0]["cnt"]["sum"]
    st.metric("No holiday", value=no_holiday)

with col2:
    holiday = holiday_rent_df[holiday_rent_df["holiday"] == 1]["cnt"]["sum"]
    st.metric("Holiday", value=holiday)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(
    data=holiday_rent_df[holiday_rent_df['holiday'] == 0]["cnt"].drop(columns="sum", axis=1), ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel("Number of Rent", fontsize=30)
ax[0].set_title("Rent on No Holiday", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(
    data=holiday_rent_df[holiday_rent_df['holiday'] == 1]["cnt"].drop(columns="sum", axis=1), ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel("Number of Rent", fontsize=30)
ax[1].set_title("Rent on Holiday", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)

# Product Rent holiday
st.subheader("Rent on Workingday")
# workingday
col1, col2 = st.columns(2)

with col1:
    weekend = working_day_rent_df[working_day_rent_df["workingday"]
                                  == 0]["cnt"]["sum"]
    st.metric("Weekend", value=weekend)

with col2:
    workingday = working_day_rent_df[working_day_rent_df["workingday"]
                                     == 1]["cnt"]["sum"]
    st.metric("Workingday", value=workingday)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(
    data=working_day_rent_df[working_day_rent_df['workingday'] == 0]["cnt"].drop(columns="sum", axis=1), ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel("Number of Rent", fontsize=30)
ax[0].set_title("Rent on Weekend", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(
    data=working_day_rent_df[working_day_rent_df['workingday'] == 1]["cnt"].drop(columns="sum", axis=1), ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel("Number of Rent", fontsize=30)
ax[1].set_title("Rent on Workingday", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)


# Product Rent holiday
st.subheader("Rent on Workingday and Various Weather")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(
    x=working_day_weather_df[working_day_weather_df['workingday'] == 0]["weathersit"], y=working_day_weather_df[working_day_weather_df['workingday'] == 0]["cnt"]["sum"], ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel("Number of Rent", fontsize=30)
ax[0].set_title("Rent on Weekend", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(
    x=working_day_weather_df[working_day_weather_df['workingday'] == 1]["weathersit"], y=working_day_weather_df[working_day_weather_df['workingday'] == 1]["cnt"]["sum"], ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel("Number of Rent", fontsize=30)
ax[1].set_title("Rent on Workingday", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)

# hour mean rent
st.subheader('Hourly Rent')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hour_mean_trend_df[hour_mean_trend_df['workingday'] == 0]["hr"],
    hour_mean_trend_df[hour_mean_trend_df['workingday'] == 0]["cnt"]["mean"],
    marker='o',
    linewidth=2,
    color="#90CAF9",
    label="Working Day = 0"
)


# Plot line for workingday=1
ax.plot(
    hour_mean_trend_df[hour_mean_trend_df['workingday'] == 1]["hr"],
    hour_mean_trend_df[hour_mean_trend_df['workingday'] == 1]["cnt"]["mean"],
    marker='o',
    linewidth=2,
    color="#FFA726",  # Choose a different color
    label="Working Day = 1"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
# Set x-axis ticks to all unique hours
plt.xticks(hour_mean_trend_df["hr"].unique())
plt.xticks(rotation=45)

# Add a legend to the plot
ax.legend(loc='best', fontsize=15)
st.pyplot(fig)

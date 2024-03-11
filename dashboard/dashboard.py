import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# load data 
day_df = pd.read_csv("../data/Bike_Sharing_daily.csv")
hour_df = pd.read_csv("../data/Bike_Sharing_hourly.csv")

st.set_page_config(page_title="Bike Share Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

# Functions
def create_byseason_df(df):
    byseason_df = df.groupby(by='season').agg({
    'cnt': 'sum'})
    return byseason_df

def create_monthly_counts_df(df):
    monthly_counts_df = df.groupby(by=['mnth','yr']).agg({
    'cnt': 'sum'
    }).reset_index()
    return monthly_counts_df

def create_byweather_df(df):
    byweather_df = df.groupby(by='weathersit').agg({
    'cnt': 'sum'
    })
    return byweather_df

def create_daily_share_df(df):
    rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return rent_df

def create_daily_casual_df(df):
    casual_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_rent_df

def create_daily_registered_df(df):
    registered_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_rent_df

def create_byholiday_df(df):
    byholiday_df = df.groupby(by='holiday').agg({
    'cnt': ['mean']
    }).reset_index()
    return byholiday_df

def create_byweekday_df(df):
    byweekday_df = df.groupby(by='weekday').agg({
    'cnt': ['mean']
    }).reset_index()
    return byweekday_df

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by='workingday').agg({
    'cnt': ['mean']
    }).reset_index()
    return byworkingday_df

# Date Column
datetime_columns = ['dteday']
day_df.sort_values(by='dteday', inplace=True)
day_df.reset_index(inplace=True)   

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])
    day_df[column] = pd.to_datetime(day_df[column])

min_date_days = day_df['dteday'].min()
max_date_days = day_df['dteday'].max()

min_date_hour = day_df['dteday'].min()
max_date_hour = hour_df['dteday'].max()

# Sidebar
st.sidebar.markdown("Luthfia Rahmi Setyorini")

with st.sidebar:
    # Add Logo
    st.image("https://banner2.cleanpng.com/20190715/asf/kisspng-bicycle-shop-road-bicycle-cycling-mountain-bike-vector-bike-picture-format-transparent-amp-png-c-5d2d2a3dd2c733.3976117315632410218634.jpg")
    # Retrieve start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_day = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]
main_df_hour = hour_df[(hour_df['dteday'] >= str(start_date)) & (hour_df['dteday'] <= str(end_date))]

# Dataframe
monthly_counts_df = create_monthly_counts_df(main_df_day)
byweather_df = create_byweather_df(main_df_day)
byseason_df = create_byseason_df(main_df_day)
rent_df = create_daily_share_df(main_df_day)
casual_rent_df = create_daily_casual_df(main_df_day)
registered_rent_df = create_daily_registered_df(main_df_day)
byholiday_df = create_byholiday_df(main_df_day)
byweekday_df = create_byweekday_df(main_df_day)
byworkingday_df = create_byworkingday_df(main_df_day)

# Dashboard
st.header('Bike Sharing Dashboard')
col1, col2 = st.columns(2)

with col1:
    total_df = rent_df['cnt'].sum()
    st.metric('Total Peminjam', value= total_df.astype(int))

# Visualization
# To answer question 1
st.subheader('Seasonal Rentals')

fig, ax = plt.subplots(figsize=(12, 9))

colors=["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x= byseason_df.index,
    y= byseason_df['cnt'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(byseason_df['cnt']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# To answer question 2
st.subheader('Working day vs Holiday Rentals')

# Create subplots
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))  # Adjust figsize as needed

# Plotting
sns.barplot(x='workingday', y='cnt', hue='workingday', data=day_df, ax=axes)
axes.set_xlabel('Day Type')
axes.set_ylabel('Number of Bike Renters')

plt.tight_layout()
st.pyplot(fig)
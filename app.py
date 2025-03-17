# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 18:07:09 2025

@author: carba
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load the data ---
@st.cache_data
def load_data():
    file_path = "Center for Nonprofit Webinar Information.xlsx"
    df = pd.read_excel(file_path)
    df['Webinar Date'] = pd.to_datetime(df['Webinar Date'])
    df['Webinar_Year_Month'] = df['Webinar Date'].dt.to_period('M')
    return df

df = load_data()

# --- Sidebar Filter for Date Selection ---
st.sidebar.header("Filter Options")

# Ensure the calendar allows selection within the data range
date_range = st.sidebar.date_input(
    "Select Date Range",
    [],
    key="date_range",
    min_value=df["Webinar Date"].min(),
    max_value=df["Webinar Date"].max()
)

# Apply date filtering
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    
    # Filter data based on selected date range
    df_filtered = df[(df['Webinar Date'] >= start_date) & (df['Webinar Date'] <= end_date)]
else:
    df_filtered = df  # Show all data if no range is selected

# --- Prepare Data for Visualization ---
webinar_counts = df_filtered.groupby('Webinar_Year_Month')['Webinar Attendees'].sum().reset_index()
webinar_counts['Webinar_Year_Month'] = webinar_counts['Webinar_Year_Month'].astype(str)

# --- Streamlit Page Title ---
st.title("📊 Webinars Dashboard")

# --- Bar Chart: Webinar Attendees Over Time ---
st.subheader("📅 Webinar Attendees by Year-Month")
fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    x=webinar_counts['Webinar_Year_Month'],
    y=webinar_counts['Webinar Attendees'],
    color='red',
    ax=ax
)

# Fix the tick label issue
ax.set_xticks(range(len(webinar_counts)))  # Set the tick positions
ax.set_xticklabels(webinar_counts['Webinar_Year_Month'], rotation=45, ha="right")

ax.set_xlabel("Webinar Year-Month")
ax.set_ylabel("Total Webinar Attendees")
ax.set_title("Webinar Attendees Count by Year-Month")

st.pyplot(fig)

# --- Data Table: Webinar Information ---
st.subheader("📋 Webinar Data Table")
st.dataframe(df_filtered[['Webinar Date', 'Webinar Topic', 'Webinar Attendees']])

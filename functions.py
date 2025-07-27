import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def prepareGraph(df):
    # Ensure correct types
    df['accident_severity'] = df['accident_severity'].astype('category')
    df['hour'] = pd.to_numeric(df['hour'], errors='coerce')
    df['weekday'] = pd.Categorical(df['weekday'], categories=[
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

    sns.set(style='whitegrid')
    plt.rcParams['figure.figsize'] = (6, 4)  # Adjust size to fit in columns

    ### Row 1 - Charts 1, 2, 3
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Accident Severity Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='accident_severity_label', palette='Set2', ax=ax)
        ax.set_title("Severity Distribution")
        st.pyplot(fig)

    with col2:
        st.subheader("Accidents by Hour of Day")
        fig, ax = plt.subplots()
        sns.histplot(df['hour'].dropna(), bins=24, kde=False, color='orange', ax=ax)
        ax.set_title("By Hour of Day")
        ax.set_xticks(range(0, 24))
        st.pyplot(fig)

    with col3:
        st.subheader("Accidents by Day of Week")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='weekday', order=[
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], palette='Blues_d', ax=ax)
        ax.set_title("By Day of Week")
        st.pyplot(fig)

    ### Row 2 - Charts 4, 5, 6
    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("Light Conditions")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='light_conditions', order=df['light_conditions'].value_counts().index, ax=ax)
        ax.set_title("Light Conditions")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    with col5:
        st.subheader("Weather Conditions")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='weather_conditions', order=df['weather_conditions'].value_counts().index, ax=ax)
        ax.set_title("Weather Conditions")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    with col6:
        st.subheader("Speed vs Severity")
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x='accident_severity_label', y='speed_limit', palette='coolwarm', ax=ax)
        ax.set_title("Speed Limit vs Severity")
        st.pyplot(fig)

    ### Row 3 - Charts 7, 8
    col7, col8 = st.columns(2)

    with col7:
        st.subheader("Urban vs Rural Accidents")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='urban_or_rural_area', hue='accident_severity_label', palette='husl', ax=ax)
        ax.set_title("Urban vs Rural")
        ax.legend(title='Severity')
        st.pyplot(fig)

    with col8:
        st.subheader("Accidents by Month")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='month', palette='viridis', ax=ax)
        ax.set_title("Monthly Distribution")
        st.pyplot(fig)
def cleanData(df):
           
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace('[^a-z0-9_]', '', regex=True)

    # Handle Date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.day_name()

    # Handle Time
    df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce')
    df['hour'] = df['time'].dt.hour

    # Weekend or not
    df['is_weekend'] = df['weekday'].isin(['Saturday', 'Sunday'])

    # Basic cleanup (if needed)
    df.dropna(subset=['date', 'time'], inplace=True)

    # Convert severity to labels (Optional)
    severity_map = {1: 'Fatal', 2: 'Serious', 3: 'Slight'}
    df['accident_severity_label'] = df['accident_severity'].map(severity_map)

    # Save summary of missing values to a file
    missing_values = df.isnull().sum().sort_values(ascending=False)
    missing_values.to_csv("missing_values_summary.csv")

    # Save preview to a new CSV file
    df_preview = df[['date', 'time', 'weekday', 'hour', 'accident_severity', 'accident_severity_label']]
    df_preview.head().to_csv("accident_preview.csv", index=False)

    # Save the full cleaned data to a file
    df.to_csv("AccidentsCleaned.csv", index=False)
    
    return df

def remap_columns(df, required_map):
    new_columns = {}
    for standard_col, possible_names in required_map.items():
        for name in possible_names:
            if name.lower() in df.columns:
                new_columns[name] = standard_col
                break
    df = df.rename(columns=new_columns)
    return df

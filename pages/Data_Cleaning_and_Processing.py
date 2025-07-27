import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functions import cleanData, prepareGraph, remap_columns

# Streamlit config
st.set_page_config(page_title="Accident Data Dashboard", layout="wide")
st.title("🚦 Road Accident Data Visualizations")

# Optional CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # If no style file, continue without it

local_css("style.css")

# Flexible accident columns
REQUIRED_COLUMNS = {
    'date': ['date', 'accident_date'],
    'time': ['time', 'accident_time'],
    'accident_severity': ['accident_severity', 'severity'],
    'light_conditions': ['light_conditions', 'lighting'],
    'weather_conditions': ['weather_conditions', 'weather'],
    'urban_or_rural_area': ['urban_or_rural_area', 'area_type'],
    'speed_limit': ['speed_limit', 'speed'],
    'accident_index': ['accident_index', 'id'],
    'number_of_vehicles': ['number_of_vehicles'],
    'number_of_casualties': ['number_of_casualties'],
    'road_type': ['road_type'],
}

# File Upload
uploaded_file = st.file_uploader("📤 Upload any CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.lower()

        st.subheader("📄 Data Preview")
        st.dataframe(df.head(50))
        
        # st.subheader("📄 Data Preview with Search")

        # search_input = st.text_input("🔍 Search rows (case-insensitive, applies to all columns):")

        # # Optional row count selector
        # max_rows = st.slider("Max rows to display", min_value=10, max_value=500, value=100, step=10)

        # if search_input:
        #     filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_input, case=False).any(), axis=1)]
        #     st.write(f"Showing {min(len(filtered_df), max_rows)} of {len(filtered_df)} matching rows:")
        #     st.dataframe(filtered_df.head(max_rows))
        # else:
        #     st.write(f"Showing first {max_rows} rows of full dataset ({len(df)} rows total):")
        #     st.dataframe(df.head(max_rows))


        st.subheader("🔍 Column Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Descriptive Statistics**")
            st.dataframe(df.describe(include='all'))

        with col2:
            st.markdown("**🧾 Data Types**")
            st.dataframe(df.dtypes.reset_index().rename(columns={'index': 'Column', 0: 'Type'}))


        st.subheader("📈 Column Visualizations (3 per row)")

        cols = st.columns(3)
        for idx, col in enumerate(df.columns):
            with cols[idx % 3]:
                st.markdown(f"**🔹 {col}**")
                try:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        fig, ax = plt.subplots()
                        sns.histplot(df[col].dropna(), kde=True, ax=ax)
                        st.pyplot(fig)
                    else:
                        value_counts = df[col].value_counts().nlargest(20)
                        st.bar_chart(value_counts)
                except Exception as e:
                    st.warning(f"Could not plot `{col}`: {e}")
                
            # Start new row every 3 charts
            if (idx + 1) % 3 == 0 and idx + 1 < len(df.columns):
                cols = st.columns(3)


        # Try to remap and clean accident data if possible
        df_mapped = remap_columns(df.copy(), REQUIRED_COLUMNS)
        required_keys = ['date', 'time', 'accident_severity']
        missing = [col for col in required_keys if col not in df_mapped.columns]

        if not missing:
            st.subheader("🧹 Accident Data Analysis (Auto Detected)")
            cleaned_df = cleanData(df_mapped)
            st.dataframe(cleaned_df.head(50))
            prepareGraph(cleaned_df)
        else:
            st.info("This file doesn't appear to be road accident data. Only generic analysis is shown.")

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")

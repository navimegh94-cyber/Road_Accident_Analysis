import streamlit as st
from PIL import Image
# from streamlit_extras.switch_page_button import switch_page

# ---- Page Configuration ----
st.set_page_config(
    page_title="Home | Accident Dashboard",
    page_icon="🚦",
    layout="wide"
)

# ---- Optional Banner Image ----
# Uncomment if you have a banner image
# banner = Image.open("banner.jpg")
# st.image(banner, use_column_width=True)

# ---- Title and Subheading ----
st.markdown("<h1 style='text-align: center;'>🚦 Road Accident Data Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Upload, Explore, and Visualize Accident or Any CSV Data Easily</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---- About Section ----
with st.expander("📘 What Can You Do With This App?"):
    st.markdown("""
    This dashboard lets you:
    
    - 📥 Upload your **own CSV file** — accident or general data
    - 🔍 **Search and preview** the data
    - 📊 Automatically **generate visualizations**
    - 🧹 Perform **accident-specific analysis** (if valid columns exist)
    - ⚙️ Use flexible column name mapping

    You can get started by navigating to the **Data Cleaning and Processing page or use sample data below.
    """)

# ---- Navigation Help / Action Row ----
st.markdown("## 🧭 Get Started")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📂 Upload Your File")
    st.write("Go to the **Data Cleaning and Processing** page from the sidebar to analyze your CSV file.")

# with col2:
#     st.markdown("### 🧪 Try Sample Data")
#     if st.button("Load Sample Data"):
#         st.session_state["load_sample"] = True
#         st.success("Sample data loaded! Now navigate to the 'Upload' page to see the analysis.")
#     if st.button("🚀 Go to Upload Page"):
#         st.switch_page("any") # This matches the file name: Upload.py (case-sensitive)

# ---- Optional Footer ----
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Made with ❤️ using Streamlit | 2025</div>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import os
from datetime import date
from PIL import Image
from fpdf import FPDF
import plotly.express as px

# Paths
DATA_FILE = 'material_specification_data.xlsx'
IMAGE_DIR = 'uploaded_images'
LOGO_PATH = 'Artboard 2.png'

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load logo
st.set_page_config(page_title="Material Spec Manager - By Aadil Sukry", layout="wide")
logo = Image.open(LOGO_PATH)
st.image(logo, width=150)

st.title("📋 Material Specification Manager")

# Load or create Excel database
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE)
    else:
        return pd.DataFrame()

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

# PDF export function
def export_to_pdf(data, output_path, logo_path=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for index, row in data.iterrows():
        pdf.add_page()

        if logo_path and os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=40)
            pdf.set_y(30)

        pdf.set_font("Arial", size=12)
        for key, value in row.items():
            if key == 'Image Path' and isinstance(value, str) and os.path.exists(value):
                pdf.ln(5)
                pdf.image(value, w=80)
                pdf.ln(5)
            else:
                pdf.multi_cell(0, 8, f"{key}: {value}", 0)
                pdf.ln(1)

    pdf.output(output_path)
    return output_path

# Tabs for Pages
page = st.sidebar.selectbox("Navigate", ["Add Material", "View Report", "Analytics Dashboard", "Project Dashboard"])

data = load_data()

if page == "Add Material":
    # [Unchanged: Form to Add Material Entry]
    ...

elif page == "View Report":
    # [Unchanged: Main Report View, Search, Edit/Delete, Export]
    ...

elif page == "Analytics Dashboard":
    # [Unchanged: Charts for Category, Project, Supplier, Origin]
    ...

elif page == "Project Dashboard":
    st.subheader("📁 Project Dashboard")
    if not data.empty:
        all_projects = sorted(data['Project Name'].dropna().unique())
        selected_project = st.selectbox("Select a Project to View", options=all_projects)
        project_data = data[data['Project Name'] == selected_project]

        st.markdown(f"### 🗂️ {selected_project} - {len(project_data)} Material(s)")
        st.dataframe(project_data, use_container_width=True)

        if st.button("📄 Export This Project to PDF"):
            output_path = f"project_{selected_project.replace(' ', '_')}.pdf"
            export_to_pdf(project_data, output_path, logo_path=LOGO_PATH)
            with open(output_path, "rb") as f:
                st.download_button("Download Project PDF", data=f, file_name=output_path)

        with st.expander("📸 View Project Images"):
            for idx, row in project_data.iterrows():
                if isinstance(row["Image Path"], str) and os.path.exists(row["Image Path"]):
                    st.image(row["Image Path"], caption=row["Material/Item Name"], width=200)
    else:
        st.info("No project data available.")

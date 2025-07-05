import streamlit as st
import pandas as pd
import os
from datetime import date
from PIL import Image

# Paths
DATA_FILE = 'material_specification_data.xlsx'
IMAGE_DIR = 'uploaded_images'
LOGO_PATH = 'Artboard 2.png'

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load logo
st.set_page_config(page_title="Material Spec Manager", layout="wide")
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

# Form
st.subheader("➕ Add New Material Specification")
with st.form("material_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input("Project Name")
        location = st.text_input("Location")
        id_package = st.text_input("ID Package Ref")
        prepared_by = st.text_input("Prepared By")
        mat_name = st.text_input("Material/Item Name")
        mat_category = st.selectbox("Material Category", ["Furniture", "Finishes", "Joinery", "Loose FF&E", "Wall Treatment", "Flooring", "Ceiling", "Architectural Detail"])
        area = st.text_input("Area of Application")
        ref_code = st.text_input("Reference Code")
        mat_type = st.text_input("Type")
        brand = st.text_input("Brand / Manufacturer")
        model = st.text_input("Model / Collection Name")
        color = st.text_input("Finish / Color / Pattern")

    with col2:
        dimensions = st.text_input("Dimensions")
        thickness = st.text_input("Thickness / Weight / Density")
        texture = st.text_input("Texture / Surface Treatment")
        edge_detail = st.text_input("Edge / Joint Detail")
        substrate = st.text_input("Substrate")
        fire_rating = st.text_input("Fire Rating / Classification")
        voc = st.text_input("VOC / Sustainability Certs")
        durability = st.text_input("Durability / Abrasion Rating")
        warranty = st.text_input("Warranty / Lifespan")
        fixing = st.text_input("Fixing Method")
        maintenance = st.text_input("Maintenance Guidelines")
        supplier = st.text_input("Supplier Name / Contact")
        origin = st.text_input("Country of Origin")
        lead_time = st.text_input("Lead Time")

    image = st.file_uploader("Upload Material Image", type=["png", "jpg", "jpeg"])

    submit = st.form_submit_button("Submit")

    if submit:
        img_path = ""
        if image:
            img_path = os.path.join(IMAGE_DIR, image.name)
            with open(img_path, "wb") as f:
                f.write(image.read())

        new_entry = pd.DataFrame([{
            "Project Name": project_name,
            "Location": location,
            "ID Package Ref": id_package,
            "Prepared By": prepared_by,
            "Date": date.today(),
            "Material/Item Name": mat_name,
            "Material Category": mat_category,
            "Area of Application": area,
            "Reference Code": ref_code,
            "Type": mat_type,
            "Brand / Manufacturer": brand,
            "Model / Collection Name": model,
            "Finish / Color / Pattern": color,
            "Dimensions": dimensions,
            "Thickness / Weight / Density": thickness,
            "Texture / Surface Treatment": texture,
            "Edge / Joint Detail": edge_detail,
            "Primary Material(s)": "",  # You can expand if needed
            "Substrate": substrate,
            "Fire Rating / Classification": fire_rating,
            "VOC Compliance / Sustainability Certs": voc,
            "Durability / Abrasion Rating": durability,
            "Acoustic / Thermal Performance": "",
            "Water / Moisture Resistance": "",
            "Warranty / Lifespan": warranty,
            "Substrate Requirement": "",
            "Fixing Method": fixing,
            "Installation Notes": "",
            "Maintenance Guidelines": maintenance,
            "Supplier Name / Contact": supplier,
            "Country of Origin": origin,
            "Lead Time": lead_time,
            "MOQ": "",
            "Unit of Measure": "",
            "Unit Cost": "",
            "Sample Status": "",
            "Image Path": img_path
        }])

        db = load_data()
        db = pd.concat([db, new_entry], ignore_index=True)
        save_data(db)
        st.success("✅ Material specification saved!")

# Report View
st.subheader("📑 Material Report Viewer")
data = load_data()

if not data.empty:
    st.dataframe(data, use_container_width=True)
    with st.expander("📸 View Images"):
        for idx, row in data.iterrows():
            if isinstance(row["Image Path"], str) and os.path.exists(row["Image Path"]):
                st.image(row["Image Path"], caption=row["Material/Item Name"], width=200)
else:
    st.info("No materials submitted yet.")

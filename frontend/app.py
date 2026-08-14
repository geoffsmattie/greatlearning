import os

import streamlit as st
import requests

st.title("SuperKart Sales Prediction")

# This is the "two-tier" version of the app: a Streamlit UI that calls a
# separately hosted Flask API (see ../backend). It's kept here for reference
# and for local/Docker use. The version actually deployed live at
# https://share.streamlit.io does NOT depend on a separate backend service —
# see /streamlit_app.py at the repo root, which loads the model directly.
#
# Set the BACKEND_API_URL environment variable to point this UI at your
# running Flask API, e.g.:
#   BACKEND_API_URL=http://127.0.0.1:7860/v1/predict streamlit run app.py
API_URL = os.environ.get("BACKEND_API_URL", "http://127.0.0.1:7860/v1/predict")

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product ID Category", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)
Product_Type_Category = st.selectbox("Product Category Type", ["Perishables", "Non Perishables"])

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

if st.button("Predict", type='primary'):
    try:
        response = requests.post(API_URL, json=product_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            predicted_sales = result["Sales"]
            st.write(f"Predicted Product Store Sales Total: ₹{predicted_sales:.2f}")
        else:
            st.error(f"Error in API request (status {response.status_code}): {response.text}")
    except requests.exceptions.RequestException as exc:
        st.error(f"Could not reach the backend API at {API_URL}: {exc}")

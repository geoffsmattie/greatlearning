"""
SuperKart Sales Forecasting — live app.

This is the single, self-contained app deployed live on Streamlit Community
Cloud (free, no credit card required). It loads the trained model pipeline
directly and runs inference in-process, so it doesn't depend on a separate
backend service being online.

(See /backend and /frontend for the original two-tier Flask API + Streamlit
UI design from the notebook, kept for reference / local Docker use.)
"""
import os

import pandas as pd
import streamlit as st
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "best_superkart_model.joblib")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

st.set_page_config(page_title="SuperKart Sales Predictor", page_icon="🛒")
st.title("🛒 SuperKart Sales Predictor")
st.write(
    "Predict the total sales revenue for a product at a given store, "
    "using a Gradient Boosting model trained on SuperKart's historical sales data."
)

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Product details")
        Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66, step=0.01)
        Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        Product_Allocated_Area = st.number_input(
            "Product Allocated Area (ratio of store display area)",
            min_value=0.0, max_value=1.0, value=0.027, step=0.001, format="%.3f",
        )
        Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08, step=0.01)
        Product_Id_char = st.selectbox(
            "Product ID Category", ["FD", "DR", "NC"],
            help="FD = Food, DR = Drinks, NC = Non-Consumable",
        )
        Product_Type_Category = st.selectbox("Product Category Type", ["Non Perishables", "Perishables"])

    with col2:
        st.subheader("Store details")
        Store_Size = st.selectbox("Store Size", ["Medium", "High", "Small"])
        Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        Store_Type = st.selectbox(
            "Store Type",
            ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"],
        )
        Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16, step=1)

    submitted = st.form_submit_button("Predict Sales", type="primary")

if submitted:
    sample = {
        "Product_Weight": Product_Weight,
        "Product_Sugar_Content": Product_Sugar_Content,
        "Product_Allocated_Area": Product_Allocated_Area,
        "Product_MRP": Product_MRP,
        "Store_Size": Store_Size,
        "Store_Location_City_Type": Store_Location_City_Type,
        "Store_Type": Store_Type,
        "Product_Id_char": Product_Id_char,
        "Store_Age_Years": Store_Age_Years,
        "Product_Type_Category": Product_Type_Category,
    }
    input_data = pd.DataFrame([sample])
    prediction = model.predict(input_data)[0]
    st.success(f"### Predicted Product Store Sales Total: ${prediction:,.2f}")

st.divider()
st.caption(
    "Model: Gradient Boosting Regressor (hyperparameter-tuned via GridSearchCV) "
    "trained on the SuperKart dataset. Source: github.com/geoffsmattie/greatlearning"
)

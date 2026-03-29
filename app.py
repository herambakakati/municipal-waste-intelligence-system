# =========================================
# MUNICIPAL WASTE INTELLIGENCE SYSTEM (FINAL PREMIUM)
# =========================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Waste Intelligence System", layout="wide")

# -------------------------------
# STYLING (PREMIUM UI)
# -------------------------------
st.markdown("""
<style>

/* REMOVE DEFAULT HEADER */
[data-testid="stHeader"] {display:none;}
.block-container {padding-top: 1rem;}

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background:
    linear-gradient(rgba(0,30,20,0.85), rgba(0,40,30,0.95)),
    url("https://thumbs.dreamstime.com/b/waste-sorting-plant-many-different-conveyors-bins-conveyors-filled-various-household-waste-waste-disposal-recycling-290892411.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* HEADER BOX */
.header-box {
    background: linear-gradient(135deg,#052e2b,#064e3b);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(34,197,94,0.4);
    box-shadow: 0 0 25px rgba(34,197,94,0.3);
    margin-bottom: 20px;
}

/* TITLE */
.header-title {
    font-size: 40px;
    font-weight: 800;
    color: #ecfdf5;
}

/* SUBTITLE */
.header-sub {
    font-size: 18px;
    color: #bbf7d0;
}

/* SECTION */
.section {
    color:#ecfdf5;
    font-size:24px;
    font-weight:700;
    margin-top:25px;
}

/* INPUT LABEL */
label {
    color:#d1fae5 !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#16a34a);
    color:white;
    font-size:18px;
    height:50px;
    border-radius:10px;
}

/* KPI CARD */
.card {
    background: rgba(255,255,255,0.06);
    padding:20px;
    border-radius:15px;
    text-align:center;
    backdrop-filter: blur(6px);
    box-shadow: 0 0 15px rgba(0,0,0,0.3);
}

/* FOOTER */
.footer {
    text-align:center;
    color:#6ee7b7;
    margin-top:40px;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER (FIXED)
# -------------------------------
st.markdown("""
<div class="header-box">
    <div class="header-title">
        ♻️ Municipal Waste Management Intelligence System
    </div>
    <div class="header-sub">
        AI/ML based decision support system for optimizing waste collection, recycling efficiency, and sustainable urban management.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD MODEL
# -------------------------------
model = pickle.load(open("waste_model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# -------------------------------
# INPUT SECTION
# -------------------------------
st.markdown('<div class="section">📊 Input Parameters</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    recycling_rate = st.slider("Recycling Rate (%)", 30, 85, 55)
    population_density = st.number_input("Population Density", 2000, 30000, 12000)
    awareness = st.slider("Awareness Campaigns", 0, 20, 10)

with col2:
    efficiency = st.slider("Municipal Efficiency Score", 1, 10, 7)
    landfill_capacity = st.number_input("Landfill Capacity (Tons)", 20000, 100000, 60000)
    year = st.selectbox("Year", [2019,2020,2021,2022,2023])

with col3:
    cost_per_ton = st.number_input("Cost per Ton (₹)", 500, 5000, 2500)
    waste_type = st.selectbox("Waste Type", ["Organic","Plastic","E-Waste","Hazardous"])
    disposal = st.selectbox("Disposal Method", ["Recycling","Landfill","Incineration"])

# -------------------------------
# PREPARE INPUT
# -------------------------------
def prepare_input():
    df = pd.DataFrame([np.zeros(len(columns))], columns=columns)

    df["Recycling Rate (%)"] = recycling_rate
    df["Population Density (People/km²)"] = population_density
    df["Municipal Efficiency Score (1-10)"] = efficiency
    df["Cost of Waste Management (₹/Ton)"] = cost_per_ton
    df["Awareness Campaigns Count"] = awareness
    df["Landfill Capacity (Tons)"] = landfill_capacity
    df["Year"] = year

    for col in columns:
        if col == f"Waste Type_{waste_type}":
            df[col] = 1
        if col == f"Disposal Method_{disposal}":
            df[col] = 1

    return df

# -------------------------------
# PREDICTION
# -------------------------------
if st.button("🚀 Generate Prediction"):

    input_df = prepare_input()
    waste_pred = model.predict(input_df)[0]
    total_cost = waste_pred * cost_per_ton

    # STATUS LOGIC
    if waste_pred < 4000:
        status, color = "🟢 Efficient", "#22c55e"
        msg = "Low waste generation indicates efficient municipal operations."
    elif waste_pred < 7000:
        status, color = "🟡 Moderate Load", "#facc15"
        msg = "Waste levels are moderate and require optimization."
    else:
        status, color = "🔴 Critical Load", "#ef4444"
        msg = "High waste generation may strain infrastructure."

    # -------------------------------
    # DASHBOARD
    # -------------------------------
    st.markdown('<div class="section">📊 Results Dashboard</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div class="card">
        <h4 style="color:#a7f3d0;">Waste Generated</h4>
        <h2 style="color:#ecfdf5;">{int(waste_pred)} Tons/Day</h2>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="card">
        <h4 style="color:#a7f3d0;">Estimated Cost</h4>
        <h2 style="color:#ecfdf5;">₹ {int(total_cost):,} / Day</h2>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="card">
        <h4 style="color:#a7f3d0;">System Status</h4>
        <h2 style="color:{color};">{status}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="color:#bbf7d0; margin-top:15px;">
    👉 {msg}
    </p>
    """, unsafe_allow_html=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("""
<div class='footer'>
✨ Developed by <b>Heramba Kakati</b>
</div>
""", unsafe_allow_html=True)
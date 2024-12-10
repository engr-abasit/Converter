import streamlit as st
from pathlib import Path

# App Configuration
st.set_page_config(page_title="Engineering Unit Converter", page_icon="⚙️", layout="centered")

# Background Image Styling (Online Image)
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1558888436-02cf35f70d10");
    background-size: cover;
    background-position: center;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.7);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.title("⚙️ Engineering Unit Converter")

# Conversion Data
conversion_factors = {
    "Length": {
        "units": ["Meters", "Kilometers", "Centimeters", "Millimeters", "Inches", "Feet", "Yards", "Miles"],
        "factors": {
            "Meters": 1.0, "Kilometers": 0.001, "Centimeters": 100.0, "Millimeters": 1000.0,
            "Inches": 39.3701, "Feet": 3.28084, "Yards": 1.09361, "Miles": 0.000621371,
        },
        "allow_negative": False,
    },
    "Mass": {
        "units": ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces", "Tons (Metric)"],
        "factors": {
            "Kilograms": 1.0, "Grams": 1000.0, "Milligrams": 1e6,
            "Pounds": 2.20462, "Ounces": 35.274, "Tons (Metric)": 0.001,
        },
        "allow_negative": False,
    },
    "Force": {
        "units": ["Newtons", "Kilonewtons", "Pounds-force", "Kilogram-force"],
        "factors": {
            "Newtons": 1.0, "Kilonewtons": 0.001, "Pounds-force": 0.224809, "Kilogram-force": 0.101972,
        },
        "allow_negative": True,
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "convert": lambda v, f, t: (
            v if f == t else
            (v * 9 / 5 + 32 if f == "Celsius" and t == "Fahrenheit" else
             v - 273.15 if f == "Kelvin" and t == "Celsius" else
             v - 273.15 * 9 / 5 + 32 if f == "Kelvin" and t == "Fahrenheit" else
             (v - 32) * 5 / 9 if f == "Fahrenheit" and t == "Celsius" else
             (v - 32) * 5 / 9 + 273.15 if f == "Fahrenheit" and t == "Kelvin" else
             v + 273.15 if f == "Celsius" and t == "Kelvin" else
             v)
        ),
        "allow_negative": True,
    },
    "Pressure": {
        "units": ["Pascals", "Bar", "Atmospheres", "PSI"],
        "factors": {
            "Pascals": 1.0, "Bar": 1e-5, "Atmospheres": 9.8692e-6, "PSI": 0.000145038,
        },
        "allow_negative": False,
    },
}

# Dropdown for Conversion Type
conversion_type = st.selectbox("Select Conversion Type:", list(conversion_factors.keys()))

# Input Section
st.header(f"Enter Value for {conversion_type} Conversion")

# Allow negative values where appropriate
min_value = None if conversion_factors[conversion_type]["allow_negative"] else 0.0
value = st.number_input("Enter value:", min_value=min_value, format="%.4f")

# Unit Selection
units = conversion_factors[conversion_type]["units"]
from_unit = st.selectbox("From:", units)
to_unit = st.selectbox("To:", units)

# Conversion Logic
if st.button("Convert"):
    if from_unit == to_unit:
        result = value
    else:
        if conversion_type == "Temperature":
            result = conversion_factors["Temperature"]["convert"](value, from_unit, to_unit)
        else:
            factor_from = conversion_factors[conversion_type]["factors"][from_unit]
            factor_to = conversion_factors[conversion_type]["factors"][to_unit]
            result = value / factor_from * factor_to

    st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

import streamlit as st
import random

# Set page config
st.set_page_config(page_title="Main Page", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton > button {
        width: 200px;
        margin: 10px;
        border-radius: 10px;
        height: 50px;
    }
    .emergency-button > button {
        background-color: #ff4b4b;
        color: white;
    }
    .normal-button > button {
        background-color: #ffffff;
        color: black;
        border: 2px solid #e0e0e0;
    }
    .map-container {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        min-height: 300px;
        position: relative;
    }
    .dot {
        height: 20px;
        width: 20px;
        border-radius: 50%;
        display: inline-block;
        margin: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Create the map container
st.markdown("""
    <div class="map-container">
        <!-- Map dots will be added here in the future -->
    </div>
""", unsafe_allow_html=True)

# Legend
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("⚪ members")
with col2:
    st.markdown("🔴 distress call")
with col3:
    st.markdown("🔷 you")

# Create two rows of buttons
col1, col2 = st.columns(2)

# First row of buttons
with col1:
    st.markdown('<div class="normal-button">', unsafe_allow_html=True)
    st.button("Edit Profile")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="normal-button">', unsafe_allow_html=True)
    st.button("See user profiles")
    st.markdown('</div>', unsafe_allow_html=True)

# Second row of buttons (emergency buttons)
with col1:
    st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
    st.button("Distress Call")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
    st.button("Manage requests")
    st.markdown('</div>', unsafe_allow_html=True)

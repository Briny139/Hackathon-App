import streamlit as st
import time

# Configure the page
st.set_page_config(
    page_title="Distress Call Confirmation",
    page_icon="🆘",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton > button {
        width: 150px;
        border-radius: 10px;
        height: 45px;
        margin: 10px;
    }
    .cancel-button > button {
        background-color: #ff4b4b;
        color: white;
    }
    .confirm-button > button {
        background-color: #00cc00;
        color: white;
    }
    .status-box {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        background-color: #f8f9fa;
    }
    .waiting-text {
        color: #FFA500;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Distress Call")

# Display submitted information
with st.container():
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.write("Details and description of needs:")
    # Here you would typically pull the actual data from session state
    st.text("Sample distress call details...")
    st.markdown('</div>', unsafe_allow_html=True)

# Status indicators
st.markdown('<div class="waiting-text">Waiting for response...</div>', 
            unsafe_allow_html=True)

# Progress indicator
progress_text = "Searching for available helpers nearby..."
progress_bar = st.progress(0)

# Simulate progress
if 'progress' not in st.session_state:
    st.session_state.progress = 0

if st.session_state.progress < 100:
    st.session_state.progress += 1
    progress_bar.progress(st.session_state.progress)
    
# Buttons
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="cancel-button">', unsafe_allow_html=True)
    if st.button("Cancel"):
        st.session_state.progress = 0
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="confirm-button">', unsafe_allow_html=True)
    if st.button("Update"):
        st.session_state.progress = 0
        st.switch_page("pages/1_distress_call.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Add back button
if st.button("← Back"):
    st.session_state.progress = 0
    st.switch_page("pages/1_distress_call.py")

# Optional: Display nearby helpers (can be added later)
st.markdown("### Nearby Helpers")
with st.expander("Show available helpers"):
    st.write("Helper 1 - 0.5 miles away")
    st.write("Helper 2 - 1.2 miles away")
    st.write("Helper 3 - 1.8 miles away") 
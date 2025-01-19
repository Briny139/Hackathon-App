import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Distress Call",
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
    }
    .cancel-button > button {
        background-color: #ff4b4b;
        color: white;
    }
    .confirm-button > button {
        background-color: #00cc00;
        color: white;
    }
    .description-box {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Distress Call")

# Description input
with st.container():
    st.markdown('<div class="description-box">', unsafe_allow_html=True)
    st.text_area("Details and description of needs:", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

# Location section
st.subheader("Location")
location_options = ["Share current location", "Enter address manually"]
selected_location = st.radio("Choose location option:", location_options)

if selected_location == "Enter address manually":
    st.text_input("Enter your address:")

# Duration section
st.subheader("Expected Duration of Need")
duration_options = ["1-2 hours", "2-4 hours", "4-8 hours", "8+ hours"]
st.selectbox("Select duration:", duration_options)

# Buttons at the bottom
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="cancel-button">', unsafe_allow_html=True)
    if st.button("Cancel"):
        st.switch_page("app.py")  # Return to main page
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="confirm-button">', unsafe_allow_html=True)
    if st.button("Confirm"):
        st.switch_page("pages/2_distress_confirmation.py")  # Go to confirmation page
    st.markdown('</div>', unsafe_allow_html=True)

# Add back button
if st.button("← Back to Main"):
    st.switch_page("app.py") 
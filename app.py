import streamlit as st
import time

# Configure the default settings of the page
st.set_page_config(
    page_title="Safety App",
    page_icon="🆘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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

# Session state initialization
if 'name' not in st.session_state:
    st.session_state.name = ''
    st.session_state.signed_up = False

# Sign Up Page
if not st.session_state.signed_up:
    st.title("Sign Up Page")
    with st.container():
        st.markdown("""
            <div style="padding: 20px; 
                        border: 2px solid #f0f0f0; 
                        border-radius: 10px;
                        margin: 10px;">
        """, unsafe_allow_html=True)
        
        name = st.text_input("Your Name:")
        if st.button("Next"):
            if name.strip():
                st.session_state.name = name
                st.session_state.signed_up = True
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please enter your name")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Main Page
else:
    st.title("Main Page")
    
    # Map container
    with st.container():
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        # Placeholder for map - you can integrate actual map here
        st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("⚪ members")
    with col2:
        st.markdown("🔴 distress call")
    with col3:
        st.markdown("🔷 you")

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="normal-button">', unsafe_allow_html=True)
        if st.button("Edit Profile"):
            st.switch_page("pages/3_edit_profile.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="normal-button">', unsafe_allow_html=True)
        if st.button("See user profiles"):
            st.switch_page("pages/5_search_users.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
        if st.button("Distress Call"):
            st.switch_page("pages/1_distress_call.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="emergency-button">', unsafe_allow_html=True)
        if st.button("Manage requests"):
            st.switch_page("pages/4_managing_requests.py")
        st.markdown('</div>', unsafe_allow_html=True)

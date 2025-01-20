import streamlit as st

# Hide default sidebar
st.markdown("""
    <style>
        button[kind="header"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="stSidebarNav"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state for distress call data
if 'distress_call_data' not in st.session_state:
    st.session_state.distress_call_data = {
        'notes': '',
        'urgency': '',
        'category': [],
        'submitted': False
    }

def show_confirmation_page():
    col1, col2 = st.columns([1, 4])
    
    # Circle logo placeholder in top left
    with col1:
        st.markdown("""
            <div style="
                width: 50px;
                height: 50px;
                background-color: #ffffff;
                border-radius: 50%;
                margin: 10px;
            "></div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.title("Distress Call")
    
    st.text_area("Notes and description of needs", 
                value=st.session_state.distress_call_data['notes'],
                disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Level of Urgency")
    with col2:
        st.write(st.session_state.distress_call_data['urgency'])
    
    st.write("Category of Needs")
    st.write(", ".join(st.session_state.distress_call_data['category']))
    
    st.write("Waiting for response...", help="Your distress call has been submitted")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", type="primary"):
            st.session_state.distress_call_data['submitted'] = False
            st.rerun()
    with col2:
        if st.button("Update", type="secondary"):
            st.session_state.distress_call_data['submitted'] = False
            st.rerun()

def show_distress_call_form():
    st.title("Distress Call")
    
    # Notes and description
    notes = st.text_area("Notes and description of needs",
                        value=st.session_state.distress_call_data['notes'])
    
    # Urgency level
    col1, col2 = st.columns(2)
    with col1:
        st.write("Level of Urgency")
    with col2:
        urgency = st.selectbox("",
                             options=["Immediate", "High", "Moderate"],
                             index=None,
                             placeholder="Select urgency level")
    
    # Category selection
    category = st.multiselect("Category of Needs",
                            options=["Resource", "Service"],
                            default=st.session_state.distress_call_data['category'])
    
    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", type="primary"):
            st.session_state.distress_call_data = {
                'notes': '',
                'urgency': '',
                'category': [],
                'submitted': False
            }
            st.rerun()
    
    with col2:
        if st.button("Confirm", type="secondary"):
            if not notes or not urgency or not category:
                st.error("Please fill in all fields")
                return
            
            st.session_state.distress_call_data = {
                'notes': notes,
                'urgency': urgency,
                'category': category,
                'submitted': True
            }
            st.rerun()

# Main app logic
if st.session_state.distress_call_data['submitted']:
    show_confirmation_page()
else:
    show_distress_call_form()

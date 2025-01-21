import streamlit as st
from database import DatabaseManager
from components import show_logo

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
        'specific_needs': [],
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
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Category of Needs")
    with col2:
        st.write(", ".join(st.session_state.distress_call_data['category']))
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Specific Needs")
    with col2:
        st.write(", ".join(st.session_state.distress_call_data['specific_needs']))
    
    # Add animated waiting message
    st.markdown("""
        <style>
            @keyframes ellipsis {
                0% { content: ''; }
                25% { content: '.'; }
                50% { content: '..'; }
                75% { content: '...'; }
            }
            
            .waiting-text {
                color: #FF0000;
                font-size: 24px;
                font-weight: bold;
                margin: 20px 0;
            }
            
            .waiting-text::after {
                content: '';
                animation: ellipsis 2s infinite;
            }
        </style>
        <div class='waiting-text'>Waiting for response</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 14px; color: #666;'>Your distress call has been submitted</div>", 
                unsafe_allow_html=True)
    
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
    
    # Resource/Service specific dropdown
    if category:
        resource_options = {
            "Resource": ["Food", "Water", "Shelter", "Medical Supplies", "Clothing"],
            "Service": ["Medical Care", "Transportation", "Legal Aid", "Counseling", "Child Care"]
        }
        
        specific_needs = []
        for cat in category:
            specific_need = st.selectbox(
                f"Select specific {cat.lower()}",
                options=resource_options[cat],
                key=f"specific_{cat.lower()}",
                index=None,
                placeholder=f"Choose {cat.lower()}"
            )
            if specific_need:
                specific_needs.append(specific_need)
    
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
            if not notes or not urgency or not category or not specific_needs:
                st.error("Please fill in all fields")
                return
            
            st.session_state.distress_call_data = {
                'notes': notes,
                'urgency': urgency,
                'category': category,
                'specific_needs': specific_needs,
                'submitted': True
            }
            st.rerun()

def show_distress_call():
    show_logo()
    
    # Initialize all required session state variables
    if 'distress_submitted' not in st.session_state:
        st.session_state.distress_submitted = False
    
    if 'distress_call_data' not in st.session_state:
        st.session_state.distress_call_data = {
            'notes': '',
            'urgency': '',
            'category': [],
            'submitted': False
        }
    
    if not st.session_state.distress_submitted:
        # Show the distress call form
        
        if st.session_state.distress_call_data['submitted']:
            show_confirmation_page()
        
        else:
            show_distress_call_form()

# Main app logic
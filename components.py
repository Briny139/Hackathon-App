import streamlit as st

def show_logo():
    # Create a container for the logo and make it clickable
    with st.container():
        col1, col2, col3 = st.columns([1,3,1])
        with col1:
            if st.button("🏠", help="Back to Main Page"):
                st.session_state.page = "main"
                # Clear any page-specific session states
                if 'distress_submitted' in st.session_state:
                    del st.session_state.distress_submitted
                if 'distress_data' in st.session_state:
                    del st.session_state.distress_data
                if 'active_request' in st.session_state:
                    del st.session_state.active_request
                if 'recipient' in st.session_state:
                    del st.session_state.recipient
                st.rerun() 
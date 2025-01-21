import streamlit as st
from database import DatabaseManager
from components import show_logo

def show_manage_requests():
    show_logo()
    # Add custom CSS for styling
    st.markdown("""
        <style>
        .request-card {
            border: 1px solid #e1e4e8;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .need-text {
            color: #D62828;  /* Emergency red color */
            font-size: 18px;
            margin: 0;
        }
        .time-text {
            color: #457B9D;  /* Blue color */
            font-size: 14px;
        }
        .distance-text {
            color: #1D3557;  /* Dark blue color */
            font-size: 14px;
        }
        .sos-logo {
            color: #D62828;
            font-size: 24px;
            margin-right: 10px;
        }
        .stButton button {
            border-radius: 5px;
            font-weight: 500;
        }
        .respond-button button {
            background-color: #457B9D;
            color: white;
        }
        .notes-button button {
            background-color: #E9ECEF;
            color: #1D3557;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Page header with logo
    st.markdown('<h1 style="display: flex; align-items: center;"><span class="sos-logo">🆘</span>Requests</h1>', 
                unsafe_allow_html=True)
    
    # Get all active requests from database
    requests = DatabaseManager.get_all_requests()
    
    if not requests:
        st.info("No active requests at the moment.")
        return
    
    # Display each request in a card format
    for request in requests:
        st.markdown('<div class="request-card">', unsafe_allow_html=True)
        
        # Request details in a single line
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f'<p class="need-text">🆘 {request["need"]}</p>', 
                      unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="time-text">⏰ {request["time"]}</p>', 
                      unsafe_allow_html=True)
        with col3:
            st.markdown(f'<p class="distance-text">📍 {request["distance"]}</p>', 
                      unsafe_allow_html=True)
        
        # Action buttons in a row
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="respond-button">', unsafe_allow_html=True)
            if st.button("🤝 Respond", key=f"respond_{request['id']}", 
                       use_container_width=True):
                # Store request data in session state
                st.session_state.active_request = request
                st.session_state.recipient = request['requester']
                st.session_state.page = "communication"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="notes-button">', unsafe_allow_html=True)
            if st.button("📝 See notes", key=f"notes_{request['id']}", 
                       use_container_width=True):
                # Handle viewing notes
                pass
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) 
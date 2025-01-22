import streamlit as st
from database import DatabaseManager
from components import show_logo
import sqlite3
import uuid

def add_sample_requests():
    # Check for and add sample requests if none exist
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    try:
        # Check if there are any active requests
        c.execute("SELECT COUNT(*) FROM requests WHERE status = 'active'")
        count = c.fetchone()[0]
        
        if count == 0:
            print("No active requests found, adding samples...")
            # Add sample requests with realistic data
            sample_requests = [
                ("Medical Supplies", "Need urgent insulin supplies", "10km"),
                ("Food Aid", "Require baby formula and diapers", "3km"),
                ("Transport", "Need transportation to medical facility", "5km"),
                ("Shelter", "Temporary housing needed for family of 4", "7km"),
                ("Water", "Clean drinking water needed", "2km")
            ]
            
            for need, notes, distance in sample_requests:
                try:
                    DatabaseManager.create_request(
                        need=need,
                        requester_id=str(uuid.uuid4()),  # Generate random requester_id
                        requester_name=f"Sample User {uuid.uuid4().hex[:4]}",  # Generate random name
                        distance=distance
                    )
                    print(f"Added sample request: {need}")
                except Exception as e:
                    print(f"Error adding sample request {need}: {str(e)}")
            
            print("Finished adding sample requests")
            
        # Verify requests were added
        c.execute("SELECT COUNT(*) FROM requests WHERE status = 'active'")
        new_count = c.fetchone()[0]
        print(f"Total active requests in database: {new_count}")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def show_manage_requests():
    show_logo()

    #adding sample requests if there are none
    add_sample_requests()

    # Add custom CSS for styling
    st.markdown("""
        <style>
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
    
    # Display each request in a container
    for request in requests:
        with st.container(border=True):
            
            # Request details in columns
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
            
            # Action buttons in columns
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="respond-button">', unsafe_allow_html=True)
                if st.button("🤝 Respond", key=f"respond_{request['id']}", 
                           use_container_width=True):
                    st.session_state.active_request = request
                    st.session_state.recipient = request['requester']
                    st.session_state.page = "communication"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="notes-button">', unsafe_allow_html=True)
                if st.button("📝 See notes", key=f"notes_{request['id']}", 
                           use_container_width=True):
                    st.session_state.show_notes = request['id']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show notes if requested
            @st.dialog("Notes", width="large")
            def show_notes():
                st.write(request.get('notes', 'No notes available'))

            if st.session_state.get('show_notes') == request['id']:
                show_notes()
                    
            
            st.markdown('</div>', unsafe_allow_html=True) 
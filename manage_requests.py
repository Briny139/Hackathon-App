import streamlit as st
from database import DatabaseManager

def show_manage_requests():
    st.title("Managing Requests")
    
    # Container for requests list
    with st.container():
        st.subheader("Requests")
        
        # Get requests from database
        requests = DatabaseManager.get_all_requests()
        
        if not requests:
            st.info("No active requests at the moment")
            return
        
        for request in requests:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write("**Need:** " + str(request['need']))
                with col2:
                    st.write("**Time:** " + str(request['time']))
                with col3:
                    st.write("**Distance:** " + str(request['distance']))
                
                col4, col5 = st.columns(2)
                with col4:
                    if st.button("Respond", key=f"respond_{request['id']}"):
                        st.session_state.page = "communication"
                        st.session_state.active_request = request
                        st.session_state.recipient = request['requester']
                        st.rerun()
                with col5:
                    if st.button("See notes", key=f"notes_{request['id']}"):
                        st.info("Notes for this request will appear here")
                
                st.divider() 
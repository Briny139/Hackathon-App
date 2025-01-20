import streamlit as st
from database import save_message, get_messages, mark_request_complete

def show_communication_page():
    st.header("Communication Page")
    
    if 'active_request' not in st.session_state:
        st.error("No active request found")
        if st.button("Back to Requests"):
            st.session_state.page = "manage_requests"
            st.rerun()
        return
    
    # Header with names and request info
    st.subheader("Request: " + st.session_state.active_request['need'])
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.write("**Your name:** " + "Current User")  # Replace with actual user name
    with col2:
        if st.button("Complete"):
            mark_request_complete(st.session_state.active_request['id'])
            st.success("Request marked as complete")
            st.session_state.page = "manage_requests"
            st.rerun()
    with col3:
        st.write("**Recipient:** " + st.session_state.recipient)
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        messages = get_messages(st.session_state.active_request['id'])
        
        for msg in messages:
            if msg["sender"] == "Current User":  # Replace with actual user check
                st.write("**You:** " + str(msg['message']))
            else:
                st.write("**" + msg["sender"] + ":** " + str(msg['message']))
    
    # Message input
    with st.container():
        message_input = st.text_input("Type your message...")
        if st.button("Send") and message_input.strip():
            save_message(
                st.session_state.active_request['id'],
                "current_user_id",  # Replace with actual user ID
                "Current User",     # Replace with actual user name
                message_input
            )
            st.rerun()
    
    # Back button
    if st.button("Back to Requests"):
        st.session_state.page = "manage_requests"
        if 'active_request' in st.session_state:
            del st.session_state.active_request
        if 'recipient' in st.session_state:
            del st.session_state.recipient
        st.rerun() 
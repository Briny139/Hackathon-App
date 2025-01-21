import streamlit as st
from database import DatabaseManager
from components import show_logo

def show_communication_page():
    # Add custom CSS for styling
    st.markdown("""
        <style>
        .chat-message {
            padding: 8px;  /* Reduced padding */
            border-radius: 8px;
            margin: 4px 0;  /* Reduced margin */
        }
        .user-message {
            background-color: #457B9D;
            color: white;
            margin-left: 20%;
        }
        .other-message {
            background-color: #E9ECEF;
            margin-right: 20%;
        }
        .message-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 0.8rem;  /* Reduced padding */
            background-color: white;
            border-top: 1px solid #ddd;
            z-index: 1000;
        }
        .chat-container {
            height: 200px;  /* Reduced from 300px */
            overflow-y: auto;
            margin-bottom: 60px;  /* Reduced margin */
            padding: 8px;  /* Reduced padding */
        }
        .stButton button {
            margin-top: 0;
            padding: 0.4rem 0.8rem;  /* Reduced padding */
            height: 38px;  /* Reduced height */
        }
        .distance-text {
            text-align: right;
            padding-right: 20px;
        }
        footer {
            visibility: hidden;
        }
        /* Reduce spacing around headers */
        h1, h3 {
            margin: 0.5rem 0;
            padding: 0;
        }
        /* Reduce spacing around paragraphs */
        p {
            margin: 0.3rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    show_logo()
    
    if 'active_request' not in st.session_state:
        st.error("No active request found")
        if st.button("Back to Requests"):
            st.session_state.page = "manage_requests"
            st.rerun()
        return
    
    # Header with request info (more compact)
    st.markdown(f"## 🆘 {st.session_state.active_request['need']}")  # Changed from title to h2
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**From:** {st.session_state.recipient}")
    with col2:
        if st.button("✅ Complete"):
            DatabaseManager.mark_request_complete(st.session_state.active_request['id'])
            st.success("Request marked as complete")
            st.session_state.page = "manage_requests"
            st.rerun()
    with col3:
        st.markdown(f'<p class="distance-text">**📍 {st.session_state.active_request["distance"]}**</p>', 
                   unsafe_allow_html=True)
    
    # Chat section (more compact)
    st.markdown("### Chat")
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        messages = DatabaseManager.get_messages(st.session_state.active_request['id'])
        
        for msg in messages:
            is_user = msg["sender"] == st.session_state.user_data.get('name')
            message_class = "user-message" if is_user else "other-message"
            sender = "You" if is_user else msg["sender"]
            
            st.markdown(
                f'<div class="chat-message {message_class}">'
                f'<strong>{sender}:</strong> {msg["message"]}'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fixed position message input (more compact)
    st.markdown('<div class="message-input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        message = st.text_input("Type your message...", key="message_input", label_visibility="collapsed")
    with col2:
        if st.button("📤", key="send_button", use_container_width=True) and message.strip():
            DatabaseManager.save_message(
                st.session_state.active_request['id'],
                st.session_state.user_data.get('user_id', 'unknown'),
                st.session_state.user_data.get('name', 'You'),
                message
            )
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Requests"):
        st.session_state.page = "manage_requests"
        if 'active_request' in st.session_state:
            del st.session_state.active_request
        if 'recipient' in st.session_state:
            del st.session_state.recipient
        st.rerun() 
import streamlit as st

st.set_page_config(page_title="Communication", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .chat-container {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        height: 400px;
        overflow-y: auto;
    }
    .message {
        padding: 10px;
        margin: 5px;
        border-radius: 10px;
    }
    .sent {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .received {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .input-area {
        position: fixed;
        bottom: 20px;
        width: 100%;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Chat")

# Chat header with user info
st.write("Chatting with: John Doe")
st.write("Status: Online")

# Chat messages container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Sample messages
    st.markdown('<div class="message received">Hey, I saw your distress call. How can I help?</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="message sent">Thank you for responding! I need assistance with...</div>', 
                unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Message input area
with st.container():
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    col1, col2 = st.columns([4,1])
    with col1:
        message = st.text_input("Type your message...", key="message")
    with col2:
        st.button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Back Button
if st.button("← Back"):
    st.switch_page("app.py") 
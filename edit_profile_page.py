import streamlit as st

# Hide default sidebar
st.markdown("""
    <style>
        button[kind="header"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
        div[data-testid="stSidebarNav"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state for resources and services
if 'user_resources' not in st.session_state:
    st.session_state.user_resources = set()

if 'user_services' not in st.session_state:
    st.session_state.user_services = set()

if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
    st.session_state.popup_category = ''

def show_add_popup(category):
    with st.form(key=f"add_{category}_form"):
        st.subheader(f"Select {category}")
        
        options = [f"{category[:-1]} {i}" for i in range(1, 5)]
        selection = st.selectbox(
            f"Choose {category}",
            options=options,
            index=None,
            placeholder=f"Select {category[:-1]}"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Cancel"):
                st.session_state.show_popup = False
                st.rerun()
        with col2:
            if st.form_submit_button("Save"):
                if selection:
                    if category == "Resources":
                        st.session_state.user_resources.add(selection)
                    else:
                        st.session_state.user_services.add(selection)
                    st.session_state.show_popup = False
                    st.rerun()
                else:
                    st.error("Please make a selection")

def main():
    col1, col2 = st.columns([1, 4])
    
    # Logo
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
    
    # Profile Photo placeholder box - centered
    st.markdown("""
        <div style="
            width: 150px;
            height: 150px;
            background-color: #ffffff20;
            border: 2px solid #ffffff40;
            border-radius: 10px;
            margin: 10px auto;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <span style="color: #ffffff80;">Profile Photo</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Name placeholder - centered and styled
    st.markdown("""
        <style>
            div[data-testid="stTextInput"] {
                width: 150px !important;
                margin: 0 auto;
            }
        </style>
    """, unsafe_allow_html=True)
    st.text_input("", value="Name", key="user_name", disabled=True)
    
    # Resources Section
    st.subheader("Resources")
    
    # Display selected resources
    for resource in sorted(st.session_state.user_resources):
        st.button(resource, key=f"resource_{resource}")
    
    # Add Resource button
    if st.button("Add +", key="add_resource"):
        st.session_state.show_popup = True
        st.session_state.popup_category = "Resources"
        st.rerun()
    
    # Services Section
    st.subheader("Services")
    
    # Display selected services
    for service in sorted(st.session_state.user_services):
        st.button(service, key=f"service_{service}")
    
    # Add Service button
    if st.button("Add +", key="add_service"):
        st.session_state.show_popup = True
        st.session_state.popup_category = "Services"
        st.rerun()
    
    # Show popup if triggered
    if st.session_state.show_popup:
        with st.container():
            st.markdown("""
                <style>
                    div[data-testid="stForm"] {
                        background-color: #262730;
                        padding: 20px;
                        border-radius: 10px;
                        border: 1px solid #ffffff30;
                    }
                </style>
            """, unsafe_allow_html=True)
            show_add_popup(st.session_state.popup_category)

if __name__ == "__main__":
    main()
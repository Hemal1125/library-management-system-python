"""
pages/1_Login.py
"""

import streamlit as st
from auth import login_user, is_logged_in

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("📚 Library Management System")
st.subheader("Login")

if is_logged_in():
    st.success(f"You are already logged in as {st.session_state['user_name']}.")
    st.info("Use the sidebar to navigate to other pages.")
else:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(email, password):
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password.")
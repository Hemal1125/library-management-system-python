"""
app.py
"""

import streamlit as st
from auth import is_logged_in, render_sidebar_user_info

st.set_page_config(page_title="Library Management System", page_icon="📚")

render_sidebar_user_info()

st.title("📚 Library Management System")

if is_logged_in():
    st.success(f"Welcome back, {st.session_state['user_name']}!")
    st.write("Use the sidebar to navigate.")
else:
    st.info("Please log in using the **Login** page in the sidebar to continue.")
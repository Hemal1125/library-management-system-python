"""
auth.py
"""

import bcrypt
import streamlit as st
from database import SessionLocal
from models import User, RoleEnum


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def login_user(email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.password_hash):
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user.id
            st.session_state["user_name"] = user.name
            st.session_state["user_role"] = user.role.value
            return True
        return False
    finally:
        db.close()


def logout_user():
    st.session_state["logged_in"] = False
    st.session_state["user_id"] = None
    st.session_state["user_name"] = None
    st.session_state["user_role"] = None


def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)


def is_admin() -> bool:
    return st.session_state.get("user_role") == RoleEnum.admin.value


def require_login():
    if not is_logged_in():
        st.warning("Please log in first.")
        st.stop()


def require_admin():
    require_login()
    if not is_admin():
        st.error("You don't have permission to view this page.")
        st.stop()
def render_sidebar_user_info():
    if is_logged_in():
        st.sidebar.markdown("---")
        st.sidebar.write(f"👤 **{st.session_state['user_name']}**")
        st.sidebar.write(f"Role: {st.session_state['user_role']}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
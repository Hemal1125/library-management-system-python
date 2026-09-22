"""
pages/4_Members.py
"""

import streamlit as st
import pandas as pd
from auth import require_admin
from models import RoleEnum
from crud.user_crud import (
    create_user, get_all_users, get_user_by_id, update_user, delete_user
)

st.set_page_config(page_title="Members", page_icon="👥")
require_admin()

st.title("👥 Members")

users = get_all_users()

if users:
    df = pd.DataFrame([{
        "ID": u.id,
        "Name": u.name,
        "Email": u.email,
        "Role": u.role.value,
    } for u in users])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No members found.")

st.divider()
st.subheader("Manage Members")

tab_add, tab_edit, tab_delete = st.tabs(["➕ Add", "✏️ Edit", "🗑️ Delete"])

with tab_add:
    with st.form("add_user_form", clear_on_submit=True):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", [RoleEnum.member.value, RoleEnum.admin.value])
        submitted = st.form_submit_button("Add Member")

        if submitted:
            if name and email and password:
                user, msg = create_user(name, email, password, RoleEnum(role))
                if user:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("All fields are required.")

with tab_edit:
    user_ids = [u.id for u in users]
    if user_ids:
        selected_id = st.selectbox("Select Member ID to edit", user_ids)
        user = get_user_by_id(selected_id)

        if user:
            with st.form("edit_user_form"):
                name = st.text_input("Name", value=user.name)
                email = st.text_input("Email", value=user.email)
                role = st.selectbox(
                    "Role",
                    [RoleEnum.member.value, RoleEnum.admin.value],
                    index=0 if user.role == RoleEnum.member else 1
                )
                updated = st.form_submit_button("Update Member")

                if updated:
                    update_user(selected_id, name, email, RoleEnum(role))
                    st.success("Member updated.")
                    st.rerun()
    else:
        st.info("No members to edit.")

with tab_delete:
    user_ids = [u.id for u in users]
    if user_ids:
        delete_id = st.selectbox("Select Member ID to delete", user_ids, key="del_user_select")
        if st.button("Delete Member", type="primary"):
            if delete_id == st.session_state["user_id"]:
                st.error("You cannot delete your own account while logged in.")
            else:
                delete_user(delete_id)
                st.success("Member deleted.")
                st.rerun()
    else:
        st.info("No members to delete.")
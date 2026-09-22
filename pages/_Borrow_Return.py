"""
pages/3_Borrow_Return.py
"""

import streamlit as st
import pandas as pd
from auth import require_login, is_admin
from crud.book_crud import get_all_books, get_book_by_id
from crud.borrow_crud import (
    borrow_book, return_book,
    get_active_borrows_for_member, get_history_for_member,
    get_all_active_borrows
)

st.set_page_config(page_title="Borrow / Return", page_icon="🔄")
require_login()

st.title("🔄 Borrow / Return")

member_id = st.session_state["user_id"]

# ---------- Borrow a book ----------
st.subheader("Borrow a Book")
books = [b for b in get_all_books() if b.available_copies > 0]

if books:
    book_options = {f"{b.title} by {b.author} ({b.available_copies} available)": b.id for b in books}
    selected_label = st.selectbox("Select a book to borrow", list(book_options.keys()))
    if st.button("Borrow"):
        record, msg = borrow_book(member_id, book_options[selected_label])
        if record:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)
else:
    st.info("No books currently available to borrow.")

st.divider()

# ---------- My active borrows / return ----------
st.subheader("My Borrowed Books")
active = get_active_borrows_for_member(member_id)

if active:
    for record in active:
        book = get_book_by_id(record.book_id)
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{book.title}** by {book.author}")
        col2.write(f"Due: {record.due_date.strftime('%Y-%m-%d')}")
        if col3.button("Return", key=f"return_{record.id}"):
            success, msg = return_book(record.id)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
else:
    st.info("You have no borrowed books.")

st.divider()

# ---------- My history ----------
st.subheader("My Borrow History")
history = get_history_for_member(member_id)

if history:
    df = pd.DataFrame([{
        "Book ID": r.book_id,
        "Issued": r.issue_date.strftime("%Y-%m-%d"),
        "Due": r.due_date.strftime("%Y-%m-%d"),
        "Returned": r.return_date.strftime("%Y-%m-%d") if r.return_date else "-",
        "Status": r.status.value,
    } for r in history])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No borrow history yet.")

# ---------- Admin: all active borrows ----------
if is_admin():
    st.divider()
    st.subheader("All Active Borrows (Admin View)")
    all_active = get_all_active_borrows()

    if all_active:
        df = pd.DataFrame([{
            "Record ID": r.id,
            "Book ID": r.book_id,
            "Member ID": r.member_id,
            "Issued": r.issue_date.strftime("%Y-%m-%d"),
            "Due": r.due_date.strftime("%Y-%m-%d"),
        } for r in all_active])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No active borrows system-wide.")
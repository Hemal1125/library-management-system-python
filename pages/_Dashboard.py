"""
pages/5_Dashboard.py
"""

import streamlit as st
import pandas as pd
from collections import Counter
from auth import require_admin
from crud.book_crud import get_all_books
from crud.user_crud import get_all_users
from crud.borrow_crud import get_all_active_borrows
from models import RoleEnum
from database import SessionLocal
from models import BorrowRecord

st.set_page_config(page_title="Dashboard", page_icon="📊")
require_admin()

st.title("📊 Admin Dashboard")

books = get_all_books()
users = get_all_users()
active_borrows = get_all_active_borrows()

total_books = len(books)
total_copies = sum(b.total_copies for b in books)
available_copies = sum(b.available_copies for b in books)
total_members = len([u for u in users if u.role == RoleEnum.member])
total_admins = len([u for u in users if u.role == RoleEnum.admin])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books (titles)", total_books)
col2.metric("Total Copies", total_copies)
col3.metric("Available Copies", available_copies)
col4.metric("Currently Borrowed", total_copies - available_copies)

col5, col6 = st.columns(2)
col5.metric("Total Members", total_members)
col6.metric("Total Admins", total_admins)

st.divider()

st.subheader("Most Borrowed Books")

db = SessionLocal()
try:
    records = db.query(BorrowRecord).all()
finally:
    db.close()

if records:
    book_map = {}
    for b in books:
        book_map[b.id] = b.title

    book_ids_borrowed = []
    for r in records:
        book_ids_borrowed.append(r.book_id)

    counts = Counter(book_ids_borrowed)

    rows = []
    for bid, count in counts.most_common(10):
        book_title = book_map.get(bid, "ID " + str(bid))
        rows.append({"Book": book_title, "Times Borrowed": count})

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No borrow activity yet.")

st.divider()

st.subheader("Currently Active Borrows")

if active_borrows:
    rows = []
    for r in active_borrows:
        rows.append({
            "Record ID": r.id,
            "Book ID": r.book_id,
            "Member ID": r.member_id,
            "Issued": r.issue_date.strftime("%Y-%m-%d"),
            "Due": r.due_date.strftime("%Y-%m-%d"),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No active borrows right now.")
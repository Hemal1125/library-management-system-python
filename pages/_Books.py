"""
pages/2_Books.py
"""

import streamlit as st
import pandas as pd
from auth import require_login, is_admin
from crud.book_crud import (
    add_book, get_all_books, search_books,
    get_book_by_id, update_book, delete_book
)
from utils.validators import is_valid_isbn, is_non_empty

st.set_page_config(page_title="Books", page_icon="📖")
require_login()

st.title("📖 Books")

# ---------- Search ----------
keyword = st.text_input("Search by title, author, or category")
books = search_books(keyword) if keyword else get_all_books()

if books:
    df = pd.DataFrame([{
        "ID": b.id,
        "Title": b.title,
        "Author": b.author,
        "ISBN": b.isbn,
        "Category": b.category,
        "Total": b.total_copies,
        "Available": b.available_copies,
    } for b in books])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No books found.")

# ---------- Admin-only: Add/Edit/Delete ----------
if is_admin():
    st.divider()
    st.subheader("Manage Books")

    tab_add, tab_edit, tab_delete = st.tabs(["➕ Add", "✏️ Edit", "🗑️ Delete"])

    with tab_add:
        with st.form("add_book_form", clear_on_submit=True):
            title = st.text_input("Title")
            author = st.text_input("Author")
            isbn = st.text_input("ISBN")
            category = st.text_input("Category")
            total_copies = st.number_input("Total Copies", min_value=1, value=1)
            submitted = st.form_submit_button("Add Book")

            if submitted:
                if not is_non_empty(title) or not is_non_empty(author):
                    st.error("Title and Author are required.")
                elif not is_valid_isbn(isbn):
                    st.error("ISBN must be 10 or 13 digits (hyphens allowed).")
                else:
                    add_book(title, author, isbn, category, int(total_copies))
                    st.success(f"Book '{title}' added.")
                    st.rerun()

    with tab_edit:
        book_ids = [b.id for b in books]
        if book_ids:
            selected_id = st.selectbox("Select Book ID to edit", book_ids)
            book = get_book_by_id(selected_id)

            if book:
                with st.form("edit_book_form"):
                    title = st.text_input("Title", value=book.title)
                    author = st.text_input("Author", value=book.author)
                    isbn = st.text_input("ISBN", value=book.isbn)
                    category = st.text_input("Category", value=book.category or "")
                    total_copies = st.number_input(
                        "Total Copies", min_value=1, value=book.total_copies
                    )
                    updated = st.form_submit_button("Update Book")

                    if updated:
                        if not is_non_empty(title) or not is_non_empty(author):
                            st.error("Title and Author are required.")
                        elif not is_valid_isbn(isbn):
                            st.error("ISBN must be 10 or 13 digits (hyphens allowed).")
                        else:
                            update_book(
                                selected_id, title, author, isbn, category, int(total_copies)
                            )
                            st.success("Book updated.")
                            st.rerun()
        else:
            st.info("No books to edit.")

    with tab_delete:
        book_ids = [b.id for b in books]
        if book_ids:
            delete_id = st.selectbox("Select Book ID to delete", book_ids, key="del_select")
            if st.button("Delete Book", type="primary"):
                delete_book(delete_id)
                st.success("Book deleted.")
                st.rerun()
        else:
            st.info("No books to delete.")
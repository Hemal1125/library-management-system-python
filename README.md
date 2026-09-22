# Library Management System (Python + Streamlit)

A Python rebuild of a Java/Spring Boot Library Management System, using Streamlit for the UI and MySQL for the database. Built as a learning project to understand full-stack CRUD development in Python.

## Features
- User authentication with hashed passwords (bcrypt)
- Role-based access control (Admin / Member)
- Book management (Add / Edit / Delete / Search) — Admin only
- Browse and search books — all users
- Borrow / Return workflow with available copy tracking
- Member management — Admin only
- Admin dashboard with library statistics

## Tech Stack
- **Language:** Python 3.12
- **Frontend/UI:** Streamlit
- **Backend/ORM:** SQLAlchemy
- **Database:** MySQL
- **Auth:** bcrypt password hashing + Streamlit session state

## Project Structure
```
library_app/
├── Home.py                     # Entry point — landing page + logout
├── database.py                 # MySQL connection setup (SQLAlchemy engine/session)
├── models.py                   # SQLAlchemy models: User, Book, BorrowRecord
├── auth.py                     # Password hashing, login/logout, session state, role checks
├── requirements.txt             # Python dependencies
├── .env                         # DB credentials (not committed)
├── .gitignore
│
├── pages/
│   ├── 1_Login.py               # Login form
│   ├── 2_Books.py               # Book CRUD (Admin) + browse/search (all users)
│   ├── 3_Borrow_Return.py       # Borrow/return workflow
│   ├── 4_Members.py             # Member management (Admin only)
│   └── 5_Dashboard.py           # Library statistics (Admin only)
│
├── crud/
│   ├── book_crud.py             # add/update/delete/list/search books
│   ├── borrow_crud.py           # borrow/return logic, active borrows, history
│   └── user_crud.py             # create/update/delete/list users
│
└── utils/
    └── validators.py            # Email/ISBN/field validation helpers
```
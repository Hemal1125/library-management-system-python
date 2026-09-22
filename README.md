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
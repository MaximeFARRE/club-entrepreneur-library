# Projet Bibli Club

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Streamlit web application to manage a book club's library. It handles book cataloging, borrowing, returning, history tracking, and notifications.

## Features
- **Catalog Management**: View and search the book collection.
- **Book Operations**: Add new books and manage inventory.
- **Borrowing & Returns**: Track who borrowed what and when it is due.
- **History**: Keep a ledger of all past borrowing activity.
- **Notifications**: Automated email reminders for late returns.

## Tech Stack
- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **Database**: SQLite with `peewee` ORM
- **Data Manipulation**: `pandas`
- **Emailing**: `smtplib` / `email`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Projet-bibli-club
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run Accueil.py
```
The application will open in your default web browser at `http://localhost:8501`.

## Repository Structure
```text
.
├── Accueil.py               # Main application entry point
├── assets/                  # Images and static assets
├── data/                    # SQLite database storage (ignored in git)
├── database.py              # Database connection and ORM models
├── email_utils.py           # Email sending utilities
├── notifications.py         # Notification logic
├── pages/                   # Streamlit sub-pages
└── requirements.txt         # Project dependencies
```

## Limitations
- Designed for small to medium book clubs.
- Uses a local SQLite database (not suitable for highly concurrent deployments without modification).

## Contributors
- Maxime FARRE

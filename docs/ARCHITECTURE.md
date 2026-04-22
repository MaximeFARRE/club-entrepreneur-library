# Architecture Overview

The Bibli Club application follows a modular architecture adapted for Streamlit.

## 1. Presentation Layer (UI)
- **Files**: `Accueil.py`, `pages/*.py`
- **Responsibility**: Rendering widgets, handling user inputs, and displaying data.
- **Rule**: Must not contain direct SQL queries or complex data transformations.

## 2. Business Logic Layer
- **Files**: `notifications.py`, `email_utils.py`.
- **Responsibility**: Calculating due dates, checking late returns, and formatting/sending emails.

## 3. Data Access Layer
- **Files**: `database.py`
- **Responsibility**: Defining Peewee ORM models and managing the SQLite connection. Acts as the single source of truth for persistence.

## State Management
Streamlit's `st.session_state` is used for transient UI state. Persistent data is immediately written to the SQLite database via the ORM.

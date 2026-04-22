# Architecture Overview

The application follows a pragmatic 3-tier architecture designed for Streamlit, specifically tailored for the Club Entrepreneur (Pôle Léonard de Vinci) use case.

## 1. Presentation Layer (UI)
- **Files**: `Accueil.py`, `pages/*.py`
- **Responsibility**: Rendering UI components, managing `st.session_state`, and handling user interactions.
- **Constraint**: Must never execute SQL directly or handle complex state transformations.

## 2. Business Logic Layer
- **Files**: `notifications.py`, `email_utils.py`
- **Responsibility**: Orchestrating application rules (e.g., finding overdue books, generating email content).

## 3. Data Access Layer
- **Files**: `database.py`
- **Responsibility**: Connecting to either SQLite or Neon PostgreSQL dynamically. Contains the `PostgresCursorWrapper` to translate SQLite placeholders (`?`) to Postgres placeholders (`%s`). Acts as the sole executor of queries.

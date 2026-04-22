# Agent Operating Manual

Read this file before making any changes to the repository.

## Repository Structure
- **UI Layer**: `Accueil.py` and `pages/*.py`. These files must ONLY contain Streamlit UI code.
- **Data Layer**: `database.py`. Contains Peewee ORM models and database configuration.
- **Services**: `email_utils.py`, `notifications.py`.

## Commands to Run/Test/Build
- **Run App**: `streamlit run Accueil.py`
- **Install Deps**: `pip install -r requirements.txt`

## Engineering Rules
1. **Separation of Concerns**: Do not put database logic or heavy business rules directly inside `pages/*.py`. Call functions from `database.py` or dedicated service modules.
2. **Minimal Changes**: Do not refactor whole files if a small edit is enough.
3. **Database**: Use Peewee ORM for database interactions. Avoid raw SQL strings unless necessary.
4. **Documentation**: Add or update documentation when behavior changes.

## Git Workflow
1. Never work directly on `main`.
2. Create dedicated feature/fix branches (e.g., `feat/add-author-filter`, `fix/borrow-date`).
3. Make small, logical commits using Conventional Commits (`feat: ...`, `fix: ...`, `chore: ...`).
4. Do not batch unrelated changes into a single commit.

## What an Agent Must NEVER Do
- Never commit directly to `main`.
- Never make broad refactors unless explicitly requested.
- Never silently change the architecture.
- Never put business logic in UI files.
- Never invent implementation details without reading the existing code first.

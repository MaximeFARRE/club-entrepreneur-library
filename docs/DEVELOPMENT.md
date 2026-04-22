# Development Guide

## Environment Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and run: `pip install -r requirements.txt`

## Adding a New Page
To add a new feature page to the application:
1. Create a new Python file in the `pages/` directory.
2. Prefix it with the next logical number (e.g., `07_Statistiques.py`).
3. Streamlit will automatically detect and add it to the sidebar.

## Managing the Database
The project uses SQLite and the Peewee ORM.
- The database file is located at `data/bibliotheque.db`.
- Schema modifications should be done by updating the models in `database.py`.

## Local Secrets
For features like email notifications, do not hardcode credentials. Use Streamlit's secrets management by placing your configurations in `.streamlit/secrets.toml` (this file is git-ignored).

## Neon PostgreSQL Setup
To connect to a Neon database instead of local SQLite, add the following to your `.streamlit/secrets.toml`:

```toml
DATABASE_URL = "postgresql://user:password@ep-cool-pine-123456.eu-central-1.aws.neon.tech/dbname"
```

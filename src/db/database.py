import sqlite3
import os
import streamlit as st
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extras import DictCursor
except ImportError:
    psycopg2 = None

DB_PATH = Path("data") / "bibliotheque.db"

def get_database_url():
    """Check Streamlit secrets then environment for DATABASE_URL."""
    try:
        if "DATABASE_URL" in st.secrets:
            return st.secrets["DATABASE_URL"]
    except Exception:
        pass
    return os.environ.get("DATABASE_URL")

DB_URL = get_database_url()
IS_POSTGRES = DB_URL is not None and DB_URL.startswith("postgres")

class PostgresCursorWrapper:
    """Wraps psycopg2 cursor to mimic sqlite3 behavior (e.g. ? placeholders)"""
    def __init__(self, cur):
        self.cur = cur

    def execute(self, query, vars=None):
        pg_query = query.replace("?", "%s")
        if vars is None:
            return self.cur.execute(pg_query)
        return self.cur.execute(pg_query, vars)

    def fetchall(self):
        return self.cur.fetchall()

    def fetchone(self):
        return self.cur.fetchone()

class PostgresConnWrapper:
    """Wraps psycopg2 connection to provide our custom cursor"""
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return PostgresCursorWrapper(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

# --- Connection helper ---
def get_connection():
    """Create the DB if needed and return a connection."""
    if IS_POSTGRES:
        if psycopg2 is None:
            raise ImportError("psycopg2-binary is required for PostgreSQL.")
        conn = psycopg2.connect(DB_URL, cursor_factory=DictCursor)
        return PostgresConnWrapper(conn)
    else:
        DB_PATH.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

# --- Initialize DB ---
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    if IS_POSTGRES:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                id SERIAL PRIMARY KEY,
                titre TEXT NOT NULL,
                auteur TEXT,
                categorie TEXT,
                proprietaire TEXT,
                proprietaire_email TEXT,
                disponibilite TEXT DEFAULT 'Disponible',
                emprunte_par TEXT,
                resume TEXT,
                couverture TEXT,
                date_ajout TEXT
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historique (
                id SERIAL PRIMARY KEY,
                id_livre INTEGER NOT NULL REFERENCES livres(id),
                emprunteur TEXT NOT NULL,
                emprunteur_email TEXT,
                date_emprunt TEXT NOT NULL,
                date_retour_prevue TEXT NOT NULL,
                date_retour TEXT,
                commentaire TEXT
            );
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT,
                categorie TEXT,
                proprietaire TEXT,
                proprietaire_email TEXT,
                disponibilite TEXT DEFAULT 'Disponible',
                emprunte_par TEXT,
                resume TEXT,
                couverture TEXT,
                date_ajout TEXT
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historique (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_livre INTEGER NOT NULL,
                emprunteur TEXT NOT NULL,
                emprunteur_email TEXT,
                date_emprunt TEXT NOT NULL,
                date_retour_prevue TEXT NOT NULL,
                date_retour TEXT,
                commentaire TEXT,
                FOREIGN KEY (id_livre) REFERENCES livres(id)
            );
        """)

    conn.commit()
    conn.close()

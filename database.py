import sqlite3
import os
import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta

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
        # Translate SQLite ? to Postgres %s
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
        # Table des livres
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
        # Table historique des emprunts
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


# --- Add a book ---
def ajouter_livre(titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture):
    conn = get_connection()
    cur = conn.cursor()
    date_ajout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO livres (titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture, date_ajout)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture, date_ajout))

    conn.commit()
    conn.close()


# --- Get all books ---
def get_livres():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM livres ORDER BY titre ASC")
    rows = cur.fetchall()

    conn.close()
    return rows


# --- Emprunter un livre ---
def emprunter_livre(id_livre, emprunteur, emprunteur_email, commentaire=""):
    conn = get_connection()
    cur = conn.cursor()

    date_emprunt = datetime.now()
    date_emprunt_str = date_emprunt.strftime("%Y-%m-%d %H:%M:%S")
    date_retour_prevue = (date_emprunt + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    # Mise à jour du livre
    cur.execute("""
        UPDATE livres
        SET disponibilite = 'Indisponible', emprunte_par = ?
        WHERE id = ?
    """, (emprunteur, id_livre))

    # Ajout dans l'historique
    cur.execute("""
        INSERT INTO historique (id_livre, emprunteur, emprunteur_email, date_emprunt, date_retour_prevue, commentaire)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_livre, emprunteur, emprunteur_email, date_emprunt_str, date_retour_prevue, commentaire))

    conn.commit()
    conn.close()

    # On renvoie les dates pour les emails
    return date_emprunt_str, date_retour_prevue
     

# --- Rendre un livre ---
def rendre_livre(id_livre, commentaire=""):
    conn = get_connection()
    cur = conn.cursor()

    date_retour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Remettre disponible
    cur.execute("""
        UPDATE livres
        SET disponibilite = 'Disponible', emprunte_par = NULL
        WHERE id = ?
    """, (id_livre,))

    # Compléter l’historique (dernier emprunt du livre)
    cur.execute("""
        UPDATE historique
        SET date_retour = ?, commentaire = ?
        WHERE id_livre = ? AND date_retour IS NULL
    """, (date_retour, commentaire, id_livre))

    conn.commit()
    conn.close()


# --- Historique complet ---
def get_historique():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT h.*, l.titre, l.proprietaire, l.proprietaire_email
        FROM historique h
        JOIN livres l ON l.id = h.id_livre
        ORDER BY date_emprunt DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


# --- Récupérer un livre par id ---
def get_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM livres WHERE id = ?", (id_livre,))
    row = cur.fetchone()
    conn.close()
    return row


# --- Mettre à jour un livre ---
def mettre_a_jour_livre(id_livre, titre, auteur, categorie, proprietaire, resume, couverture, disponibilite, emprunte_par):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE livres
        SET titre = ?,
            auteur = ?,
            categorie = ?,
            proprietaire = ?,
            resume = ?,
            couverture = ?,
            disponibilite = ?,
            emprunte_par = ?
        WHERE id = ?
    """, (titre, auteur, categorie, proprietaire, resume, couverture,
          disponibilite, emprunte_par, id_livre))

    conn.commit()
    conn.close()


# --- Supprimer un livre (et son historique associé) ---
def supprimer_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()

    # On supprime d'abord l'historique lié à ce livre
    cur.execute("DELETE FROM historique WHERE id_livre = ?", (id_livre,))
    # Puis le livre lui-même
    cur.execute("DELETE FROM livres WHERE id = ?", (id_livre,))

    conn.commit()
    conn.close()


def archiver_livre(id_livre: int):
    """Marque un livre comme archivé (il n'apparaîtra plus dans l'app)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE livres
        SET disponibilite = 'Archivé',
            emprunte_par = NULL
        WHERE id = ?
        """,
        (id_livre,),
    )

    conn.commit()
    conn.close()


def get_dernier_emprunt(id_livre: int):
    """
    Retourne le dernier emprunt d'un livre (ou None s'il n'y en a pas).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT h.*, l.titre, l.proprietaire, l.proprietaire_email
        FROM historique h
        JOIN livres l ON l.id = h.id_livre
        WHERE h.id_livre = ?
        ORDER BY h.date_emprunt DESC
        LIMIT 1
    """, (id_livre,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)

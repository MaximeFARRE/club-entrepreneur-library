from src.db.database import get_connection
from datetime import datetime

def get_livres():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM livres ORDER BY titre ASC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM livres WHERE id = ?", (id_livre,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

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

def archiver_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE livres
        SET disponibilite = 'Archivé',
            emprunte_par = NULL
        WHERE id = ?
    """, (id_livre,))
    conn.commit()
    conn.close()

def supprimer_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM livres WHERE id = ?", (id_livre,))
    conn.commit()
    conn.close()

def update_disponibilite(id_livre: int, disponibilite: str, emprunte_par: str = None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE livres
        SET disponibilite = ?, emprunte_par = ?
        WHERE id = ?
    """, (disponibilite, emprunte_par, id_livre))
    conn.commit()
    conn.close()

from src.db.database import get_connection

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
    return [dict(r) for r in rows]

def get_dernier_emprunt(id_livre: int):
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
    return dict(row) if row else None

def get_emprunt_en_cours(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT h.*, l.titre, l.proprietaire, l.proprietaire_email
        FROM historique h
        JOIN livres l ON l.id = h.id_livre
        WHERE h.id_livre = ? AND h.date_retour IS NULL
        ORDER BY h.date_emprunt DESC
        LIMIT 1
    """, (id_livre,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def ajouter_emprunt(id_livre: int, emprunteur: str, emprunteur_email: str, date_emprunt: str, date_retour_prevue: str, commentaire: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO historique (id_livre, emprunteur, emprunteur_email, date_emprunt, date_retour_prevue, commentaire)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_livre, emprunteur, emprunteur_email, date_emprunt, date_retour_prevue, commentaire))
    conn.commit()
    conn.close()

def cloturer_emprunt(id_livre: int, date_retour: str, commentaire: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE historique
        SET date_retour = ?, commentaire = ?
        WHERE id_livre = ? AND date_retour IS NULL
    """, (date_retour, commentaire, id_livre))
    conn.commit()
    conn.close()

def supprimer_historique_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM historique WHERE id_livre = ?", (id_livre,))
    conn.commit()
    conn.close()

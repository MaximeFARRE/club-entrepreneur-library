import streamlit as st
from src.db.database import init_db
from src.services.livre_service import get_tous_les_livres
from src.services.emprunt_service import get_tout_historique, get_emprunts_en_retard
from pathlib import Path

# Charger et afficher le logo
logo_path = Path("assets/logo.png")

if logo_path.exists():
    st.image(str(logo_path), width=200)

# Configuration de la page principale
st.set_page_config(
    page_title="Bibliothèque du Club Entrepreneurs",
    page_icon="assets/logo_icone.png",
    layout="wide"
)

# Initialisation de la base de données
init_db()

# Titre principal
st.title("Bibliothèque du Club Entrepreneurs")

# Introduction
st.markdown("""
Bienvenue sur la plateforme de gestion et de partage des livres du Club Entrepreneurs.

Cet outil a été conçu pour permettre aux membres du club de :
- consulter les ouvrages disponibles ;
- ajouter facilement leurs propres livres à la bibliothèque commune ;
- emprunter et rendre des ouvrages en quelques secondes ;
- suivre l’historique des emprunts.

Utilisez le menu situé à gauche pour accéder aux différentes sections de l’application : 
le catalogue, l’ajout de livre, la gestion des emprunts et l’historique.
""")

# Séparateur
st.markdown("---")

# Section complémentaire (optionnelle)
st.markdown("""
### À propos du projet

Cette plateforme a été développée pour encourager le partage de connaissances
et faciliter l’accès à des ressources utiles en entrepreneuriat, management,
développement personnel et domaines associés.  
N’hésitez pas à contribuer en ajoutant vos livres ou en partageant vos retours.
""")
st.markdown("Bonne lecture à tous ! ")

# --- Statistiques de la bibliothèque ---

livres_rows = get_tous_les_livres()
livres = [dict(row) for row in livres_rows]

total_livres = len(livres)
nb_disponibles = sum(1 for l in livres if l.get("disponibilite") == "Disponible")
nb_empruntes = sum(1 for l in livres if l.get("disponibilite") == "Indisponible")
nb_archives = sum(1 for l in livres if l.get("disponibilite") == "Archivé")

historique_rows = get_tout_historique()
historique = [dict(r) for r in historique_rows]
total_emprunts = len(historique)

retards = get_emprunts_en_retard()
nb_retards = len(retards)

# Nombre de livres différents ayant déjà été empruntés
livres_empruntes_distincts = len({h.get("id_livre") for h in historique}) if historique else 0

st.subheader("Statistiques de la bibliothèque")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Livres au total", total_livres)
    st.metric("Déjà empruntés", livres_empruntes_distincts)

with col2:
    st.metric("Disponibles", nb_disponibles)
    st.metric("Actuellement empruntés", nb_empruntes)

with col3:
    st.metric("Livres archivés", nb_archives)
    st.metric("Emprunts au total", total_emprunts)
    
with col4:
    st.metric("Livres en retard", nb_retards, delta="-Attention" if nb_retards > 0 else "OK", delta_color="inverse")

st.markdown("---")
st.markdown("© 2025 Club Entrepreneurs - Tous droits réservés.")

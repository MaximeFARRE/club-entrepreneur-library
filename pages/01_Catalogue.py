import streamlit as st
import pandas as pd

from src.services.livre_service import get_tous_les_livres
from src.services.emprunt_service import process_emprunt

st.set_page_config(page_title="Catalogue", layout="wide", page_icon="assets/logo_icone.png")

st.title("Catalogue des livres")

st.write(
    "Retrouve ici tous les livres disponibles dans la bibliothèque du Club Entrepreneurs. "
    "Utilise les filtres ci-dessous pour trouver rapidement ce que tu cherches."
)

# -----------------------------
# Récupération des données
# -----------------------------
rows = get_tous_les_livres()
livres = [dict(r) for r in rows]

if "selected_book_id" not in st.session_state:
    st.session_state["selected_book_id"] = None

# -----------------------------
# Barre de recherche & filtres
# -----------------------------
with st.container():
    col_search, col_cat = st.columns([2, 1])

    with col_search:
        query = st.text_input(
            "Recherche (titre, auteur, catégorie)",
            placeholder="Ex : mindset, investissement, Brian Tracy..."
        ).strip().lower()

    # Catégories possibles
    categories = sorted({l.get("categorie", "") for l in livres if l.get("categorie")})
    with col_cat:
        categorie_filtre = st.multiselect(
            "Catégorie",
            options=categories,
            default=[]
        )

    filtre_dispo = st.segmented_control(
        "Filtres rapides",
        options=["Tous", "Disponibles", "Empruntés", "Archivés"],
        default="Tous",
        selection_mode="single"
    )
    # Au cas où l'utilisateur décoche le bouton sélectionné
    if not filtre_dispo:
        filtre_dispo = "Tous"

# -----------------------------
# Filtrage des livres
# -----------------------------
livres_filtres = []

for l in livres:
    titre = (l.get("titre") or "").lower()
    auteur = (l.get("auteur") or "").lower()
    categorie = (l.get("categorie") or "").lower()
    dispo = l.get("disponibilite") or "Disponible"

    # Filtre texte
    if query:
        texte = " ".join([titre, auteur, categorie])
        if query not in texte:
            continue

    # Filtre catégorie
    if categorie_filtre and l.get("categorie") not in categorie_filtre:
        continue

    # Filtre dispo
    if filtre_dispo == "Disponibles" and dispo != "Disponible":
        continue
    if filtre_dispo == "Empruntés" and dispo != "Indisponible":
        continue
    if filtre_dispo == "Archivés" and dispo != "Archivé":
        continue

    livres_filtres.append(l)

st.markdown("---")
st.subheader(f"Livres trouvés : {len(livres_filtres)}")

if not livres_filtres:
    st.info("Aucun livre ne correspond à ta recherche pour l’instant.")
    st.stop()

# -----------------------------
# Fonction utilitaire : badge de disponibilité
# -----------------------------
def badge_disponibilite(dispo: str) -> str:
    dispo = dispo or "Disponible"
    if dispo == "Disponible":
        color = "#1B8C3B"
        label = "Disponible"
    elif dispo == "Indisponible":
        color = "#D99A1B"
        label = "Emprunté"
    else:
        color = "#555555"
        label = "Archivé"
    return f"<span style='background-color:{color}; padding:2px 8px; border-radius:999px; font-size:0.7rem;'>{label}</span>"

# -----------------------------
# Affichage des cartes
# -----------------------------
st.write("Clique sur « Voir le détail » pour afficher toutes les informations sur un livre.")

NB_COLS = 3  # nombre de cartes par ligne

for start in range(0, len(livres_filtres), NB_COLS):
    cols = st.columns(NB_COLS)
    slice_livres = livres_filtres[start:start + NB_COLS]

    for col, livre in zip(cols, slice_livres):
        with col:
            titre = livre.get("titre") or "Sans titre"
            auteur = livre.get("auteur") or "Auteur inconnu"
            categorie = livre.get("categorie") or "Sans catégorie"
            proprietaire = livre.get("proprietaire") or "Inconnu"
            dispo = livre.get("disponibilite") or "Disponible"

            st.markdown(
                f"""
                <div style="
                    border:1px solid #444;
                    border-radius:10px;
                    padding:0.8rem 0.9rem;
                    margin-bottom:0.8rem;
                    background-color:#1E1E1E;
                    min-height: 150px;
                ">
                    <div style="font-weight:600; font-size:1.05rem; margin-bottom:0.2rem;">
                        {titre}
                    </div>
                    <div style="color:#bbbbbb; font-size:0.9rem; margin-bottom:0.4rem;">
                        {auteur}
                    </div>
                    <div style="margin-bottom:0.3rem;">
                        <span style="
                            background-color:#273B70;
                            padding:2px 8px;
                            border-radius:999px;
                            font-size:0.7rem;
                            margin-right:4px;
                        ">{categorie}</span>
                        {badge_disponibilite(dispo)}
                    </div>
                    <div style="color:#aaaaaa; font-size:0.8rem;">
                        Propriétaire : {proprietaire}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Voir le détail", key=f"detail_{livre['id']}"):
                st.session_state["selected_book_id"] = livre["id"]

# -----------------------------
# Panneau de détail
# -----------------------------
st.markdown("---")
st.subheader("Détail du livre sélectionné")

selected_id = st.session_state.get("selected_book_id")

if selected_id is None:
    st.info("Clique sur « Voir le détail » sur un livre du catalogue pour afficher toutes les informations ici.")
else:
    livre_sel = next((l for l in livres if l["id"] == selected_id), None)

    if livre_sel is None:
        st.info("Le livre sélectionné n’existe plus dans le catalogue.")
    else:
        titre = livre_sel.get("titre") or "Sans titre"
        auteur = livre_sel.get("auteur") or "Auteur inconnu"
        categorie = livre_sel.get("categorie") or "Sans catégorie"
        proprietaire = livre_sel.get("proprietaire") or "Inconnu"
        proprietaire_email = livre_sel.get("proprietaire_email") or "Non renseigné"
        dispo = livre_sel.get("disponibilite") or "Disponible"
        resume = livre_sel.get("resume") or "Pas de résumé renseigné pour le moment."
        couverture = livre_sel.get("couverture") or None
        date_ajout = livre_sel.get("date_ajout") or "Date inconnue"

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.markdown(f"### {titre}")
            st.markdown(f"**Auteur :** {auteur}")
            st.markdown(f"**Catégorie :** {categorie}")
            st.markdown(f"**Propriétaire :** {proprietaire}")
            st.markdown(f"**Email du propriétaire :** {proprietaire_email}")
            st.markdown(f"**Disponibilité :** {dispo}")
            st.markdown(f"**Ajouté le :** {date_ajout}")
            st.markdown("**Résumé :**")
            st.write(resume)

        with col_right:
            if couverture:
                st.image(couverture, use_column_width=True)
            else:
                st.info("Aucune couverture fournie pour ce livre.")

        # ---------- Formulaire d'emprunt directement depuis la fiche ----------
        st.markdown("---")
        st.markdown("### Emprunter ce livre")

        if dispo != "Disponible":
            st.info("Ce livre n'est actuellement pas disponible à l’emprunt.")
        else:
            with st.form(f"form_emprunt_{selected_id}"):
                emprunteur = st.text_input("Ton nom")
                emprunteur_email = st.text_input("Ton email (ex : prenom.nom@edu.devinci.fr)")
                commentaire = st.text_area("Commentaire (optionnel)", height=80)

                submit_emprunt = st.form_submit_button("Emprunter ce livre")

            if submit_emprunt:
                if not emprunteur or not emprunteur_email:
                    st.error("Merci de renseigner ton nom et ton email pour emprunter le livre.")
                else:
                    try:
                        process_emprunt(selected_id, emprunteur, emprunteur_email, commentaire)
                        st.success("Le livre a bien été emprunté. Tu as un mois pour le rendre.")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))

# -----------------------------
# Vue tableau "backup" du catalogue
# -----------------------------
st.markdown("---")
st.subheader("Vue tableau du catalogue (backup)")

try:
    df_backup = pd.DataFrame(livres_filtres)[
        ["titre", "auteur", "categorie", "proprietaire", "disponibilite", "emprunte_par"]
    ].rename(
        columns={
            "titre": "Titre",
            "auteur": "Auteur",
            "categorie": "Catégorie",
            "proprietaire": "Propriétaire",
            "disponibilite": "Disponibilité",
            "emprunte_par": "Emprunté par",
        }
    )
except KeyError:
    # Si jamais certaines colonnes n'existent pas (sécurité)
    df_backup = pd.DataFrame(livres_filtres)

st.dataframe(df_backup, use_container_width=True)
st.markdown(
    "_Remarque : cette vue tableau est principalement destinée à des fins de sauvegarde et de vérification. "
    "Pour une expérience utilisateur optimale, utilise les cartes de la section principale du catalogue._"
)
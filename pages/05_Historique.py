import streamlit as st
from src.services.emprunt_service import get_tout_historique as get_historique

st.set_page_config(page_title="Historique des emprunts", page_icon="assets/logo_icone.png",
)

st.title("Historique des emprunts")
st.write("Voici l'historique complet des emprunts/rendus de la bibliothèque du club.")


rows = get_historique()

if not rows:
    st.info("Aucun emprunt enregistré pour le moment.")
else:
    historique = [dict(r) for r in rows]

    # Filtres
    st.sidebar.header("Filtres")

    # Liste unique des titres et des emprunteurs
    titres = sorted({h["titre"] for h in historique if h.get("titre")})
    emprunteurs = sorted({h["emprunteur"] for h in historique if h.get("emprunteur")})

    titre_filtre = st.sidebar.selectbox(
        "Livre",
        options=["Tous"] + titres if titres else ["Tous"]
    )

    emprunteur_filtre = st.sidebar.selectbox(
        "Emprunteur",
        options=["Tous"] + emprunteurs if emprunteurs else ["Tous"]
    )

    statut_filtre = st.sidebar.selectbox(
        "Statut",
        options=["Tous", "En cours", "Rendu"]
    )

    # Application des filtres
    data = historique

    if titre_filtre != "Tous":
        data = [h for h in data if h.get("titre") == titre_filtre]

    if emprunteur_filtre != "Tous":
        data = [h for h in data if h.get("emprunteur") == emprunteur_filtre]

    if statut_filtre != "Tous":
        if statut_filtre == "En cours":
            data = [h for h in data if h.get("date_retour") is None]
        else:  # "Rendu"
            data = [h for h in data if h.get("date_retour") is not None]

    st.subheader(f"Lignes trouvées : {len(data)}")

    # On adapte un peu les colonnes pour l’affichage
    tableau_affiche = []
    for h in data:
        tableau_affiche.append({
            "Titre": h.get("titre"),
            "Emprunteur": h.get("emprunteur"),
            "Date d'emprunt": h.get("date_emprunt"),
            "Date de retour": h.get("date_retour") or "—",
            "Commentaire": h.get("commentaire") or ""
        })

    st.dataframe(tableau_affiche, use_container_width=True)

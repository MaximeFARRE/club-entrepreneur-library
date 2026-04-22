import streamlit as st
from src.services.livre_service import get_tous_les_livres as get_livres, get_livre, mettre_a_jour_livre, archiver_livre


st.set_page_config(page_title="Gérer les livres",  page_icon="assets/logo_icone.png",
)

st.title("Gestion des livres")
st.write("Modifier les informations d'un livre existant ou le supprimer de la bibliothèque.")


# --- Récupération des livres ---
livres_rows = get_livres()
livres = [dict(row) for row in livres_rows]

if not livres:
    st.info("Aucun livre dans la base pour le moment.")
else:
    # Sélection du livre à gérer
    options = [f"{l['id']} - {l['titre']}" for l in livres]
    selection = st.selectbox("Choisir un livre à modifier / supprimer", options=options)

    id_livre = int(selection.split(" - ")[0])
    livre_row = get_livre(id_livre)

    if livre_row is None:
        st.error("Livre introuvable.")
    else:
        livre = dict(livre_row)

        st.subheader("Modifier les informations du livre")

        with st.form("form_edit_livre"):
            titre = st.text_input("Titre", value=livre.get("titre") or "")
            auteur = st.text_input("Auteur", value=livre.get("auteur") or "")
            categorie = st.text_input("Catégorie", value=livre.get("categorie") or "")
            proprietaire = st.text_input("Propriétaire", value=livre.get("proprietaire") or "")
            resume = st.text_area("Résumé", value=livre.get("resume") or "")
            couverture = st.text_input("URL de couverture", value=livre.get("couverture") or "")

            disponibilite = st.selectbox(
                "Disponibilité",
                ["Disponible", "Indisponible"],
                index=0 if livre.get("disponibilite") == "Disponible" else 1
            )

            emprunte_par = st.text_input("Emprunté par", value=livre.get("emprunte_par") or "")

            submit_modif = st.form_submit_button("Enregistrer les modifications")

        if submit_modif:
            if not titre or not proprietaire:
                st.error("Le titre et le propriétaire sont obligatoires.")
            else:
                mettre_a_jour_livre(
                    id_livre,
                    titre,
                    auteur,
                    categorie,
                    proprietaire,
                    resume,
                    couverture,
                    disponibilite,
                    emprunte_par if emprunte_par.strip() else None
                )
                st.success("Les informations du livre ont été mises à jour.")

        st.markdown("---")
        st.subheader("Archivage du livre")

        st.info(
            "Archiver un livre le retire du catalogue et de la liste d'emprunt, "
            "mais les données restent dans la base et l'historique des emprunts est conservé."
        )

        if st.button("Archiver ce livre"):
            archiver_livre(id_livre)
            st.success("Le livre a été archivé.")
            st.stop()

import streamlit as st
from src.services.livre_service import get_tous_les_livres
from src.services.emprunt_service import process_emprunt

st.set_page_config(page_title="Emprunter un livre",    page_icon="assets/logo_icone.png",
)



st.title("Emprunter un livre")
st.write("Sélectionne un livre disponible ci-dessous pour l’emprunter.")

livres_rows = get_tous_les_livres()
livres = [dict(row) for row in livres_rows]

livres_dispos = [l for l in livres if l["disponibilite"] == "Disponible"]

if not livres_dispos:
    st.info("Aucun livre disponible pour le moment.")
else:
    # Map id -> livre
    livres_par_id = {l["id"]: l for l in livres_dispos}

    options = [f"{l['id']} - {l['titre']} (par {l['auteur']})" for l in livres_dispos]
    selection = st.selectbox("Choisir un livre", options=options)

    emprunteur = st.text_input("Ton nom")
    emprunteur_email = st.text_input("Ton email (ex : prenom.nom@edu-devinci.fr)")
    commentaire = st.text_area("Commentaire (optionnel)")

    if st.button("Emprunter ce livre"):
        if not emprunteur or not emprunteur_email:
            st.error("Merci d’indiquer ton nom et ton email.")
        else:
            id_livre = int(selection.split(" - ")[0])
            livre = livres_par_id[id_livre]

            try:
                process_emprunt(id_livre, emprunteur, emprunteur_email, commentaire)
                st.success("Le livre a bien été emprunté. Tu as un mois pour le rendre.")
            except ValueError as e:
                st.error(str(e))

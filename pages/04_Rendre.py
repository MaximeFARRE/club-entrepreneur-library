import streamlit as st
from src.services.livre_service import get_tous_les_livres
from src.services.emprunt_service import process_retour

st.set_page_config(page_title="Rendre un livre",    page_icon="assets/logo_icone.png",)



st.title("Rendre un livre")
st.write("Sélectionne un livre actuellement emprunté pour le marquer comme rendu.")

livres_rows = get_tous_les_livres()
livres = [dict(row) for row in livres_rows]

livres_empruntes = [l for l in livres if l["disponibilite"] == "Indisponible"]

if not livres_empruntes:
    st.info("Aucun livre n'est actuellement enregistré comme emprunté.")
else:
    livres_par_id = {l["id"]: l for l in livres_empruntes}

    selection = st.selectbox(
        "Livre à rendre",
        options=[f"{l['id']} - {l['titre']} (emprunté par {l['emprunte_par']})" for l in livres_empruntes]
    )

    commentaire = st.text_area("Commentaire (optionnel, état du livre, remarques, etc.)")

    if st.button("Marquer comme rendu"):
        id_livre = int(selection.split(" - ")[0])

        try:
            process_retour(id_livre, commentaire)
            st.success("Le livre a bien été marqué comme rendu.")
        except ValueError as e:
            st.error(str(e))

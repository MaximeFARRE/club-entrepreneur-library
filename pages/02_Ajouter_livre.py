import streamlit as st
from src.services.livre_service import ajouter_nouveau_livre

st.set_page_config(page_title="Ajouter un livre",    page_icon="assets/logo_icone.png",
)

st.title("Ajouter un livre")
st.write("Remplis les informations ci-dessous pour ajouter un livre à la bibliothèque du club.")

with st.form("ajout_livre_form"):

    titre = st.text_input("Titre du livre")
    auteur = st.text_input("Auteur")
    categorie = st.selectbox(
        "Catégorie",
        ["Business", "Mindset", "Finance", "Marketing", "Management", "Développement personnel", "Autre"]
    )
    proprietaire = st.text_input("Propriétaire (ton nom)")
    proprietaire_email = st.text_input("Email DeVinci du propriétaire")
    resume = st.text_area("Résumé (optionnel)")
    couverture = st.text_input("URL de couverture (optionnel)")

    submitted = st.form_submit_button("Ajouter le livre")

    if submitted:
        if not titre or not proprietaire or not proprietaire_email:
            st.error("Le titre, le propriétaire et l'email du propriétaire sont obligatoires.")
        else:
            # Optionnel : vérifier le domaine
            if not proprietaire_email.endswith("@edu.devinci.fr"):
                 st.error("Merci d'utiliser ton email de l'école (@edu.devinci.fr).")
            else:
                ajouter_nouveau_livre(titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture)
                st.success(f"Le livre **{titre}** a été ajouté avec succès.")

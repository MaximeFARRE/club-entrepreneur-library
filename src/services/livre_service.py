from src.repositories import livre_repository, historique_repository

def get_tous_les_livres():
    return livre_repository.get_livres()

def get_livre(id_livre: int):
    return livre_repository.get_livre(id_livre)

def ajouter_nouveau_livre(titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture):
    livre_repository.ajouter_livre(titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture)

def mettre_a_jour_livre(id_livre, titre, auteur, categorie, proprietaire, resume, couverture, disponibilite, emprunte_par):
    livre_repository.mettre_a_jour_livre(id_livre, titre, auteur, categorie, proprietaire, resume, couverture, disponibilite, emprunte_par)

def archiver_livre(id_livre: int):
    livre_repository.archiver_livre(id_livre)

def supprimer_livre_et_historique(id_livre: int):
    historique_repository.supprimer_historique_livre(id_livre)
    livre_repository.supprimer_livre(id_livre)

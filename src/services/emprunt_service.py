from datetime import datetime, timedelta
from src.repositories import livre_repository, historique_repository
from src.services import notification_service

def process_emprunt(id_livre: int, emprunteur: str, emprunteur_email: str, commentaire: str = ""):
    date_emprunt = datetime.now()
    date_emprunt_str = date_emprunt.strftime("%Y-%m-%d %H:%M:%S")
    date_retour_prevue = (date_emprunt + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    livre = livre_repository.get_livre(id_livre)
    if not livre:
        raise ValueError("Livre introuvable.")
    if livre['disponibilite'] != "Disponible":
        raise ValueError("Ce livre n'est pas disponible.")

    livre_repository.update_disponibilite(id_livre, "Indisponible", emprunteur)
    historique_repository.ajouter_emprunt(id_livre, emprunteur, emprunteur_email, date_emprunt_str, date_retour_prevue, commentaire)

    titre = livre.get("titre", "Titre inconnu")
    proprietaire = livre.get("proprietaire", "un membre du club")
    proprietaire_email = livre.get("proprietaire_email", "")

    # Emails (Failures are ignored so they don't break the borrowing flow)
    try:
        notification_service.envoyer_mail_emprunt_proprietaire(
            proprietaire, proprietaire_email, emprunteur, emprunteur_email, titre, date_emprunt_str, date_retour_prevue
        )
    except Exception as e:
        print(f"Erreur envoi email propriétaire : {e}")

    try:
        notification_service.envoyer_mail_emprunt_emprunteur(
            proprietaire, proprietaire_email, emprunteur, emprunteur_email, titre, date_emprunt_str, date_retour_prevue
        )
    except Exception as e:
        print(f"Erreur envoi email emprunteur : {e}")

def process_retour(id_livre: int, commentaire: str = ""):
    livre = livre_repository.get_livre(id_livre)
    if not livre:
        raise ValueError("Livre introuvable.")

    dernier_emprunt = historique_repository.get_dernier_emprunt(id_livre)
    
    date_retour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    livre_repository.update_disponibilite(id_livre, "Disponible", None)
    historique_repository.cloturer_emprunt(id_livre, date_retour, commentaire)

    if dernier_emprunt:
        titre = dernier_emprunt.get("titre", "Titre inconnu")
        proprietaire = dernier_emprunt.get("proprietaire", "un membre du club")
        proprietaire_email = dernier_emprunt.get("proprietaire_email", "")
        emprunteur = dernier_emprunt.get("emprunteur", "Inconnu")
        emprunteur_email = dernier_emprunt.get("emprunteur_email", "")
        date_emprunt = dernier_emprunt.get("date_emprunt", "")
        date_retour_prevue = dernier_emprunt.get("date_retour_prevue", "")

        try:
            notification_service.envoyer_mail_retour_proprietaire(
                proprietaire, proprietaire_email, emprunteur, emprunteur_email, titre, date_emprunt, date_retour_prevue, date_retour
            )
        except Exception as e:
            print(f"Erreur envoi email propriétaire : {e}")
            
        try:
            notification_service.envoyer_mail_retour_emprunteur(
                proprietaire, proprietaire_email, emprunteur, emprunteur_email, titre, date_emprunt, date_retour_prevue, date_retour
            )
        except Exception as e:
            print(f"Erreur envoi email emprunteur : {e}")

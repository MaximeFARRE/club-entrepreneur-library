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


def get_tout_historique():
    return historique_repository.get_historique()

def get_emprunts_en_retard():
    """
    Retourne la liste des emprunts actuellement en retard,
    avec le nombre de jours de retard calculé.
    """
    historique = get_tout_historique()
    maintenant = datetime.now()
    retards = []
    
    for emprunt in historique:
        if emprunt.get("date_retour") is None: # L'emprunt est toujours en cours
            date_prevue_str = emprunt.get("date_retour_prevue")
            if date_prevue_str:
                try:
                    date_prevue = datetime.strptime(date_prevue_str, "%Y-%m-%d %H:%M:%S")
                    if maintenant > date_prevue:
                        jours_retard = (maintenant - date_prevue).days
                        emprunt["jours_retard"] = jours_retard
                        retards.append(emprunt)
                except ValueError:
                    continue
                    
    # Trier par nombre de jours de retard (le plus long en premier)
    retards.sort(key=lambda x: x.get("jours_retard", 0), reverse=True)
    return retards

def get_emprunt_actif_pour_livre(id_livre: int):
    """Retourne l'emprunt en cours pour un livre donné, ou None s'il n'y en a pas."""
    return historique_repository.get_emprunt_en_cours(id_livre)

def determiner_statut_couleur(date_retour: str, date_retour_prevue: str) -> str:
    """
    Détermine la couleur du statut d'un emprunt.
    - Vert (🟢) : si rendu, ou s'il reste plus de 3 jours.
    - Orange (🟠) : si en cours et qu'il reste moins de 3 jours (inclus).
    - Rouge (🔴) : si en retard.
    """
    if date_retour:
        return "🟢" # Rendu
        
    if not date_retour_prevue:
        return "🟢" # Pas de date prévue, par défaut OK
        
    maintenant = datetime.now()
    try:
        date_prevue = datetime.strptime(date_retour_prevue, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return "🟢"
        
    if maintenant > date_prevue:
        return "🔴" # En retard
        
    jours_restants = (date_prevue - maintenant).days
    if jours_restants <= 3:
        return "🟠" # Bientôt à rendre
        
    return "🟢" # Reste plus de 3 jours

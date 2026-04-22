import pytest
from src.services import livre_service

def test_ajouter_nouveau_livre(mocker):
    # Setup mock for the repository
    mock_ajouter = mocker.patch('src.repositories.livre_repository.ajouter_livre')
    
    # Execute service
    livre_service.ajouter_nouveau_livre(
        "Titre Test", "Auteur Test", "Business", 
        "Proprio Test", "test@test.com", "Resume", "url"
    )
    
    # Assert repository was called correctly
    mock_ajouter.assert_called_once_with(
        "Titre Test", "Auteur Test", "Business", 
        "Proprio Test", "test@test.com", "Resume", "url"
    )

def test_supprimer_livre_et_historique(mocker):
    mock_supprimer_livre = mocker.patch('src.repositories.livre_repository.supprimer_livre')
    mock_supprimer_historique = mocker.patch('src.repositories.historique_repository.supprimer_historique_livre')
    
    livre_service.supprimer_livre_et_historique(1)
    
    # Verify the order of operations: historique must be deleted before livre
    mock_supprimer_historique.assert_called_once_with(1)
    mock_supprimer_livre.assert_called_once_with(1)

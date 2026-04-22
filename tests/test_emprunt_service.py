import pytest
from src.services import emprunt_service

def test_process_emprunt_livre_introuvable(mocker):
    mocker.patch('src.repositories.livre_repository.get_livre', return_value=None)
    
    with pytest.raises(ValueError, match="Livre introuvable."):
        emprunt_service.process_emprunt(999, "Jean", "jean@test.com")

def test_process_emprunt_indisponible(mocker):
    mocker.patch('src.repositories.livre_repository.get_livre', return_value={"id": 1, "disponibilite": "Indisponible"})
    
    with pytest.raises(ValueError, match="Ce livre n'est pas disponible."):
        emprunt_service.process_emprunt(1, "Jean", "jean@test.com")

def test_process_emprunt_success(mocker):
    mocker.patch('src.repositories.livre_repository.get_livre', return_value={
        "id": 1, "disponibilite": "Disponible", "titre": "Livre Test", "proprietaire_email": "proprio@test.com"
    })
    mock_update = mocker.patch('src.repositories.livre_repository.update_disponibilite')
    mock_add = mocker.patch('src.repositories.historique_repository.ajouter_emprunt')
    mock_mail_proprio = mocker.patch('src.services.notification_service.envoyer_mail_emprunt_proprietaire')
    
    emprunt_service.process_emprunt(1, "Jean", "jean@test.com", "Merci")
    
    # Check DB was updated
    mock_update.assert_called_once_with(1, "Indisponible", "Jean")
    assert mock_add.called
    
    # Check Emails were sent
    assert mock_mail_proprio.called

def test_process_emprunt_email_failure_does_not_block(mocker):
    """Test that if email fails, the borrowing still succeeds."""
    mocker.patch('src.repositories.livre_repository.get_livre', return_value={
        "id": 1, "disponibilite": "Disponible", "titre": "Livre Test"
    })
    mocker.patch('src.repositories.livre_repository.update_disponibilite')
    mocker.patch('src.repositories.historique_repository.ajouter_emprunt')
    
    # Simulate email failure
    mocker.patch('src.services.notification_service.envoyer_mail_emprunt_proprietaire', side_effect=Exception("SMTP Error"))
    
    # Should not raise exception
    try:
        emprunt_service.process_emprunt(1, "Jean", "jean@test.com", "Merci")
    except Exception as e:
        pytest.fail(f"process_emprunt raised an exception when email failed: {e}")

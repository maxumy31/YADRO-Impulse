import pytest
from unittest.mock import MagicMock, patch
import uuid
from main import app as flask_app
from notification_repository import NotificationRepository
from model import *


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db():
    return MagicMock(spec=NotificationRepository)

def test_get_notification_success(client):
    '''
    Тестирует, что раут работает корректно: при запросе записи возвращает ее.
    '''
    target_id = str(uuid.uuid4())
    mock_notif = MagicMock()
    mock_notif.id = target_id
    mock_notif.status = NotificationStatus.SENT
    mock_notif.error_text = None

    with patch('notification_repository.NotificationRepository.get_by_id', return_value=mock_notif):
        response = client.get(f'/api/v1/notifications/{target_id}')
        
        assert response.status_code == 200
        assert response.json['id'] == target_id
        assert response.json['status'] == "sent"
        assert response.json['error'] == None

def test_get_notification_not_found(client):
    '''
    Тестирует, что раут возвращает только те записи, id которых совпадает с данными из запроса.
    '''
    random_id = str(uuid.uuid4())

    with patch('notification_repository.NotificationRepository.get_by_id', return_value=None):
        response = client.get(f'/api/v1/notifications/{random_id}')
        
        assert response.status_code == 404
        assert response.json['error'] == "Not found"

def test_get_notification_invalid_uuid_format(client):
    '''
    Тестирует, что раут работает только с валидными uuid.
    '''
    invalid_id = "not-a-uuid-12345"
    response = client.get(f'/api/v1/notifications/{invalid_id}')
    
    assert response.status_code == 404

